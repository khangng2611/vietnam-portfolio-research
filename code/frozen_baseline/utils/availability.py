"""Availability contract for a declared valuation-proxy research protocol.

An assigned policy time is a simulation assumption, never a claim that the
historical first-publication timestamp was independently observed.
"""
import numpy as np
import pandas as pd

def build_asof_panel(records,calendar,cutoff_hour=18):
    required={'asset','observed_at','available_at','price','availability_basis','source'}
    if not required.issubset(records.columns):
        raise ValueError('Missing availability record fields')
    r=records.copy()
    for key in ['observed_at','available_at']:
        if r[key].isna().any() or any(pd.Timestamp(x).tzinfo is None for x in r[key]):
            raise ValueError('Unknown or timezone-naive availability')
        r[key]=pd.to_datetime(r[key],utc=True)
    if (r.available_at<r.observed_at).any():
        raise ValueError('Impossible observation/availability chronology')
    r['price']=pd.to_numeric(r.price,errors='raise')
    if not np.isfinite(r.price).all() or r.price.le(0).any():
        raise ValueError('Nonpositive or nonfinite price')
    if r[['asset','availability_basis','source']].isna().any().any():
        raise ValueError('Unknown availability identity')
    keys=['asset','observed_at','available_at']
    if r.groupby(keys).price.nunique().gt(1).any():
        raise ValueError('conflicting records at the same availability cutoff')
    r=r.drop_duplicates(keys).sort_values(['asset','available_at','observed_at'])
    dates=pd.DatetimeIndex(calendar)
    if dates.tz is not None or dates.has_duplicates or not dates.is_monotonic_increasing:
        raise ValueError('Calendar must be unique ordered local dates')
    panel=pd.DataFrame(index=dates,columns=sorted(r.asset.unique()),dtype=float)
    decisions=(dates+pd.Timedelta(hours=cutoff_hour)).tz_localize('Asia/Ho_Chi_Minh').tz_convert('UTC')
    ledger=[]
    for asset,group in r.groupby('asset',sort=False):
        rows=group.to_dict('records');j=0;best=None
        for date,decision in zip(dates,decisions):
            while j<len(rows) and rows[j]['available_at']<=decision:
                candidate=rows[j]
                if best is None or (candidate['observed_at'],candidate['available_at'])>(best['observed_at'],best['available_at']):
                    best=candidate
                j+=1
            if best is None:continue
            panel.at[date,asset]=best['price']
            ledger.append(dict(session_date=str(date.date()),decision_at=decision.isoformat(),asset=asset,
                               observed_at=best['observed_at'].isoformat(),available_at=best['available_at'].isoformat(),
                               price=best['price'],availability_basis=best['availability_basis'],source=best['source'],
                               observation_age_days=int((decision-best['observed_at']).total_seconds()//86400)))
    return panel,pd.DataFrame(ledger)

def readiness_status(checks,*,scope,assumptions,historical_publication_verified):
    required=['complete_inputs','causal_features_labels','availability_protocol_enforced','next_close_execution',
              'constraints_nav_turnover','ml_bl_selection_provenance','deterministic_repeat','mvo_reconciled','metadata_documented']
    if scope not in ['valuation_proxy','strict_historical']:
        raise ValueError('Unknown research scope')
    blockers=[key for key in required if checks.get(key) is not True]
    if scope=='strict_historical' and historical_publication_verified is not True:
        blockers.append('observed_historical_publication')
    return dict(status='NOT READY FOR STEP 2' if blockers else 'READY FOR STEP 2',scope=scope,
                historical_publication_verified=historical_publication_verified is True,
                assumptions=list(assumptions),blocking_checks=blockers,
                actual_fund_execution_or_live_trading_certified=False)
