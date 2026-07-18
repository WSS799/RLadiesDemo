import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge, LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from scipy import stats
RS=42; rng=np.random.default_rng(RS)

df=pd.read_csv('../data/pre_modelling_data.csv').sort_values(['PTID','Years.bl'])
g=df.groupby('PTID'); base_dx=g['DX'].first(); nvis=g.size(); seqs=g['DX'].apply(list); base=g.first().reset_index()
flags=[c for c in df.columns if c.endswith('null_flag')]; featflag=[c[:-9] for c in flags if c[:-9] in base.columns]
obs=base.copy()
for f in featflag: obs.loc[obs[f+'null_flag']==1,f]=np.nan
def confirmed(s,thr): return any(s[i]>=thr and s[i+1]>=thr for i in range(len(s)-1))
def dem_rev(s): return any(s[i]==2 and s[i+1]<2 for i in range(len(s)-1))
drop_ids=set(seqs[seqs.apply(dem_rev)].index)
MRI=['Hippocampus','Entorhinal','MidTemp','Fusiform','Ventricles','WholeBrain']
FEATS=[c for c in base.columns if c not in ['PTID','Years.bl','Month.bl','DX','DX_change_flag','Last_Visit_DX_Flag','ICV'] and not c.endswith('null_flag')]
def build(ids,thr):
    ids=[p for p in ids if p not in drop_ids and nvis[p]>=2]
    sub=obs[obs['PTID'].isin(ids)].reset_index(drop=True)
    y=np.array([int(confirmed(seqs[p],thr)) for p in sub['PTID']]); return sub,y
cohorts={'CN->progression':build(base_dx[base_dx==0].index,1),
 'MCI->Dementia':build(base_dx[base_dx==1].index,2),
 'Pooled->AD':build(pd.Index(list(base_dx[base_dx==0].index)+list(base_dx[base_dx==1].index)),2)}

def process_fold(Xtr,Xte):
    imp=IterativeImputer(estimator=BayesianRidge(),max_iter=5,random_state=RS); cols=Xtr.columns
    Xtr_i=pd.DataFrame(imp.fit_transform(Xtr),columns=cols,index=Xtr.index)
    Xte_i=pd.DataFrame(imp.transform(Xte),columns=cols,index=Xte.index)
    icv=Xtr_i['ICV'].values.reshape(-1,1)
    for m in MRI:
        lr=LinearRegression().fit(icv,Xtr_i[m].values)
        Xtr_i[m]=Xtr_i[m]-lr.predict(icv); Xte_i[m]=Xte_i[m]-lr.predict(Xte_i['ICV'].values.reshape(-1,1))
    Xtr_i=Xtr_i.drop(columns=['ICV']); Xte_i=Xte_i.drop(columns=['ICV'])
    sc=StandardScaler().fit(Xtr_i)
    return pd.DataFrame(sc.transform(Xtr_i),columns=Xtr_i.columns), pd.DataFrame(sc.transform(Xte_i),columns=Xte_i.columns)

# ---------- (1) permutation importance (leakage-free, RF) ----------
print("### Permutation importance (ICV-residualized, fold-wise impute, RF) ###")
imp_out={}
for name,(sub,y) in cohorts.items():
    X=sub[FEATS+['ICV']].copy(); skf=StratifiedKFold(5,shuffle=True,random_state=RS)
    agg=np.zeros(len(FEATS))
    for tr,te in skf.split(X,y):
        Xtr_s,Xte_s=process_fold(X.iloc[tr].copy(),X.iloc[te].copy())
        rf=RandomForestClassifier(n_estimators=400,max_depth=10,class_weight='balanced',random_state=RS,n_jobs=-1).fit(Xtr_s,y[tr])
        r=permutation_importance(rf,Xte_s,y[te],n_repeats=3,scoring='roc_auc',random_state=RS,n_jobs=-1)
        agg+=r.importances_mean
    ser=pd.Series(agg/5,index=Xtr_s.columns).sort_values(ascending=False)
    imp_out[name]=ser.head(10).round(4).to_dict()
    print(f"\n{name} top10:"); print(ser.head(10).round(4).to_string())

