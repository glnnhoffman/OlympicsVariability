import pandas as pd
import numpy as np

# medals
df = pd.read_csv('olympic_medals.csv')
# hosts
hosts = pd.read_csv('olympic_hosts.csv')
# total results
results = pd.read_csv('olympic_results.csv')


# filter to summer and select game_slug column
summer = hosts[hosts['game_season'] == 'Summer']

# games of interest
games = summer['game_slug']

# filter to games of interest
df = df[df['slug_game'].isin(games)]
results = results[results['slug_game'].isin(games)]

# confirm number of games is the same in both dataframes
g_medal = df['slug_game'].nunique()
g_total = results['slug_game'].nunique()

if g_medal == g_total:
    print('Number of games is the same in both dataframes')


# assign count to new column
results['country_event'] = results.groupby('event_title')['country_name'].transform('nunique')
results['country_discipline'] = results.groupby('discipline_title')['country_name'].transform('nunique')

# concat discipline_title and event title columns
#df['Event'] = df['discipline_title'] + ' ' + df['event_title']


df['cntryMedal_event'] = df.groupby('event_title')['country_name'].transform('nunique')
df['cntryMedal_discipline'] = df.groupby('discipline_title')['country_name'].transform('nunique')

# Sort countries in descending order

disc_total = results[['discipline_title', 'country_discipline']].drop_duplicates().sort_values(by='discipline_title', ascending=False)
disc_medal = df[['cntryMedal_discipline', 'discipline_title']].drop_duplicates().sort_values(by='discipline_title', ascending=False)

# join the total_disc and medal_disc dataframes by discipline_title
country_counts = pd.merge(disc_total, disc_medal, on='discipline_title', how='left')

print(country_counts.head())
print(country_counts.columns)
# rename columns

country_counts['percent'] = country_counts['cntryMedal_discipline'] / country_counts['country_discipline']

# filter to wheere coutnry_discipline is greater than 15
country_counts = country_counts[country_counts['country_discipline'] > 15]

# print sorted by percent
print(country_counts.sort_values(by='percent', ascending=False).head(40))

# Looks like Rugby is a good option, or maybe canoe marathon or sprint