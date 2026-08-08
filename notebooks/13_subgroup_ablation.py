import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
RS=42
df=pd.read_csv('../data/pre_modelling_data.csv').sort_values(['PTID','Years.bl'])
g=df.groupby('PTID'); base_dx=g['DX'].first(); nvis=g.size(); seqs=g['DX'].apply(list); base=g.first().reset_index()
flags=[c for c in df.columns if c.endswith('null_flag')]; featflag=[c[:-9] for c in flags if c[:-9] in base.columns]
obs=base.copy()
for f in featflag: obs.loc[obs[f+'null_flag']==1,f]=np.nan
def confirmed(s,thr): return any(s[i]>=thr and s[i+1]>=thr for i in range(len(s)-1))
def dem_rev(s): return any(s[i]==2 and s[i+1]<2 for i in range(len(s)-1))
drop=set(seqs[seqs.apply(dem_rev)].index)
MRI=['Hippocampus','Entorhinal','MidTemp','Fusiform','Ventricles','WholeBrain']
FEATS=[c for c in base.columns if c not in ['PTID','Years.bl','Month.bl','DX','DX_change_flag','Last_Visit_DX_Flag','ICV'] and not c.endswith('null_flag')]
ids=[p for p in list(base_dx[base_dx==0].index)+list(base_dx[base_dx==1].index) if p not in drop and nvis[p]>=2]
sub=obs[obs['PTID'].isin(ids)].reset_index(drop=True)
y=np.array([int(confirmed(seqs[p],2)) for p in sub['PTID']])

GROUPS={'cognitive':['ADAS13','MMSE','MOCA','mPACCdigit','mPACCtrailsB','LDELTOTAL','RAVLT.immediate','RAVLT.learning','RAVLT.forgetting','RAVLT.perc.forgetting','TRABSCOR','CDRSB','FAQ'],
        'MRI':MRI,'PET':['AV45','FDG'],'CSF':['ABETA','TAU','PTAU'],'demo_gen':['AGE','PTEDUCAT','PTGENDER','APOE4','Married','Widowed','Divorced','Never_married']}

def oof_pred(feat_subset, Xall, y):
    skf=StratifiedKFold(5,shuffle=True,random_state=RS); oof=np.full(len(y),np.nan)
    for tr,te in skf.split(Xall,y):
        Xtr,Xte=Xall.iloc[tr].copy(),Xall.iloc[te].copy()
        im=IterativeImputer(estimator=BayesianRidge(),max_iter=5,random_state=RS)
        Xtr=pd.DataFrame(im.fit_transform(Xtr),columns=Xall.columns); Xte=pd.DataFrame(im.transform(Xte),columns=Xall.columns)
        ic=Xtr['ICV'].values.reshape(-1,1)
        for m in MRI:
            if m in Xtr: 
                lr=LinearRegression().fit(ic,Xtr[m]); Xtr[m]=Xtr[m]-lr.predict(ic); Xte[m]=Xte[m]-lr.predict(Xte['ICV'].values.reshape(-1,1))
        keep=[c for c in feat_subset if c in Xtr.columns]
        Xtr2=Xtr[keep]; Xte2=Xte[keep]
        sc=StandardScaler().fit(Xtr2)
        rf=RandomForestClassifier(n_estimators=400,max_depth=10,class_weight='balanced',random_state=RS,n_jobs=-1).fit(sc.transform(Xtr2),y[tr])
        oof[te]=rf.predict_proba(sc.transform(Xte2))[:,1]
    return oof

Xall=sub[FEATS+['ICV']].copy()
full=oof_pred(FEATS,Xall,y); full_auc=roc_auc_score(y,full)
print(f"### Ablation (Pooled->AD, ICV-resid, fold-wise) full AUC={full_auc:.3f} ###")
abl={'full':round(full_auc,3)}
for gname,gfeats in GROUPS.items():
    alone=oof_pred(gfeats,Xall,y); a_auc=roc_auc_score(y,alone)
    removed=oof_pred([c for c in FEATS if c not in gfeats],Xall,y); r_auc=roc_auc_score(y,removed)
    abl[gname]={'alone':round(a_auc,3),'removed':round(r_auc,3),'delta':round(r_auc-full_auc,3)}
    print(f"  {gname:12s} alone={a_auc:.3f} removed={r_auc:.3f} delta={r_auc-full_auc:+.3f}")

# ---- subgroup fairness (reuse full oof) ----
print("\n### Subgroup AUC (Pooled->AD) ###")
meta=sub.copy(); meta['pred']=full; meta['y']=y
sex=g['PTGENDER'].first(); apoe=g['APOE4'].first(); edu=g['PTEDUCAT'].first(); age=g['AGE'].first()
meta['sex']=meta['PTID'].map(sex); meta['apoe']=meta['PTID'].map(apoe); meta['edu']=meta['PTID'].map(edu); meta['age']=meta['PTID'].map(age)
sg={}
def auc_sub(mask,label):
    m=meta[mask]
    if m['y'].nunique()<2 or len(m)<30: return None
    a=roc_auc_score(m['y'],m['pred']); sg[label]={'n':int(len(m)),'events':int(m['y'].sum()),'auc':round(a,3)}
    print(f"  {label:16s} n={len(m)} events={int(m['y'].sum())} AUC={a:.3f}"); return a
auc_sub(meta['sex']==1,'Male'); auc_sub(meta['sex']==0,'Female')
auc_sub(meta['apoe']==0,'APOE4-neg'); auc_sub(meta['apoe']>=1,'APOE4-pos')
auc_sub(meta['edu']<16,'Education<16'); auc_sub(meta['edu']>=16,'Education>=16')
auc_sub(meta['age']<75,'Age<75'); auc_sub(meta['age']>=75,'Age>=75')

json.dump({'ablation':abl,'subgroup':sg}, open('reanalysis_subgroup_ablation.json','w'),indent=2)
print("\nSaved reanalysis_subgroup_ablation.json")
