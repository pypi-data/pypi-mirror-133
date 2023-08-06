# fantasy football stats (ff-stats)

Pull fantasy football projections and determine your optimal lineup.


## Installation

```
pip install ff_stats
```

## Usage
```python
>>> import ff_stats
>>> fm = ff_stats.FantasyManager(Season = '2021', weeks = ['9', 'Rest of Season'])
```

### Get projections
```python
>>> fm.get_projections()
```

### Get espn league information
```python
>>> cookies = {'swid': '{1234A567-89CD-0E1F-G2HI-3456JKLM7O7P}'}
>>> cookies['espn_s2'] = 'ADkneoiSNFIljOIJPOIJ'
>>> fm.get_league_info(espn_league_id = '123456', cookies)
```
###





