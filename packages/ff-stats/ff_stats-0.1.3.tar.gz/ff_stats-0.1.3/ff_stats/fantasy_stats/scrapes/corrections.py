import pandas as pd
from .standardization_references import pos_fix_dict, name_fix_dict, team_names

def sum_and_drop_cols(df, column_dict, drop = True):
    if not all([isinstance(v, list) for v in column_dict.values()]):
        raise Exception('Dictionary values must be lists')
    
    for key in column_dict:
        df[key] = df[column_dict[key]].sum(axis = 1)
    

    if drop == True:
        drop_cols = {col for cols in column_dict.values() for col in cols}
        df.drop(drop_cols, axis = 1, inplace = True)
    
    return df

def add_dst_teams(df, dict_key = None):
    if dict_key is not None:
        dic = team_names[dict_key]
        for key in dic:
            df.loc[(df.player == key)&(df.pos == 'DST'), 'team'] = dic[key]
    
    teams = team_names['reverse_full_name']
    for team in teams:
        df.loc[(df.pos == 'DST')&(df.team == team), 'player'] = teams[team] + " DST"
            
    return df
    
def team_fix(df):
    for key in team_names['team_abb_corrections']:
        df.loc[df.team == key, 'team'] = team_names['team_abb_corrections'][key]
    return df

def ad_hoc_fixes(data):
    # Cordalle Patterson fixes
    for source in data.source.drop_duplicates().to_list():
        if len(data[(data.player == 'Cordarrelle Patterson')&(data.source == source)]['pos'].drop_duplicates()) > 1:
            i = data[(data.player == 'Cordarrelle Patterson')&(data.source == source)&(data.pos == 'WR')].index
            data.drop(i, inplace = True)
    
    for p in pos_fix_dict:
        for name in pos_fix_dict[p]:
            data.loc[data.player == name, 'pos'] = p
    
    for name in name_fix_dict:
        data.loc[data.player == name, 'player'] = name_fix_dict[name]

    return data