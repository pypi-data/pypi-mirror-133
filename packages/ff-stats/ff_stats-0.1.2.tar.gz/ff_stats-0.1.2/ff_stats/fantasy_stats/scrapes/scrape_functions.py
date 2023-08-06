import requests
import pandas as pd
import time
import random
import numpy as np
import json


from .source_references import source_columns, team_ids, source_position_ids, source_urls
from .corrections import sum_and_drop_cols, add_dst_teams, team_fix, ad_hoc_fixes

def pull_data(sources, positions, weeks, current_week, season, txt = None):
    pulls = []
    for source in sources:
        try:
            pulls.append(eval(source + '_pull')(positions, weeks, season, current_week))
        except:
            print('Unable to retrieve {} projections.'.format(source))
            continue
    
    pull_df = pd.concat(pulls).drop_duplicates()
    pull_df.reset_index(inplace = True, drop = True)
    
    pull_df = ad_hoc_fixes(pull_df)
    
    
    cat_cols = [col for col in source_columns['all']['categorical'] if col in  pull_df.columns]
    num_cols = [col for col in source_columns['all']['numeric'] if col in  pull_df.columns]
    
    out_df = pull_df[cat_cols + num_cols].fillna('')
    
    return out_df
    
    
    

def gen_url(position, season, week, source):
    # Get base url
    base_url = source_urls[source]
    
    if source == 'cbs':
        url = base_url.format(position.upper(), season, week.lower().replace(' ', ''))
        
    if source == 'nfl':
        url = base_url.format(season, source_position_ids['nfl'][position], week)
    
    if source == 'number_fire':
        url = base_url['Rest of Season' if week == 'Rest of Season' else 'current week'].format(position if position != 'dst' else 'd')
            
    if source == 'fantasy_sharks':
        segment = '717' if week == 'Rest of Season' else str(int(week)+ 722)
        url = base_url.format(source_position_ids['fantasy_sharks'][position], segment)
    
    if source == 'fleaflicker':
        url = base_url.format(source_position_ids['fleaflicker'][position])
    
    if source == 'FFToday':
        url = base_url.format(season, week, source_position_ids['FFToday'][position])
        
    if source == 'FantasyPros':
        url = base_url.format(position)
  
    return url


def pull_html(position, season, week, source):
    headers = {'User-Agent': 'Chrome/79.0.3945.88'}
    url = gen_url(position, season, week, source)
    
    r = requests.get(url, headers = headers)
    text = r.text
    
    if source == 'fleaflicker':
        pages = max(pd.Series(text).str.extract('Previous</a>(.+)>Next')[0].str.extractall('>([0-9]+)</a>')[0].astype(int))
        text = r.text
        for offset in np.arange(1, pages):
            text += requests.get(url + '&tableOffset=' + str(offset*20), headers = headers).text
            time.sleep(random.uniform(.5, 1.5))
    else:
        time.sleep(random.uniform(.5, 1.5))

    return text

def espn_api(season, weeks):
    
    external_ids = [int(season) if week == 'Rest of Season' else int(season + week) for week in weeks]

    filters = {'players': {'limit': 2000,
    'filterStatsForSourceIds': {'value': [1]},
    'filterStatsForExternalIds':{'value': external_ids},
    'sortDraftRanks': {
    'sortPriority': 1,
    'sortAsc': True,
    'value': 'STANDARD'}}}

    headers = {'x-fantasy-filter': json.dumps(filters)}
    
    r = requests.get('https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leaguedefaults/1'.format(season),
                     params={ 'view': 'kona_player_info'},
                     headers = headers)
    return r.json()


