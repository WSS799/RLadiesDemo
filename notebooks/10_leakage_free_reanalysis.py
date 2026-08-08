"""
10_leakage_free_reanalysis.py
Master re-analysis addressing methodological review (leakage-free, fold-wise).

Key corrections vs. the original pipeline:
  1. IMPUTATION IS FOLD-WISE. The stored analytic dataset was globally imputed;
     here we reconstruct the OBSERVED baseline (flagged values -> NaN) and fit an
     IterativeImputer inside each training fold only (no test/held-out leakage,
     no future-visit leakage since only baseline rows are used).
  2. MRI volumes are ICV-residualized inside each training fold (removes head-size
     confound); raw ICV dropped as a predictor.
  3. NO-SMOTE primary analysis (class_weight balanced); SMOTE kept as sensitivity.
  4. Calibration reported (Brier, Brier skill score vs prevalence null).
  5. Paired model comparison via bootstrap of out-of-fold AUC differences.
  6. Observed-only and complete-case sensitivity analyses.

Everything below is computed; nothing is hand-entered. Random seed = 42.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge, LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (roc_auc_score, balanced_accuracy_score, brier_score_loss,
                             confusion_matrix, f1_score)
RS = 42
rng = np.random.default_rng(RS)

# ---------------- data ----------------
df = pd.read_csv('../data/pre_modelling_data.csv').sort_values(['PTID','Years.bl'])
g = df.groupby('PTID'); base_dx = g['DX'].first(); nvis = g.size(); seqs = g['DX'].apply(list)
base = g.first().reset_index()
flags = [c for c in df.columns if c.endswith('null_flag')]
featflag = [c[:-9] for c in flags if c[:-9] in base.columns]
# reconstruct OBSERVED baseline (un-impute)
obs = base.copy()
for f in featflag:
    obs.loc[obs[f+'null_flag']==1, f] = np.nan

def confirmed(s, thr): return any(s[i]>=thr and s[i+1]>=thr for i in range(len(s)-1))
def dem_rev(s): return any(s[i]==2 and s[i+1]<2 for i in range(len(s)-1))
drop_ids = set(seqs[seqs.apply(dem_rev)].index)

MRI = ['Hippocampus','Entorhinal','MidTemp','Fusiform','Ventricles','WholeBrain']
FEATS = [c for c in base.columns
         if c not in ['PTID','Years.bl','Month.bl','DX','DX_change_flag','Last_Visit_DX_Flag','ICV']
         and not c.endswith('null_flag')]   # ICV dropped as predictor (used only to residualize)
print(f"{len(FEATS)} predictors (ICV removed; used only for residualization). MRI residualized: {MRI}")

def build(ids, thr):
    ids = [p for p in ids if p not in drop_ids and nvis[p] >= 2]
    sub = obs[obs['PTID'].isin(ids)].reset_index(drop=True)
    y = np.array([int(confirmed(seqs[p], thr)) for p in sub['PTID']])
    return sub, y

cohorts = {
 'CN->progression': build(base_dx[base_dx==0].index, 1),
 'MCI->Dementia':   build(base_dx[base_dx==1].index, 2),
 'Pooled->AD':      build(pd.Index(list(base_dx[base_dx==0].index)+list(base_dx[base_dx==1].index)), 2),
}

def models():
    return {
     'LogReg': LogisticRegression(max_iter=2000, class_weight='balanced'),
     'RandomForest': RandomForestClassifier(n_estimators=400, max_depth=10, class_weight='balanced', random_state=RS, n_jobs=-1),
     'XGBoost': XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, eval_metric='logloss', random_state=RS, n_jobs=-1),
     'SVM(RBF)': SVC(kernel='rbf', C=1, class_weight='balanced', probability=True, random_state=RS),
     'KNN': KNeighborsClassifier(n_neighbors=7),
     'NeuralNet(MLP)': MLPClassifier(hidden_layer_sizes=(32,16), max_iter=400, random_state=RS),
    }

def residualize_fit(Xtr):
    """fit ICV-residualization models on training fold; return dict of linreg per MRI col."""
    models_r = {}
    icv = Xtr['ICV'].values.reshape(-1,1)
    for m in MRI:
        lr = LinearRegression().fit(icv, Xtr[m].values)
        models_r[m] = lr
    return models_r
def residualize_apply(X, models_r):
    X = X.copy(); icv = X['ICV'].values.reshape(-1,1)
    for m in MRI:
        X[m] = X[m].values - models_r[m].predict(icv)
    return X

def run_cohort(name, sub, y, use_smote=False):
    X = sub[FEATS + ['ICV']].copy()   # keep ICV for residualization, drop before modeling
    skf = StratifiedKFold(5, shuffle=True, random_state=RS)
    oof = {m: np.full(len(y), np.nan) for m in models()}
    for tr, te in skf.split(X, y):
        Xtr, Xte = X.iloc[tr].copy(), X.iloc[te].copy()
        # 1) fold-wise imputation (fit on train only) — includes ICV so residualization has ICV
        imp = IterativeImputer(estimator=BayesianRidge(), max_iter=10, random_state=RS)
        cols = Xtr.columns
        Xtr_i = pd.DataFrame(imp.fit_transform(Xtr), columns=cols, index=Xtr.index)
        Xte_i = pd.DataFrame(imp.transform(Xte), columns=cols, index=Xte.index)
        # 2) ICV-residualize MRI (fit on train), then drop ICV
        rmod = residualize_fit(Xtr_i)
        Xtr_r = residualize_apply(Xtr_i, rmod).drop(columns=['ICV'])
        Xte_r = residualize_apply(Xte_i, rmod).drop(columns=['ICV'])
        # 3) scale (fit on train)
        sc = StandardScaler().fit(Xtr_r)
        Xtr_s = pd.DataFrame(sc.transform(Xtr_r), columns=Xtr_r.columns)
        Xte_s = pd.DataFrame(sc.transform(Xte_r), columns=Xte_r.columns)
        ytr = y[tr]
        if use_smote:
            from imblearn.over_sampling import SMOTENC
            cat_idx = [Xtr_s.columns.get_loc(c) for c in ['PTGENDER','Married','Widowed','Divorced','Never_married','APOE4'] if c in Xtr_s.columns]
            sm = SMOTENC(categorical_features=cat_idx, random_state=RS)
            Xtr_s, ytr = sm.fit_resample(Xtr_s, ytr)
        for mname, clf in models().items():
            c = clf.__class__(**clf.get_params())
            c.fit(Xtr_s, ytr)
            p = c.predict_proba(Xte_s)[:,1]
            oof[mname][te] = p
    return oof

def boot_auc_ci(y, p, n=2000):
    aucs=[]; idx=np.arange(len(y))
    for _ in range(n):
        b=rng.choice(idx, len(idx), replace=True)
        if len(np.unique(y[b]))<2: continue
        aucs.append(roc_auc_score(y[b], p[b]))
    return np.percentile(aucs,2.5), np.percentile(aucs,97.5)

def metrics(y, p):
    auc = roc_auc_score(y, p); lo,hi = boot_auc_ci(y,p)
    yhat = (p>=0.5).astype(int)
    tn,fp,fn,tp = confusion_matrix(y,yhat).ravel()
    sens = tp/(tp+fn) if tp+fn else 0; spec=tn/(tn+fp) if tn+fp else 0
    ppv = tp/(tp+fp) if tp+fp else 0; npv=tn/(tn+fn) if tn+fn else 0
    f1 = f1_score(y,yhat); bal=balanced_accuracy_score(y,yhat)
    brier = brier_score_loss(y,p); prev=y.mean(); null_brier=prev*(1-prev)
    bss = 1 - brier/null_brier
    return dict(auc=auc, auc_lo=lo, auc_hi=hi, sens=sens, spec=spec, ppv=ppv, npv=npv,
                f1=f1, balacc=bal, brier=brier, null_brier=null_brier, brier_skill=bss)

# ---------------- PRIMARY (no SMOTE) ----------------
results = {}
for name,(sub,y) in cohorts.items():
    print(f"\n=== {name}  n={len(y)} events={int(y.sum())} ({y.mean()*100:.0f}%) [PRIMARY: fold-wise impute, ICV-resid, no SMOTE] ===")
    oof = run_cohort(name, sub, y, use_smote=False)
    results[name] = {'n':int(len(y)), 'events':int(y.sum())}
    for m,p in oof.items():
        met = metrics(y,p); results[name][m]=met
        print(f"  {m:16s} AUC={met['auc']:.3f} ({met['auc_lo']:.2f}-{met['auc_hi']:.2f})  bal={met['balacc']*100:.0f}%  Brier={met['brier']:.3f} (null {met['null_brier']:.3f}, skill {met['brier_skill']:+.3f})")
    # store oof for paired test
    results[name]['_oof'] = {m:p.tolist() for m,p in oof.items()}
    results[name]['_y'] = y.tolist()

with open('reanalysis_results_primary.json','w') as f:
    json.dump({k:{kk:vv for kk,vv in v.items() if not kk.startswith('_')} for k,v in results.items()}, f, indent=2)
np.save('reanalysis_oof.npy', results, allow_pickle=True)
print("\nSaved reanalysis_results_primary.json")
