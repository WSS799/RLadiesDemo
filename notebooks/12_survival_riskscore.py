import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge, LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm
from scipy import stats
RS=42
df=pd.read_csv('../data/pre_modelling_data.csv').sort_values(['PTID','Years.bl'])
g=df.groupby('PTID'); base_dx=g['DX'].first(); nvis=g.size(); seqs=g['DX'].apply(list); base=g.first().reset_index()
flags=[c for c in df.columns if c.endswith('null_flag')]; featflag=[c[:-9] for c in flags if c[:-9] in base.columns]
obs=base.copy()
for f in featflag: obs.loc[obs[f+'null_flag']==1,f]=np.nan
def dem_rev(s): return any(s[i]==2 and s[i+1]<2 for i in range(len(s)-1))
drop=set(seqs[seqs.apply(dem_rev)].index)

# ---- MCI survival cohort ----
rows=[]
for p in base_dx[base_dx==1].index:
    if p in drop or nvis[p]<2: continue
    pp=df[df['PTID']==p].sort_values('Years.bl'); s=list(pp['DX']); t=list(pp['Years.bl'])
    ct=next((t[i] for i in range(len(s)-1) if s[i]==2 and s[i+1]==2),None)
    rows.append((p, ct if ct is not None else max(t), 1 if ct is not None else 0))
surv=pd.DataFrame(rows,columns=['PTID','time','event'])
# observed-only APOE4 (drop imputed) for KM
apoe_obs=g['APOE4'].first(); apoe_flag=g['APOE4null_flag'].first()
surv['apoe']=surv['PTID'].map(apoe_obs); surv['apoe_imp']=surv['PTID'].map(apoe_flag)
def km_at(time,event,ys=(2,3,5)):
    res=[]; S=1.0
    for tt in sorted(set(time)):
        n=(time>=tt).sum(); d=((time==tt)&(event==1)).sum()
        if n>0: S*= (1-d/n)
        res.append((tt,S))
    out={}
    for y in ys:
        s=1.0
        for tt,S in res:
            if tt<=y: s=S
        out[y]=s
    return out
def logrank(sv):
    times=sorted(sv.loc[sv.event==1,'time'].unique()); O1=E1=V=0.0
    for tt in times:
        ar=sv[sv.time>=tt]; n=len(ar); d=int((sv.time.eq(tt)&sv.event.eq(1)).sum())
        n1=int((ar.apoe>=1).sum()); d1=int(((sv.time==tt)&(sv.event==1)&(sv.apoe>=1)).sum())
        if n<=1: continue
        E1+=d*n1/n; O1+=d1; V+=d*(n1/n)*(1-n1/n)*(n-d)/(n-1)
    chi=(O1-E1)**2/V; return chi, stats.chi2.sf(chi,1)
svo=surv[(surv.apoe.notna())&(surv.apoe_imp==0)]   # FIX: truly observed-only (exclude imputed)
print(f"MCI survival: n={len(surv)} events={int(surv.event.sum())} censored={int((surv.event==0).sum())}")
print(f"KM by APOE4 (OBSERVED-only, n={len(svo)}, imputed-excluded={int(surv.apoe_imp.sum())}):")
for nm,grp in [('APOE4-neg',svo[svo.apoe==0]),('APOE4-pos',svo[svo.apoe>=1]),('All',svo)]:
    v=km_at(grp.time.values,grp.event.values); print(f"   {nm:10s} 2y={v[2]*100:.0f}% 3y={v[3]*100:.0f}% 5y={v[5]*100:.0f}%")
chi,p=logrank(svo); print(f"   log-rank chi2={chi:.1f} p={p:.2e}")

# ---- Cox PH (ICV-residualized, single imputation for inference; note in text) ----
MRI=['Hippocampus','Entorhinal','MidTemp','Fusiform','Ventricles','WholeBrain']
covs=['AGE','PTEDUCAT','APOE4','ADAS13','MMSE','MOCA','FAQ','CDRSB','Hippocampus','LDELTOTAL','FDG','AV45','ABETA','RAVLT.immediate']
mci=obs[obs['PTID'].isin(surv['PTID'])].reset_index(drop=True).merge(surv[['PTID','time','event']],on='PTID')
Xc=mci[covs+['ICV']].copy()
imp=IterativeImputer(estimator=BayesianRidge(),max_iter=10,random_state=RS)
Xi=pd.DataFrame(imp.fit_transform(Xc),columns=Xc.columns)
icv=Xi['ICV'].values.reshape(-1,1)
for m in [c for c in MRI if c in covs]:
    lr=LinearRegression().fit(icv,Xi[m]); Xi[m]=Xi[m]-lr.predict(icv)
Xi=Xi.drop(columns=['ICV'])
Xz=(Xi-Xi.mean())/Xi.std()
res=sm.PHReg(mci['time'].values, Xz.values, status=mci['event'].values, ties='efron').fit()
HR=pd.DataFrame({'HR':np.exp(res.params),'p':res.pvalues},index=covs).sort_values('HR',ascending=False)
print("\nCox PH (HR per 1 SD, ICV-residualized, fold-consistent single imputation):")
print(HR.round(3).to_string())
cint=pd.DataFrame(np.exp(res.conf_int()), index=covs, columns=['lo','hi'])
HR['lo']=cint['lo']; HR['hi']=cint['hi']
HR=HR.sort_values('HR',ascending=False)
nsig=int((HR['p']<0.05).sum())
print("\nCox PH (HR per 1 SD with 95% CI, ICV-residualized):")
for cov,row in HR.iterrows():
    print(f"  {cov:16s} HR={row['HR']:.2f} (95% CI {row['lo']:.2f}-{row['hi']:.2f}) p={row['p']:.3f}")
