import numpy as np


def fixed_targets(assets,selected):
    if len(assets)!=len(set(assets)) or len(selected)!=5 or len(set(selected))!=5 or any(a in ['GOLD','VFF'] for a in selected):
        raise ValueError('Need exactly five distinct equities and unique asset columns')
    if not set(selected+['GOLD','VFF']).issubset(assets):raise ValueError('Missing fixed-rule instrument')
    w=np.zeros(len(assets));w[[assets.index(a) for a in selected+['GOLD']]]=.7/6;w[assets.index('VFF')]=.3
    return w
