import pandas as pd
import requests
import numpy as np
import json
import time

def get_current_week(season):
    try:
        data = requests.get('https://fantasy.espn.com/apis/v3/games/ffl/seasons/'+str(season)).json()
        current_week = str(data.get('currentScoringPeriod')['id'])
        end_date = data.get('endDate')/1000
        
        if time.time() > end_date:
            current_week = -1
            print("Warning: Season has ended, try later season")
        
        return current_week

    except: raise Exception('Season is not valid!')

def get_proteam_schedules(season, weeks, current_week):
    r = requests.get('https://fantasy.espn.com/apis/v3/games/ffl/seasons/'+season+'?view=proTeamSchedules_wl')
    data = r.json()
            
    sch_weeks = [week for week in weeks if week != 'Rest of Season']
    if (current_week not in sch_weeks)&('Rest of Season' in weeks):
        sch_weeks.append(current_week)
    
    pull_df = pd.DataFrame()
    
    for team in data['settings']['proTeams']:
        if team.get('abbrev') == 'FA':
            # test = test.append(pd.Series(team), ignore_index = True)
            continue
        else:
            team.pop('teamPlayersByPosition')
            pull_df = pull_df.append(pd.DataFrame(team))
    pull_df[['awayProTeamId', 'homeProTeamId', 'scoringPeriodId']] = pull_df.proGamesByScoringPeriod.str[0].apply(pd.Series)[['awayProTeamId', 'homeProTeamId', 'scoringPeriodId']]
    pull_df = pull_df.drop('proGamesByScoringPeriod', axis = 1).sort_values(by = 'scoringPeriodId')
    
    pull_df = pull_df.astype(str).rename(columns = {'scoringPeriodId': 'week', 'abbrev': 'team', 'byeWeek': 'bye_week'})
    pull_df.team = pull_df.team.str.upper()
    
    byeWeeks = pull_df[['team', 'bye_week']].drop_duplicates()
    byeWeeks['week'] = byeWeeks['bye_week']
    
    pull_df = pull_df.append(byeWeeks)
    
    pull_df['opp_id'] = np.where(pull_df.id == pull_df.awayProTeamId, pull_df.homeProTeamId, pull_df.awayProTeamId)
    teams = pull_df[~pull_df.id.isna()][['team', 'id']].drop_duplicates()
    
    pull_df = pull_df.merge(teams, how = 'left', left_on = 'opp_id', right_on = 'id', suffixes = ['', '_opp'])
    
    pull_df['opp'] = pull_df['team_opp']
    pull_df.loc[pull_df.id == pull_df.awayProTeamId, 'opp'] = '@' + pull_df[pull_df.id == pull_df.awayProTeamId]['opp']
    
    
    if 'Rest of Season' in weeks:
        ros = pull_df[pull_df.week == current_week][['team', 'bye_week', 'opp']]
        ros['week'] = 'Rest of Season'
        pull_df = pull_df.append(ros)
        
    return pull_df[['team', 'bye_week', 'week', 'opp']].fillna('bye')