def ESPN_pull(positions, weeks, season, current_week, expand_defensive_stats = True):
    """
    all past weeks, rest of season
    """
    
    data = espn_api(season, weeks)
    
    player_df = pd.DataFrame()
    for player in data['players']:
        player = player['player']
        
        info = {'player': player['fullName'], 'player_id': str(player['id']),
                     'pos': source_position_ids['espn'][player['defaultPositionId']],
                     'team':team_ids['espn'][player['proTeamId']]}
        
        info_dict = {week: info.copy() for week in weeks}
        
        for stat in player.get('stats') or []:
            period, split, avgPts, totPts = list(map(stat.get,['scoringPeriodId', 'statSplitTypeId', 'appliedAverage', 'appliedTotal']))
            
            if (period == 0)&(split != 2): continue
             
            statWeek = str(period) if period != 0 else 'Rest of Season'
            info_dict[statWeek]['gp'] = 0 if totPts == 0 else round(totPts/avgPts) if bool(avgPts) else 1
            info_dict[statWeek].update(stat['stats'])
      
        player_df = player_df.append(pd.DataFrame(info_dict).transpose().reset_index().rename(columns = {'index': 'week'}))
    
    player_df = player_df.loc[player_df.pos.str.lower().isin(positions)]
    
    cat_cols = ['player_id', 'player', 'team', 'pos', 'week', 'gp']
    
    out_df = player_df[cat_cols + list(player_df.columns.intersection(source_columns['espn']))].copy()
    out_df.rename(columns = source_columns['espn'], inplace = True)
    
    colsDtd = ['punt_return_td', 'kick_return_td', 'def_int_td', 'def_fumble_td', 'def_blocked_kick_td']
    
    
    
    out_df = sum_and_drop_cols(out_df, {'def_td': colsDtd,
                                        'ret_td': ['punt_return_td', 'kick_return_td'],
                                        '2pt': ['2pt_rush', '2pt_rec', '2pt_pass']})

    
    out_df.loc[out_df.pos != 'DST', 'def_td'] = 0
    out_df.loc[out_df.pos == 'DST', 'ret_td'] = 0
    
    if expand_defensive_stats == False:
        defAllowedStats = list(out_df.columns[out_df.columns.str.contains('allowed', regex = True)])
        out_df.drop([x for x in defAllowedStats if x not in ['def_pt_allowed', 'def_yd_allowed']],
                    axis = 1, inplace = True)
    
    out_df['source'] = 'ESPN'
    
    out_df = add_dst_teams(out_df)
    
    return out_df


def NFL_pull(positions, weeks, season, current_week):
    """
    All weeks
    """
    out_df = pd.DataFrame()
    
    # Include additional weeks if rest of season
    if 'Rest of Season' in weeks:
        ros_weeks = [str(x) for x in np.arange(int(current_week), 19, 1)]
        nfl_weeks = [str(x) for x in np.arange(0, 19, 1) if str(x) in ros_weeks + weeks]
    else:
        ros_weeks = []
        nfl_weeks = weeks
        
    # group 'qb', 'rb', 'wr', 'te' into off to reduce requests
    if any([pos in positions for pos in ['qb', 'rb', 'wr', 'te']]):
        nfl_pos = ['off'] + [pos for pos in ['k', 'dst'] if pos in positions]
    else:
        nfl_pos = positions
   
    for pos in nfl_pos:        
        for week in nfl_weeks:
           
            pull_df = pd.read_html(pull_html(pos, season, week, 'nfl'))[0]
            
            temp_cols = pd.Series(['_'.join(col) for col in pull_df.columns])
            pull_df.columns = temp_cols.str.replace('^Unnamed.+_', '', regex = True)
            
            if pos == 'dst':
                pull_df['player'] = pull_df.Team.str.replace('( DEF.+$)|( DEF$)', '', regex = True)
                pull_df['pos'] = 'DST'
                pull_df['team'] = ''
                pull_df.rename(columns = {'Ret_TD': 'def_ret_td'}, inplace = True)
                
                
            else:
                pull_df[['player', 'team']] = pull_df.Player.str.split(' - ', expand = True)
                pull_df['team'] = pull_df['team'].str.replace(' .+', '', regex = True)
                pull_df.loc[~pull_df.Player.str.contains(' - ', regex = True), 'team'] = 'FA'
                
                    
                match_string_pos = '( {} )|( {}$)'.format('QB', 'QB')
                match_string_name = '( {}$)|( {} .+)'.format('QB', 'QB')
                for p in ['RB', 'WR', 'TE', 'K']:
                    match_string_pos += '|( {} )|( {}$)'.format(p, p)
                    match_string_name += '|( {}$)|( {} .+)'.format(p, p)
                pull_df['pos'] = pull_df.player.str.extract(match_string_pos).fillna('').sum(axis = 1).str.strip()
                pull_df['player'] = pull_df.player.str.replace(match_string_name, '', regex = True)
           
                
                pull_df.drop('Player', axis = 1, inplace = True)
                
                
            pull_df['week'] = week
            pull_df['gp'] = 1
            pull_df.loc[(pull_df.Fantasy_Points.isin(['-', '0.00']))|(pull_df.Opp == 'Bye'), 'gp'] = 0
            
            # pull_df = pull_df.replace('-', '0') 
            pull_df = pull_df.replace('-', '')
            
            out_df = out_df.append(pull_df[pull_df.columns.intersection(source_columns['nfl'].keys())])
        
    # Convert to correct data types
    str_cols = ['player', 'team', 'pos', 'week']
    num_cols = [col for col in out_df.columns if col not in str_cols]
    out_df[str_cols] = out_df[str_cols].astype('str')
    out_df[num_cols] = out_df[num_cols].apply(pd.to_numeric)
    
    # Group week outputs
    if ros_weeks:
        ros = out_df[out_df.week.isin(ros_weeks)].drop('week', axis  =1).groupby(['player', 'team', 'pos'], as_index = False).sum()
        ros['week'] = 'Rest of Season'
    
    # Add rest of season back in
    out_df = out_df.append(ros)
    
    # Remove extra positions/weeks
    out_df = out_df.loc[(out_df.week.isin(weeks))&(out_df.pos.str.lower().isin(positions))]
    
    fg_u40 = ['FG Made_0-19','FG Made_20-29','FG Made_30-39']
    def_saf, def_td = ['Score_Saf', 'Score_Def 2pt Ret'], ['Score_TD', 'def_ret_td']
    
    
    out_df = sum_and_drop_cols(out_df, {'fg_0to39': fg_u40, 'def_safety': def_saf, 'def_td': def_td})
    
    out_df.rename(columns = source_columns['nfl'], inplace = True)
    
    out_df['source'] = 'NFL'
    
    out_df = add_dst_teams(out_df, 'full_name')
    out_df = team_fix(out_df)
    
    return out_df#.fillna(0)


