# # wot-players-start
This is a repository for quickly collecting account statistics for World of tanks accounts.
Script collects: Bob's medal..., wins,losses,draws, total damage, and average xp for each account.
Script is used [Wargaming public API](https://developers.wargaming.net/reference/) for parsing credentials.
## files
- get_BB_medal.py it is the main script for parsing data and uploading it to [clickhouse DB](http://yandex.ru/dev/clickhouse/)
- Statistics.ipynb-laptop with 3-parameter distributions:
  win rate,avg_damage,avg_xp. It has a distribution of 4 groups of players in the "Team Clash" competition for the RU cluster.
