import warnings; warnings.filterwarnings("ignore")
import numpy as np, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.calibration import calibration_curve
plt.rcParams.update({'figure.dpi':300,'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
C={'CN->progression':'#1f77b4','MCI->Dementia':'#ff7f0e','Pooled->AD':'#2ca02c'}
res=np.load('reanalysis_oof.npy',allow_pickle=True).item()
ext=json.load(open('reanalysis_extended.json')); surv=json.load(open('reanalysis_survival.json'))
sga=json.load(open('reanalysis_subgroup_ablation.json'))

# FIG 1 — ROC (RF) by cohort
plt.figure(figsize=(6.5,6))
for name in C:
    y=np.array(res[name]['_y']); p=np.array(res[name]['_oof']['RandomForest'])
    fpr,tpr,_=roc_curve(y,p); a=roc_auc_score(y,p)
    lbl=name.replace('->','→')
    plt.plot(fpr,tpr,color=C[name],lw=2,label=f"{lbl} (AUC {a:.2f})")
plt.plot([0,1],[0,1],'k--',lw=1,alpha=.5)
plt.xlabel('1 − Specificity'); plt.ylabel('Sensitivity')
plt.title('Figure 1. ROC by cohort (Random Forest, leakage-free)'); plt.legend(loc='lower right')
plt.tight_layout(); plt.savefig('figures/fig1_roc_cohorts.png'); plt.close()

# FIG (new) — Calibration curves (RF)
plt.figure(figsize=(6.5,6))
for name in C:
    y=np.array(res[name]['_y']); p=np.array(res[name]['_oof']['RandomForest'])
    frac,mean=calibration_curve(y,p,n_bins=8,strategy='quantile')
    plt.plot(mean,frac,'o-',color=C[name],lw=2,label=name.replace('->','→'))
plt.plot([0,1],[0,1],'k--',lw=1,alpha=.5,label='perfect calibration')
plt.xlabel('Mean predicted probability'); plt.ylabel('Observed frequency')
plt.title('Figure 6. Calibration curves (Random Forest)'); plt.legend(loc='upper left')
plt.tight_layout(); plt.savefig('figures/fig6_calibration.png'); plt.close()

# FIG 2 — predictors (ICV-residualized)
fig,axes=plt.subplots(1,3,figsize=(15,5))
for ax,name in zip(axes,C):
    d=ext['importance'][name]; items=list(d.items())[:8][::-1]
    ax.barh([k for k,_ in items],[v for _,v in items],color=C[name])
    ax.set_title(name.replace('->','→')); ax.set_xlabel('Δ ROC-AUC (permutation)')
fig.suptitle('Figure 2. Stage-dependent predictors (ICV-residualized, leakage-free)')
plt.tight_layout(); plt.savefig('figures/fig2_predictors.png'); plt.close()

# FIG 4 — Cox forest
hr=surv['cox_HR']['HR']; pv=surv['cox_HR']['p']
items=sorted(hr.items(),key=lambda x:x[1])
plt.figure(figsize=(7,6))
for i,(k,v) in enumerate(items):
    col='#d62728' if v>1 else '#1f77b4'
    plt.plot(v,i,'o',color=col); plt.text(v,i+0.15,f"{v:.2f}",fontsize=8,ha='center')
plt.axvline(1,ls='--',color='k',alpha=.5); plt.yticks(range(len(items)),[k for k,_ in items])
plt.xlabel('Hazard ratio per 1 SD'); plt.title('Figure 4. Cox PH: time to MCI→Dementia (ICV-residualized)')
plt.tight_layout(); plt.savefig('figures/fig4_cox_forest.png'); plt.close()

# FIG 5 — subgroup
sg=sga['subgroup']; labels=list(sg.keys()); aucs=[sg[k]['auc'] for k in labels]
plt.figure(figsize=(8,5))
plt.barh(labels[::-1],aucs[::-1],color='#2ca02c'); plt.xlim(0.7,0.95)
plt.axvline(0.882,ls='--',color='k',alpha=.5,label='overall 0.88')
for i,a in enumerate(aucs[::-1]): plt.text(a+0.002,i,f"{a:.2f}",va='center',fontsize=9)
plt.xlabel('ROC-AUC'); plt.title('Figure 5. Subgroup performance (Pooled→AD)'); plt.legend()
plt.tight_layout(); plt.savefig('figures/fig5_subgroup_fairness.png'); plt.close()
print("Figures regenerated:", "fig1_roc, fig2_predictors, fig4_cox, fig5_subgroup, fig6_calibration (300 DPI)")