def CBS_pull(positions, weeks, season, current_week):
    """
    Current week, next week, rest of season
    """
    player_df = pd.DataFrame(columns = source_columns['cbs'].keys())
    
    for pos in positions:
        for week in weeks:
            pull_df = pd.read_html(pull_html(pos, season, week, 'cbs'))[0]
            
            temp_cols = pd.Series(['_'.join([col[0], col[1].split(' ')[0]]) for col in pull_df.columns])
            
            pull_df.columns = temp_cols.str.replace('^Unnamed.+_', '', regex = True)
            
            if pos == 'dst':
                pull_df['player'] = pull_df['Team']
                pull_df['pos'] = 'DST'
                pull_df['gp'] = round(pull_df['Yards Allowed_total']/pull_df['Yards Allowed_avg'])
                
                
            else:
                pull_df[['player', 'pos', 'team']] = pull_df.Player.str.split('  ', expand = True).iloc[:,[-3, -2, -1]]
            
            pull_df[['week']] = week
            
            # pull_df.drop('Player', axis = 1, inplace = True)
    
            common_cols = pull_df.columns.intersection(player_df.columns)        
            player_df = player_df.append(pull_df[common_cols])
    
    # Replace FB with RB
    player_df.loc[player_df.pos == 'FB', 'pos'] = 'RB'
    
    player_df.rename(columns = source_columns['cbs'], inplace = True)
    
    player_df['source'] = 'CBS'
    
    # Calculate kicker columns
    fg_under40 = ['fg_1to19', 'fg_20to29', 'fg_30to39']
    fga = ['fg_1to19a', 'fg_20to29a', 'fg_30to39a', 'fg_40to49a', 'fg_50plusa']
    player_df = sum_and_drop_cols(player_df, {'fg_0to39': fg_under40, 'fga': fga})
    player_df = sum_and_drop_cols(player_df, {'fgm': ['fg_0to39', 'fg_40to49', 'fg_50plus']} ,drop = False)
    player_df['fg_miss'] = player_df['fga'] - player_df['fgm']
    player_df['xp_miss'] = player_df['xpa'] - player_df['xp_made']
    player_df.drop(['xpa', 'fga', 'fgm'], axis = 1, inplace = True)
    
    
    
    char_cols = ['player', 'team', 'pos', 'week', 'source']
    num_cols = [col for col in player_df.columns if col not in char_cols]
    
    out_df = pd.concat([player_df[char_cols], player_df[num_cols].apply(pd.to_numeric)], axis = 1)#.fillna(0)
    
    out_df = add_dst_teams(out_df, 'city')
    out_df = team_fix(out_df)
    
    return out_df


