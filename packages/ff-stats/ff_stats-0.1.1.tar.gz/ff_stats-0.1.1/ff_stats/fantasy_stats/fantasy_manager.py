import pandas as pd
import numpy as np
from .utils import *
from .info.season_info import get_proteam_schedules, get_current_week
from .settings import league_settings, columns
from .info.espn_league_info import get_espn_info

from .scrapes.scrape_functions import pull_data



class FantasyManager:    
    def __init__(self, weeks, season, sources = None, positions = None, espn_league_id = None, cookies = None):
        self.sources = check_sources(sources)
        self.positions = check_positions(positions)
        self.weeks = check_weeks(weeks)
        
        
        self.current_week = get_current_week(season)
        
        self.season = str(season)
        
        
        self.scoring_settings = league_settings['scoring_settings']
        self.lineup_slots = league_settings['lineup_slots']
        self.flex_positions = league_settings['flex_positions']
        
        
    def get_projections(self, sources = None, positions = None, headers = None):
        if scrape == True:
            if sources is not None:
                self.sources = sources
            if positions is not None:
                self.positons = positions
                
        data = pull_data(self.sources, self.positions, self.weeks, self.current_week, self.season, headers)
        schedules = get_proteam_schedules(self.season, self.weeks, self.current_week)
        df = data.merge(schedules, how = 'left', on = ['team', 'week'])
        df = fix_gp(df, schedules, self.current_week)
        out_df = order_columns(df)
   
        self.data = out_df.copy()
        self.projections = out_df.copy()
   
       	return out_df


    def get_league_info(self, espn_league_id, cookies = None):
        self.teams, self.roster = get_espn_info(self.season, espn_league_id, cookies = cookies)
        
        print('ESPN league information retrieved')
        
        return self.teams
        
        
    def add_f_teams(self, in_df = None):

        df = in_df.copy() if in_df else self.projections.copy()
       
        df = source_sort(df)
        
        df = make_player_key(df)
        ids = df[['player_id', 'player_key']].groupby('player_key').first()
        ids = ids.player_id[ids.player_id != ''].reset_index() 
        
        df = df.drop('player_id', axis = 1).merge(ids, on = 'player_key', how = 'inner')
        out_df = df.merge(self.roster.rename(columns = {'team_id': 'f_team_id', 'team_name': 'f_team_name', 'playerId': 'player_id'}), on = 'player_id', how = 'left')
        out_df.loc[out_df.f_team_id.isna(), ['f_team_id', 'f_team_name']] = '-1', "Available"
        
        out_df = order_columns(out_df)
        
        if in_df is None: self.projections = out_df
    
        return out_df    
        
    def score_projections(self, in_df = None, score_settings = None):
        
        df = in_df.copy() if in_df else self.projections.copy()
        
        if score_settings is None:
            scoring_settings = self.scoring_settings
            
        score_values = pd.Series({key:scoring_settings[key] for key in scoring_settings.keys() if key in df.columns})
        df['total_pts'] = (df[score_values.index].apply(pd.to_numeric) * score_values.values).sum(axis = 1)
        df['avg_pts'] = df['total_pts']/df['gp']
        df.loc[(df.gp == 0), 'avg_pts'] = 0
        
        out_df = order_columns(df)
        
        if in_df is None: self.projections = out_df
        
        return out_df

    def combine_sources(self, in_df = None):
        
        df = in_df.copy() if in_df else self.projections.copy()
            
        aggregator = {col: 'first' for col in df.columns if col in ['player', 'team', 'pos', 'bye_week', 'opp', 'f_team_name', 'f_team_id']}
        aggregator.update({'source': 'count', 'index': 'first'})
        
        num_cols = [col for col in columns['numeric'] if col in df.columns]
        aggregator.update({col:'mean' for col in num_cols})
        df[num_cols] = df[num_cols].apply(pd.to_numeric)
        
        
        out_df = df.reset_index().groupby(['player_id', 'week'], as_index = False).agg(aggregator).sort_values(by = 'index').drop('index', axis = 1).reset_index(drop = True)
        out_df.rename(columns = {'source': 'source_count'}, inplace = True)
        
        out_df = order_columns(out_df)
        
        if in_df is None: self.projections = out_df
            
        return out_df
    
    def set_team_id(self, team_id):
        team = str(team_id)
        teams_df = self.teams
        if team in teams_df.team_id.to_list():
            self.team_id = team
            team_name, owner_name = teams_df.loc[teams_df.team_id == team, ['team_name', 'owner_name']].values[0]
            print('Team ID set as "{}", team name is "{}", owner name is "{}"'.format(team, team_name, owner_name))
        else:
            print('"{}" is not a value Team ID!'.format(team_id))
        
        return
    
    
    
    def get_best_lineup(self, in_df = None, scoring_period = None, include_fa = True, depth = 2, positions = None):
            
        slot_ids = {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 4, 'Flex': 5, 'DST': 6, 'K': 7}
        
        df = in_df.copy() if in_df else self.projections.copy()
        slots = self.lineup_slots
        
        if not scoring_period:
            scoring_period = self.current_week
        
        lineup = pd.DataFrame()
        df.sort_values(by = 'avg_pts', ascending = False, inplace = True)
        
        # Get starting roles first
        for ii in ['start', 'depth']:
            for pos in slots.keys():
                pos_list = self.flex_positions if pos == 'Flex' else [pos]
                
                if ii == 'start':
                    slot_size = slots[pos]
                    depth_num = 0
                else:
                    slot_size = depth
                    depth_num = slots[pos]
                
                temp_df = df.loc[(df.week == scoring_period)&(df.f_team_id.isin([self.team_id, '-1']))&(df.pos.isin(pos_list))][0:slot_size]
                temp_df['slot'] = ['{}{}'.format(pos, rank + 1) for rank in range(depth_num, depth_num+slot_size)]
                temp_df['slot_id'] = slot_ids[pos]
                
                temp_df.avg_pts = round(temp_df.avg_pts, 1)
            
                lineup = lineup.append(temp_df[['slot_id', 'slot', 'player', 'pos', 'team', 'opp', 'f_team_name', 'avg_pts']])
            
                df.drop(temp_df.index, inplace = True)
            
        lineup.sort_values(by = ['slot_id', 'slot'], inplace = True)
        lineup.drop('slot_id', axis = 1, inplace = True)
        lineup.set_index('slot', inplace = True)
                
        return lineup
if __name__ == 'main':
    FantasyManager()