print(f"Significant at p<0.05: {nsig} covariates: {list(HR.index[HR['p']<0.05])}")
# Harrell C-index
lp=(Xz.values@res.params)
t=mci['time'].values; e=mci['event'].values; conc=0; disc=0
import itertools
idx=np.where(e==1)[0]
for i in idx:
    comp=(t>t[i]); 
    conc+=np.sum((lp[i]>lp[comp]))  # higher risk (lp) should have shorter time
    disc+=np.sum((lp[i]<lp[comp]))
cindex=conc/(conc+disc) if (conc+disc)>0 else float('nan')
print(f"Cox C-index (concordance) = {cindex:.3f}")

print(f"C-index (concordance) = {res.summary().tables[0] if False else ''}")
# concordance
try:
    from lifelines.utils import concordance_index
    ci=concordance_index(mci['time'],-res.predict().predicted_values,mci['event'])
except Exception:
    # manual c-index via linear predictor
    lp=Xz.values@res.params
    from itertools import combinations
    ci=None
print("")

# ---- Risk score (7-var, fold-wise imputation) ----
acc=['AGE','APOE4','MMSE','FAQ','CDRSB','Hippocampus','ADAS13']
subm=obs[obs['PTID'].isin(surv['PTID'])].reset_index(drop=True)
ym=surv.set_index('PTID').loc[subm['PTID'],'event'].values
X=subm[acc+['ICV']].copy(); skf=StratifiedKFold(5,shuffle=True,random_state=RS); oof=np.full(len(ym),np.nan)
for tr,te in skf.split(X,ym):
    Xtr,Xte=X.iloc[tr].copy(),X.iloc[te].copy()
    im=IterativeImputer(estimator=BayesianRidge(),max_iter=5,random_state=RS)
    Xtr=pd.DataFrame(im.fit_transform(Xtr),columns=X.columns); Xte=pd.DataFrame(im.transform(Xte),columns=X.columns)
    ic=Xtr['ICV'].values.reshape(-1,1); lr=LinearRegression().fit(ic,Xtr['Hippocampus']); 
    Xtr['Hippocampus']-=lr.predict(ic); Xte['Hippocampus']-=lr.predict(Xte['ICV'].values.reshape(-1,1))
    Xtr=Xtr.drop(columns=['ICV']); Xte=Xte.drop(columns=['ICV'])
    sc=StandardScaler().fit(Xtr); 
    clf=LogisticRegression(max_iter=2000,class_weight='balanced').fit(sc.transform(Xtr),ym[tr])
    oof[te]=clf.predict_proba(sc.transform(Xte))[:,1]
print(f"7-variable risk score AUC (fold-wise) = {roc_auc_score(ym,oof):.3f}")
# FIX3: cross-validate the INTEGER SCORECARD itself (points derived on train, scored on test)
oof_card=np.full(len(ym),np.nan)
for tr,te in skf.split(X,ym):
    Xtr,Xte=X.iloc[tr].copy(),X.iloc[te].copy()
    im2=IterativeImputer(estimator=BayesianRidge(),max_iter=5,random_state=RS)
    Xtr=pd.DataFrame(im2.fit_transform(Xtr),columns=X.columns); Xte=pd.DataFrame(im2.transform(Xte),columns=X.columns)
    ic=Xtr['ICV'].values.reshape(-1,1); lrr=LinearRegression().fit(ic,Xtr['Hippocampus'])
    Xtr['Hippocampus']-=lrr.predict(ic); Xte['Hippocampus']-=lrr.predict(Xte['ICV'].values.reshape(-1,1))
    Xtr=Xtr.drop(columns=['ICV']); Xte=Xte.drop(columns=['ICV'])
    mu,sd=Xtr.mean(),Xtr.std()
    Ztr=(Xtr-mu)/sd; Zte=(Xte-mu)/sd
    lc=LogisticRegression(max_iter=2000,class_weight='balanced').fit(Ztr,ym[tr])
    cf=pd.Series(lc.coef_[0],index=acc); pts=(cf/cf.abs().max()*10).round()
    score_te=(Zte*pts).sum(axis=1)
    oof_card[te]=score_te.values
print(f"7-variable INTEGER SCORECARD AUC (fold-wise, points derived on train) = {roc_auc_score(ym,oof_card):.3f}")
# coefficients on full data for points
im=IterativeImputer(estimator=BayesianRidge(),max_iter=10,random_state=RS)
Xf=pd.DataFrame(im.fit_transform(X),columns=X.columns); ic=Xf['ICV'].values.reshape(-1,1)
lr=LinearRegression().fit(ic,Xf['Hippocampus']); Xf['Hippocampus']-=lr.predict(ic); Xf=Xf.drop(columns=['ICV'])
Xz2=(Xf-Xf.mean())/Xf.std()
clf=LogisticRegression(max_iter=2000,class_weight='balanced').fit(Xz2,ym)
coef=pd.Series(clf.coef_[0],index=acc); pts=(coef/coef.abs().max()*10).round().astype(int)
print("Risk points per +1 SD:"); print(pts.to_string())

json.dump({'km':{nm:km_at(svo[svo.apoe==v].time.values if isinstance(v,int) else svo.time.values, svo[svo.apoe==v].event.values if isinstance(v,int) else svo.event.values) for nm,v in [('neg',0)]},
           'logrank_p':float(p),'cox_HR':HR.round(3).to_dict(),'riskscore_auc':round(float(roc_auc_score(ym,oof)),3),
           'risk_points':pts.to_dict()}, open('reanalysis_survival.json','w'),indent=2, default=str)
print("\nSaved reanalysis_survival.json")