def number_fire_pull(positions, weeks, season, current_week):
    out_df = pd.DataFrame()
    """
    Current week, rest of season
    """
    # Correct for any non-current weeks
    weeks = [week for week in weeks if week in ['Rest of Season', current_week]]
    
    for pos in positions:
        for week in weeks:                
            
            # Get data
            pull_df = pd.read_html(pull_html(pos, season, week, 'number_fire'))
          
            
            names = pd.DataFrame(pull_df[0].columns).append(pull_df[0].rename(columns = {pull_df[0].columns[0] : 0})).rename(columns = {0:'player'})
            
            names[['pos', 'team']] = names.player.str.extract('\((.+)\)')[0].str.split('\, ', expand = True)
            
            if pos == 'dst': names['pos'] = 'DST'
                
            
            names.player = names.player.str.replace('  [A-Z]\..+', '', regex = True)
            names['week'] = week
            
            pull_df[1].columns = [' '.join(col) for col in pull_df[1].columns]
            
            pull_df[1] = pull_df[1][pull_df[1].columns.intersection(source_columns['number_fire'].keys())]
            
            out_df = out_df.append(names.join(pull_df[1]))#.fillna(0)

    out_df.rename(columns = source_columns['number_fire'], inplace = True)
     
    out_df = sum_and_drop_cols(out_df, {'fg_0to39': ['fg_0to19', 'fg_20to29', 'fg_30to39']})
    
    out_df['fg_miss'] = out_df.fga - out_df.fgm 
    
    out_df.drop(['fga', 'fgm'], axis = 1, inplace = True)
    
    out_df = team_fix(out_df)
    
    out_df = add_dst_teams(out_df)
    
    out_df['source'] = 'number_fire'
    
    return out_df
     
def fantasy_sharks_pull(positions, weeks, season, current_week):
    """
    Works for any week, info will need to change for next year
    """
    
    out_df = pd.DataFrame()
    for week in weeks:
        for pos in positions:
            pull_df = pd.read_html(pull_html(pos, season, week, 'fantasy_sharks').replace('<sup>R</sup>', ''), attrs = {'id': 'toolData'})[0]
        
            pull_df = pull_df[pull_df.Player.str.contains('\,')]
            
            pull_df['Player'] = pull_df.Player.apply(lambda x: ' '.join(x.split(', ')[::-1]))
            
            pull_df[['pos', 'week']] = pos.upper(), week
            
            cols = source_columns['fantasy_sharks']['dst' if pos == 'dst' else 'default']
            
            pull_df.rename(columns = cols, inplace = True)
            
            
            out_df = out_df.append(pull_df[pull_df.columns.intersection(cols.values())])
    
    
    num_cols = [col for col in out_df.columns if col not in ['player', 'team', 'pos', 'week']]
    
    out_df[num_cols] = out_df[num_cols].apply(pd.to_numeric)
        
    out_df['xp_miss'] = out_df.xpa - out_df.xp_made
    out_df.drop('xpa', axis = 1, inplace = True)
    
    out_df = sum_and_drop_cols(out_df, {'fg_0to39': ['fg_10to19', 'fg_20to29', 'fg_30to39']})
    
    out_df = team_fix(out_df)
    out_df = add_dst_teams(out_df)
    out_df['source'] = 'fantasy_sharks'
    
    return out_df
    
def fleaflicker_pull(positions, weeks, season, current_week):
    """
    Only works for current week
    """
    
    out_df = pd.DataFrame()
    
    for week in [week for week in weeks if week != 'Rest of Season']:    
        for pos in positions:
            
            r = pull_html(pos, season, week, 'fleaflicker') 
            
            ##### Week test
            source_week = pd.Series(r).str.extract('<em>projected</em> stats for <em>Week ([0-9]+)</em>').values[0,0]
            
            pull_df = pd.concat(pd.read_html(pd.Series(r).str.replace('(\<span class="injury text.+?\</span>)', '', regex = True).values[0]))
            
            pull_df.columns = pd.Series([' '.join(col) for col in pull_df.columns]).str.replace('Projected ', '', regex = True).str.replace('Week [0-9]+ ', '', regex = True)  
            pull_df = pull_df[~pull_df.Opp.str.contains('Previous[0-9]+Next')]
            
            pull_df[['pos', 'team']] = pull_df['Player Name'].str.extract(' ([A-Z\/]+ [A-Z]+) \(')[0].str.split(' ', expand = True) 
        
            if pos == 'dst': pull_df.pos = 'DST'
            
            pull_df['Player Name'] = pull_df['Player Name'].str.replace(' [A-Z\/]+ [A-Z]+ \([0-9]+\)$', '', regex = True)
            pull_df['week'] = source_week
        
            out_df = out_df.append(pull_df[pull_df.columns.intersection(source_columns['fleaflicker'].keys())])
    
    out_df.rename(columns = source_columns['fleaflicker'], inplace = True)
    
    out_df.loc[out_df.pos == 'RB/WR', 'pos'] = 'RB'
    
    out_df['source'] = 'fleaflicker'
    
    num_cols = [col for col in out_df.columns if col not in ['player', 'team', 'pos', 'week', 'source']]
    out_df[num_cols] = out_df[num_cols].apply(pd.to_numeric)
    
    out_df = team_fix(out_df)
        
    
    out_df = add_dst_teams(out_df)
    
    
    
    out_df['fg_miss'] = out_df['fga'] - out_df['fg_40to49']
    out_df.drop('fga', axis = 1, inplace = True)
    
    return out_df
    

