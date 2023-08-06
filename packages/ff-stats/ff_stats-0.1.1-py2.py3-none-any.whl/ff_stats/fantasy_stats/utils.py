import pandas as pd
import numpy as np
from .settings import columns, valid_sources, valid_positions, valid_weeks

def make_player_key(df):
    out_df = df.copy()
    
    name_split = out_df.player.str.split(" ")
    f,l = [name_split.str[i].str.replace(r'[\W_]+', '', regex = True).str[0:4] for i in [0,1]]
    out_df['player_key'] = (f + l + out_df.pos+out_df.team).str.lower()
    
    return out_df

def source_sort(df):
    out_df = df.copy()
    all_sources = ['ESPN', 'NFL', 'number_fire', 'fantasy_sharks', 'CBS', 'FantasyPros', 'fleaflicker', 'FFToday']
    
    out_df['sort'] = -1
    for ii in range(0,len(all_sources)):
        out_df.loc[out_df.source == all_sources[ii], 'sort'] = ii
    
    out_df = out_df.reset_index().sort_values(by = ['sort', 'index']).drop(['sort', 'index'], axis = 1).reset_index(drop = True)

    return out_df

def order_columns(df):
     cols = [col for col in columns['categorical']+columns['numeric'] if col in df.columns]
     
     out_df = df[cols]
     
     return out_df
 
def fix_gp(data, schedules, current_week):
    df = data.copy()
    
    df.loc[df.gp == '', 'gp'] = np.nan
    df.gp = df.gp.astype(float)
    df.loc[(df.gp.isna())&(df.week != 'Rest of Season'), 'gp'] = 1
    df.loc[(df.week != 'Rest of Season')&(df.opp == 'bye'), 'gp'] = 0
    
    gl = schedules.loc[(schedules.week != 'Rest of Season')&(schedules.opp != 'bye'), ['team', 'week']]
    gl.week = gl.week.astype(int)
    gl=gl[gl.week >= int(current_week)].groupby('team').count().rename(columns = {'week': 'games_left'})
    
    
    for team in gl.index:
        df.loc[(df.team == team)&(df.week == 'Rest of Season'), 'gp'] = gl.loc[team, 'games_left']
    
    df.loc[(df.team == 'FA')&(df.week == 'Rest of Season'), 'gp'] = max(gl.games_left)
    
    return df

def check_sources(sources = None):
    if sources is None:
        return valid_sources
    try:
        if not isinstance(sources, list):
            sources = [sources]
        
        invalid_sources = [source for source in sources if source not in valid_sources]
        if invalid_sources:
            raise Exception('"{}" is not a valid source! \nValid sources are: {}'.format(invalid_sources[0], ', '.join(valid_sources)))
        return sources
    
    except: raise Exception('Sources are not valid!')
       

def check_positions(positions = None):
    if positions is None:
        return valid_positions
    
    try:
        if not isinstance(positions, list):
            positions = [positions]
        
        invalid_positions = [pos for pos in positions if pos.lower() not in valid_positions]
        if invalid_positions:
            raise Exception('"{}" is not a valid position! \nValid positions are: {}'.format(invalid_positions[0], ', '.join(valid_positions)))
        
        return [pos.lower() for pos in positions if pos.lower() in valid_positions]
    except: raise Exception('Positions are not valid!')


def check_weeks(weeks):
    if not isinstance(weeks, list):
        weeks = [weeks]
    try:   
        invalid_weeks = [week for week in weeks if str(week) not in valid_weeks]    
        if invalid_weeks:
            raise Exception('"{}" is not a valid week! \nValid weeks are: {}'.format(invalid_weeks[0], ', '.join(valid_weeks)))
        
        return [str(week) for week in weeks if str(week) in valid_weeks]
    
    except: raise Exception('Weeks are not valid!')