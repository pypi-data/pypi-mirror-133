columns = {
    'categorical': ['player_id', 'player', 'team', 'pos', 'week', 'bye_week', 'opp', 'source', 'source_count', 'f_team_name', 'f_team_id'],
    'numeric': ['gp', 'total_pts', 'avg_pts', 'pass_yd', 'pass_td', 'int', 'rush_yd', 'rush_td', 'rec', 'rec_yd', 'rec_td', 'fum', '2pt', 'ret_td', 
                'fg_0to39', 'fg_40to49', 'fg_50plus', 'fg_miss', 'xp_made', 'xp_miss',
                'def_sack', 'def_int', 'def_fum', 'def_td', 'def_safety', 'def_pt_allowed', 'def_yd_allowed',
                '0_pt_allowed', '1to6_pt_allowed', '7to13_pt_allowed', '14to17_pt_allowed', '18to21_pt_allowed', '22to27_pt_allowed', 
                '28to34_pt_allowed', '35to45_pt_allowed', '46plus_pt_allowed',
                'less_than_100_yd_allowed', '100to199_yd_allowed', '200to299_yd_allowed', '300to349_yd_allowed', '350to399_yd_allowed',
                '400to449_yd_allowed', '450to499_yd_allowed', '500to549_yd_allowed', '550plus_yd_allowed']}

league_settings = {
    'scoring_settings': {
        'pass_yd': .04,
        'pass_td': 4,
        'int': -2,
        'rush_yd': .1,
        'rush_td': 6,
        'rec': .5,
        'rec_yd': .1,
        'rec_td': 6,
        'fum': -2,
        '2pt': 2,
        'ret_td': 6,
        'fg_0to39': 3,
        'fg_40to49': 4,
        'fg_50plus': 5,
        'fg_miss': -1,
        'xp_made': 1,
        'xp_miss': 0,
        'def_sack': 1,
        'def_int': 2,
        'def_fum': 2,
        'def_td': 6,
        'def_safety': 2,
        '0_pt_allowed': 5,
        '1to6_pt_allowed': 4,
        '7to13_pt_allowed': 3,
        '14to17_pt_allowed': 1,
        '18to21_pt_allowed': 0,
        '22to27_pt_allowed': 0,
        '28to34_pt_allowed': -1,
        '35to45_pt_allowed': -3,
        '46plus_pt_allowed': -5,
        'less_than_100_yd_allowed': 5,
        '100to199_yd_allowed': 3,
        '200to299_yd_allowed': 2,
        '300to349_yd_allowed': 0,
        '350to399_yd_allowed': -1,
        '400to449_yd_allowed': -3,
        '450to499_yd_allowed': -5,
        '500to549_yd_allowed': -6,
        '550plus_yd_allowed': -7},
    'lineup_slots':{
        'QB': 1,
        'RB': 2,
        'WR': 2,
        'TE': 1,
        'Flex': 1,
        'DST': 1,
        'K': 1},
    'flex_positions': ['RB', 'WR', 'TE']}


valid_sources = ['CBS', 'NFL','ESPN', 'number_fire', 'fantasy_sharks', 'fleaflicker', 'FFToday', 'FantasyPros']

valid_positions = ['qb', 'rb', 'wr', 'te', 'dst', 'k']

valid_weeks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', 'Rest of Season']