# ---------- (2) SMOTE(NC) & complete-case sensitivity (RF, LR) ----------
from imblearn.over_sampling import SMOTENC
def cv_auc(sub,y,which='primary'):
    X=sub[FEATS+['ICV']].copy(); skf=StratifiedKFold(5,shuffle=True,random_state=RS)
    oof={'RF':np.full(len(y),np.nan),'LR':np.full(len(y),np.nan)}
    for tr,te in skf.split(X,y):
        Xtr_s,Xte_s=process_fold(X.iloc[tr].copy(),X.iloc[te].copy()); ytr=y[tr]
        if which=='smote':
            cat=[Xtr_s.columns.get_loc(c) for c in ['PTGENDER','Married','Widowed','Divorced','Never_married','APOE4'] if c in Xtr_s.columns]
            Xtr_s,ytr=SMOTENC(categorical_features=cat,random_state=RS).fit_resample(Xtr_s,ytr)
        for k,clf in [('RF',RandomForestClassifier(n_estimators=400,max_depth=10,class_weight=None if which=='smote' else 'balanced',random_state=RS,n_jobs=-1)),
                      ('LR',LogisticRegression(max_iter=2000,class_weight=None if which=='smote' else 'balanced'))]:
            clf.fit(Xtr_s,ytr); oof[k][te]=clf.predict_proba(Xte_s)[:,1]
    return {k:roc_auc_score(y,v) for k,v in oof.items()}
print("\n### SMOTE-NC sensitivity (vs primary no-SMOTE) ###")
sens={}
for name,(sub,y) in cohorts.items():
    prim=cv_auc(sub,y,'primary'); smo=cv_auc(sub,y,'smote')
    sens[name]={'primary':prim,'smote':smo}
    print(f"  {name}: RF primary {prim['RF']:.3f} vs SMOTE {smo['RF']:.3f} | LR primary {prim['LR']:.3f} vs SMOTE {smo['LR']:.3f}")

# complete-case (drop rows with any missing among a reduced always-available set? use full 32 -> complete cases only)
print("\n### Complete-case sensitivity (rows with all predictors observed) ###")
cc={}
for name,(sub,y) in cohorts.items():
    mask=sub[FEATS+['ICV']].notna().all(axis=1).values
    n_cc=int(mask.sum()); ev=int(y[mask].sum())
    cc[name]={'n':n_cc,'events':ev}
    print(f"  {name}: complete cases n={n_cc}/{len(y)} events={ev}")
    if n_cc>50 and ev>10 and (y[mask].sum()>0):
        subc=sub[mask].reset_index(drop=True); yc=y[mask]
        try:
            r=cv_auc(subc,yc,'primary'); cc[name]['RF_auc']=round(r['RF'],3); cc[name]['LR_auc']=round(r['LR'],3)
            print(f"     complete-case RF AUC={r['RF']:.3f} LR AUC={r['LR']:.3f}")
        except Exception as e: print("     (skip:",e,")")

# ---------- (3) observed-only PTAU-TAU ----------
o2=df[(df['PTAUnull_flag']==0)&(df['TAUnull_flag']==0)]
print(f"\n### Observed-only corr(PTAU,TAU) = {o2['PTAU'].corr(o2['TAU']):.3f} (n={len(o2)}); all-rows = {df['PTAU'].corr(df['TAU']):.3f}")

# ---------- (4) paired model comparison (bootstrap AUC diff, pooled) ----------
res=np.load('reanalysis_oof.npy',allow_pickle=True).item()
print("\n### Paired AUC comparison (bootstrap 95% CI of difference) ###")
paired={}
for name in cohorts:
    y=np.array(res[name]['_y']); oof=res[name]['_oof']
    # top model vs LogReg
    aucs={m:roc_auc_score(y,np.array(p)) for m,p in oof.items()}
    best=max(aucs,key=aucs.get)
    for comp in [best,'LogReg']:
        pass
    diffs=[]
    idx=np.arange(len(y)); pa=np.array(oof[best]); pb=np.array(oof['LogReg'])
    for _ in range(2000):
        b=rng.choice(idx,len(idx),replace=True)
        if len(np.unique(y[b]))<2: continue
        diffs.append(roc_auc_score(y[b],pa[b])-roc_auc_score(y[b],pb[b]))
    lo,hi=np.percentile(diffs,2.5),np.percentile(diffs,97.5)
    paired[name]={'best':best,'auc_best':round(aucs[best],3),'auc_LR':round(aucs['LogReg'],3),'diff_lo':round(lo,3),'diff_hi':round(hi,3)}
    print(f"  {name}: {best} {aucs[best]:.3f} vs LogReg {aucs['LogReg']:.3f}; diff 95%CI [{lo:+.3f},{hi:+.3f}] -> {'NOT distinguishable' if lo<0<hi else 'differ'}")

json.dump({'importance':imp_out,'smote_sensitivity':sens,'complete_case':cc,'paired':paired,
           'ptau_tau_observed':round(float(o2['PTAU'].corr(o2['TAU'])),3)},
          open('reanalysis_extended.json','w'),indent=2)
print("\nSaved reanalysis_extended.json")
