import requests
import json
import pandas as pd


def get_espn_info(season, espn_league_id, cookies = None):
    r = requests.get('https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}'.format(season, espn_league_id),
                      params={ 'view': ['mTeam', 'mRoster', 'mSettings']},
                      cookies = cookies)
    
    if r.status_code in [400, 404]:
        raise Exception("League not found! Please check 'espn_league_id'")

    elif r.status_code == 401:
        raise Exception("This is a private ESPN league and you are not authorized to view this league. Please check or include the 'cookie' parameters.")
    
    elif r.status_code != 200:
            print(r.status_code)
            raise Exception("Unable to import ESPN League information.") 
    
    data = r.json()
    
    teams, roster = get_league_teams(data)
    members = get_league_members(data)

    
    teams = teams.merge(members[['display_name', 'owner_id', 'owner_name']],on = 'owner_id', how = 'left')
    teams.drop(['location', 'nickname', 'owner_id'], axis = 1, inplace = True)
    
    roster = roster.astype(str).merge(teams[['team_id', 'team_name']], on = 'team_id', how = 'left')
    
    return teams, roster
    
def get_league_teams(data):
    teams = pd.DataFrame()
    roster = pd.DataFrame()
    for team in data['teams']:
        temp_roster = pd.DataFrame(team['roster']['entries'])
        temp_roster['team_id'] = team.get('id')
        roster = roster.append(temp_roster[['team_id', 'playerId']])
    
        temp_dict = {}
        for key in team:
            if isinstance(team[key], (str, int, float)):
                temp_dict[key] = team[key]
            temp_dict['owner_id'] = team.get('owners')[0]
        teams = teams.append(pd.Series(temp_dict), ignore_index = True)
        
    
    teams.rename(columns = {'id':'team_id'}, inplace = True)
    teams['team_id'] = teams['team_id'].astype(int).astype(str)
    teams = teams[['team_id', 'abbrev', 'location', 'nickname', 'owner_id']].astype(str)
    teams['team_name'] = teams['location'] + ' ' + teams['nickname']
    
    return teams, roster.astype(str)

def get_league_members(data):
    members = pd.DataFrame()
    
    for member in data['members']:    
        member.pop('notificationSettings')
        members = members.append(pd.Series(member), ignore_index = True)
    
    members['owner_name'] = members['firstName'] + ' ' + members['lastName']
    members.rename(columns= {'id': 'owner_id', 'displayName': 'display_name'}, inplace = True)
    
    return members