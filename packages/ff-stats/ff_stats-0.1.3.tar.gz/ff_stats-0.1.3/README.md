# fantasy football stats (ff-stats)

Pull fantasy football projections and determine your optimal lineup.


## Installation

```
pip install ff_stats
```

## Usage
```python
>>> import ff_stats
# Initialize with season and week(s) of interest
>>> fm = ff_stats.FantasyManager(Season = '2021', weeks = ['9', 'Rest of Season'])

# Scrape projections
>>> fm.get_projections()

# Get espn league information (See notes below)
>>> cookies = {'swid': '{1234A567-89CD-0E1F-G2HI-3456JKLM7O7P}'}
>>> cookies['espn_s2'] = 'ADkneoiSNFIljOIJPOIJ'
>>> fm.get_league_info(espn_league_id = '123456', cookies)
>>> print(fm.teams)
  team_id abbrev                 team_name   display_name       owner_name
0       1   DRE       The Double Entandres         nowdre    Andre Nowzick
1       2   PIS           Password is Taco      tacomacka   Taco MacArthur


# Set your team id
>>> fm.set_team_id('5')


# Add fantasy team names to each player
>>> fm.add_f_teams()

# Score Projections
>>> fm.score_projections()

# Combine Sources
fm.combine_sources()

# Get optimal lineup
>>> fm.get_best_lineup(scoring_period = '9', include_fa = True, depth = 2)
```


## Notes
* For private ESPN leagues the swid and espn_s2 cookies must be provided. They can be found in your browser settings.

* Scoring settings can be altered by accessing scoring settings
```python
>>> score_set = fm.scoring_settings
>>> print(score_set)
{'pass_yd': 0.04,
 'pass_td': 4,
 'int': -2,
...
```