def FFToday_pull(positions, weeks, season, current_week):
    """
    Past weeks, current week
    """
    weeks = [week for week in weeks if week != 'Rest of Season']
    
    out_of_bounds = [week for week in weeks if int(week) > int(current_week)]
    if out_of_bounds:
        print('FFToday does not have projections for future weeks.')
        for week in out_of_bounds:
            weeks.remove(week)

    
    positions = [pos for pos in positions if pos != 'dst']
    
    
    out_df = pd.DataFrame()
    
    for week in [week for week in weeks if week != 'Rest of Season']:
        unavail_flag = 0
        for pos in [pos for pos in positions if pos != 'dst']:
            if unavail_flag == 1: continue
        
            r = pull_html(pos, season, week, 'FFToday') 
            
            if 'No Player Found!' in r:
                print('FFToday projections for Week {} are not available.'.format(week))
                unavail_flag = 1
                continue 
                
            
            source_week = pd.Series(r).str.extract("name='GameWeek' value='([0-9]+)'>").values[0,0]
    
    
            r_red = pd.Series(r).str.replace("\n", ' ').str.extract("(<TABLE WIDTH.+?</table>)")
    
    
            pull_df =pd.read_html(r_red.values[0,0])[0].fillna('').T.set_index([0,1],append = False).T    
            pull_df.columns = [' '.join(col).strip() for col in pull_df.columns]
            
            pull_df[['week', 'pos']] = source_week, pos.upper()
            pull_df.columns = pull_df.columns.str.replace("^Player.+", 'player', regex = True)  
    
            out_df = out_df.append(pull_df[pull_df.columns.intersection(source_columns['FFToday'].keys())])
       
    if out_df.empty: return out_df
    
    out_df.rename(columns = source_columns['FFToday'], inplace = True)
    num_cols = [col for col in out_df.columns if col not in ['player', 'team', 'pos', 'week']]
    out_df[num_cols] = out_df[num_cols].apply(pd.to_numeric)#.fillna(0)
    out_df = team_fix(out_df)
    out_df['source'] = 'FFToday'    
    
    return out_df


def FantasyPros_pull(positions, weeks, season, current_week):
    """
    current week
    """
   
    if current_week in weeks:
        week = current_week
    else:
        raise Exception('FantasyPros only contains current week data')
    
    
    output_df = pd.DataFrame()
    for pos in positions:
        r = pull_html(pos, season, week, 'FantasyPros')
        
        source_week = pd.Series(r).str.extractall('<title>Week ([0-9]+) ').values[0,0]
        
        pull_df = pd.read_html(r, attrs = {'id': 'data'})[0]
        
        if pos not in ['k', 'dst']:
            pull_df.columns =  [' '.join(col) for col in pull_df.columns]
        
        pull_df.rename(columns = {pull_df.columns[0]:'Player'}, inplace = True)
        
        if pos != 'dst':
            pull_df['team'] = pull_df.Player.str.extract(' ([A-Z]+$)')
            pull_df.Player = pull_df.Player.str.replace(' [A-Z]+$', '', regex = True)
        
        pull_df[['week', 'pos']] = source_week, pos.upper()
        output_df = output_df.append(pull_df[pull_df.columns.intersection(source_columns['FantasyPros'].keys())])
    
    output_df.rename(columns = source_columns['FantasyPros'], inplace = True)
    num_cols = [col for col in output_df.columns if col not in ['player', 'team', 'week', 'pos']]
    output_df[num_cols] = output_df[num_cols].apply(pd.to_numeric)
    
    output_df['source'] = 'FantasyPros'
    
    output_df = add_dst_teams(output_df, dict_key = 'full_name')
    output_df = team_fix(output_df)
    
    output_df['fg_miss'] = output_df['fg_40to49'] - output_df['fga']
    output_df.drop('fga', axis = 1, inplace = True)

    return output_df

