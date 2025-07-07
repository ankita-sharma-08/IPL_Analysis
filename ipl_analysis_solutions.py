import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)



# Load the datasets from local paths
matches_df = pd.read_csv('/content/IPL Matches 2008-2020.csv')
balls_df = pd.read_csv('/content/IPL Ball-by-Ball 2008-2020.csv')

# Optional: convert date to datetime and extract season
matches_df['date'] = pd.to_datetime(matches_df['date'])
matches_df['season'] = matches_df['date'].dt.year




# Q1: Count of matches played in each season
matches_per_season = matches_df['season'].value_counts().sort_index()

# Visualization 1: Matches played per season
matches_per_season = matches_df['season'].value_counts().sort_index()
plt.figure()
sns.barplot(x=matches_per_season.index, y=matches_per_season.values, palette="viridis")
plt.title("Matches Played per Season")
plt.xlabel("Season")
plt.ylabel("Number of Matches")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()










# Q2: Total runs scored in each season
# Merge matches_df with balls_df on 'id'
merged_df = balls_df.merge(matches_df[['id', 'season']], on='id')
runs_per_season = merged_df.groupby('season')['total_runs'].sum()

# Visualization 2: Total Runs scored in each season (available only for 2008 in data)
merged_df = balls_df.merge(matches_df[['id', 'season']], on='id')
runs_per_season = merged_df.groupby('season')['total_runs'].sum()
plt.figure()
sns.barplot(x=runs_per_season.index, y=runs_per_season.values, palette="magma")
plt.title("Total Runs Scored per Season")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()










# Q3: Runs scored per match in different seasons
runs_per_match_season = runs_per_season / matches_per_season




# Q4: Umpire who has officiated the most
umpires = pd.concat([matches_df['umpire1'], matches_df['umpire2']])
most_common_umpire = umpires.value_counts().idxmax()




# Q5: Team that won the most tosses
most_tosses_won = matches_df['toss_winner'].value_counts().idxmax()




# Q6: Toss decisions after winning toss
toss_decision_count = matches_df.groupby('toss_decision')['id'].count()




# Q7: Toss decision variation across seasons
toss_decision_by_season = matches_df.groupby(['season', 'toss_decision'])['id'].count().unstack().fillna(0)

# Visualization 3: Toss Decision Trends Across Seasons
toss_decision_by_season = matches_df.groupby(['season', 'toss_decision'])['id'].count().unstack().fillna(0)
toss_decision_by_season.plot(kind='bar', stacked=True, colormap='Set2')
plt.title("Toss Decisions per Season")
plt.xlabel("Season")
plt.ylabel("Number of Matches")
plt.legend(title="Toss Decision")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()










# Q8: Correlation between toss win and match win
matches_df['toss_win_match_win'] = matches_df['toss_winner'] == matches_df['winner']
toss_win_match_win_rate = matches_df['toss_win_match_win'].mean()

# Visualization: Toss win vs Match win (Q8)
matches_df['toss_win_match_win'] = matches_df['toss_winner'] == matches_df['winner']
toss_outcome_counts = matches_df['toss_win_match_win'].value_counts()
toss_outcome_counts.index = ['Did Not Win Match', 'Won Match']
plt.figure()
toss_outcome_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#FF9999', '#99FF99'])
plt.title("Toss Win Resulting in Match Win")
plt.ylabel("")
plt.tight_layout()
plt.show()



# Q9: Count of wins by chasing team (team that batted second)
# We'll consider innings and match winners
last_innings = balls_df.groupby('id')['inning'].max().reset_index()
chasing_winners = matches_df[matches_df['id'].isin(last_innings[last_innings['inning'] == 2]['id'])]
chasing_win_count = chasing_winners[chasing_winners['winner'].notnull()].shape[0]

(
    matches_per_season, 
    runs_per_season, 
    runs_per_match_season,
    most_common_umpire,
    most_tosses_won,
    toss_decision_count,
    toss_decision_by_season,
    toss_win_match_win_rate,
    chasing_win_count
)





# Q10: Teams that have won the tournament (final match winners of each season)
final_matches = matches_df.sort_values('date').drop_duplicates('season', keep='last')
tournament_winners = final_matches[['season', 'winner']].dropna()




# Q11: Team that has played the most number of matches
matches_played = pd.concat([matches_df['team1'], matches_df['team2']])
most_matches_played = matches_played.value_counts().idxmax()




# Q12: Team that has won the most number of matches
most_wins = matches_df['winner'].value_counts().idxmax()





# Q13: Team with the highest winning percentage (min 50 matches played)
total_matches_team = matches_played.value_counts()
wins_team = matches_df['winner'].value_counts()
win_percentage = (wins_team / total_matches_team) * 100
win_percentage = win_percentage[total_matches_team >= 50].sort_values(ascending=False)





# Q14: Lucky venue for each team (venue where team has max wins)
lucky_venues = matches_df.groupby(['winner', 'venue']).size().reset_index(name='win_count')
lucky_venues = lucky_venues.sort_values(['winner', 'win_count'], ascending=[True, False])
lucky_venue_per_team = lucky_venues.groupby('winner').first().reset_index()





# Q15: Innings-wise comparison (total runs scored by each team in each innings)
innings_comparison = balls_df.groupby(['batting_team', 'inning'])['total_runs'].sum().unstack().fillna(0)





# Q16: Team with most 200+ scores
team_total_runs = balls_df.groupby(['id', 'batting_team'])['total_runs'].sum().reset_index()
team_200plus_scores = team_total_runs[team_total_runs['total_runs'] >= 200]
most_200plus_scores = team_200plus_scores['batting_team'].value_counts()




# Q17: Team that has conceded 200+ scores the most
team_200plus_against = balls_df.groupby(['id', 'bowling_team'])['total_runs'].sum().reset_index()
team_200plus_against = team_200plus_against[team_200plus_against['total_runs'] >= 200]
most_conceded_200plus = team_200plus_against['bowling_team'].value_counts()





# Q18: Highest team total in a single match
highest_team_score = team_total_runs.sort_values('total_runs', ascending=False).head(1)




# Q19: Biggest win by run margin
biggest_run_margin_win = matches_df[matches_df['result'] == 'runs'].sort_values('result_margin', ascending=False).head(1)




# Q20: Batsmen who have played the most balls
balls_played = balls_df[balls_df['extra_runs'] == 0].groupby('batsman').size().sort_values(ascending=False)

(
    tournament_winners,
    most_matches_played,
    most_wins,
    win_percentage.head(5),
    lucky_venue_per_team.head(5),
    innings_comparison,
    most_200plus_scores.head(5),
    most_conceded_200plus.head(5),
    highest_team_score,
    biggest_run_margin_win[['winner', 'result_margin', 'venue']],
    balls_played.head(5)
)







# Q21: Leading run-scorers of all time
run_scorers = balls_df.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False)

# Visualization 4: Top 5 Batsmen by Total Runs
run_scorers = balls_df.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False)
top_5_batsmen = run_scorers.head(5)
plt.figure()
sns.barplot(x=top_5_batsmen.values, y=top_5_batsmen.index, palette="coolwarm")
plt.title("Top 5 Run Scorers")
plt.xlabel("Total Runs")
plt.ylabel("Batsman")
plt.tight_layout()
plt.show()





# Q22: Most number of 4s
fours = balls_df[(balls_df['batsman_runs'] == 4)]
most_fours = fours['batsman'].value_counts()

# Visualization: Most 4s by Batsmen (Q22)
fours = balls_df[balls_df['batsman_runs'] == 4]
fours_by_batsman = fours['batsman'].value_counts().head(5)
plt.figure()
sns.barplot(x=fours_by_batsman.values, y=fours_by_batsman.index, palette='Blues_r')
plt.title("Top 5 Batsmen with Most Fours")
plt.xlabel("Number of Fours")
plt.ylabel("Batsman")
plt.tight_layout()
plt.show()











# Q23: Most number of 6s
sixes = balls_df[(balls_df['batsman_runs'] == 6)]
most_sixes = sixes['batsman'].value_counts()

# Visualization: Most 6s by Batsmen (Q23)
sixes = balls_df[balls_df['batsman_runs'] == 6]
sixes_by_batsman = sixes['batsman'].value_counts().head(5)
plt.figure()
sns.barplot(x=sixes_by_batsman.values, y=sixes_by_batsman.index, palette='Reds_r')
plt.title("Top 5 Batsmen with Most Sixes")
plt.xlabel("Number of Sixes")
plt.ylabel("Batsman")
plt.tight_layout()
plt.show()









# Q24: Highest strike rate (min 100 balls faced)
balls_faced = balls_df.groupby('batsman').size()
total_runs = balls_df.groupby('batsman')['batsman_runs'].sum()
strike_rate = (total_runs / balls_faced) * 100
strike_rate = strike_rate[balls_faced >= 100].sort_values(ascending=False)




# Q25: Leading wicket-taker
wickets_df = balls_df[balls_df['is_wicket'] == 1]
wickets_df = wickets_df[wickets_df['dismissal_kind'] != 'run out']  # exclude run outs
leading_wicket_taker = wickets_df['bowler'].value_counts()

# Visualization: Leading Wicket-Takers (Q25)
wickets_df = balls_df[(balls_df['is_wicket'] == 1) & (balls_df['dismissal_kind'] != 'run out')]
top_wicket_takers = wickets_df['bowler'].value_counts().head(5)
plt.figure()
sns.barplot(x=top_wicket_takers.values, y=top_wicket_takers.index, palette='Greens_r')
plt.title("Top 5 Wicket Takers")
plt.xlabel("Wickets")
plt.ylabel("Bowler")
plt.tight_layout()
plt.show()





# Q26: Stadium with most matches hosted
stadium_matches = matches_df['venue'].value_counts()

# Visualization: Most Matches by Stadium (Q26)
stadium_matches = matches_df['venue'].value_counts().head(5)
plt.figure()
sns.barplot(x=stadium_matches.values, y=stadium_matches.index, palette='Purples')
plt.title("Top 5 Stadiums by Number of Matches")
plt.xlabel("Number of Matches")
plt.ylabel("Venue")
plt.tight_layout()
plt.show()



# Q27: Most Man of the Match awards
mom_awards = matches_df['player_of_match'].value_counts()




# Q28: Count of 4s hit in each season
fours_season = fours.merge(matches_df[['id', 'season']], on='id')
fours_by_season = fours_season.groupby('season').size()




# Q29: Count of 6s hit in each season
sixes_season = sixes.merge(matches_df[['id', 'season']], on='id')
sixes_by_season = sixes_season.groupby('season').size()


# Visualization: Count of 4s and 6s by Season (Q28 & Q29)
fours_season = fours.merge(matches_df[['id', 'season']], on='id')
sixes_season = sixes.merge(matches_df[['id', 'season']], on='id')
fours_by_season = fours_season.groupby('season').size()
sixes_by_season = sixes_season.groupby('season').size()
boundary_df = pd.DataFrame({'Fours': fours_by_season, 'Sixes': sixes_by_season}).fillna(0)
boundary_df.plot(kind='bar', stacked=True, colormap='Accent')
plt.title("Fours and Sixes Hit Per Season")
plt.xlabel("Season")
plt.ylabel("Count")
plt.tight_layout()
plt.show()









# Q30: Runs scored from boundaries (4s and 6s) per season
boundaries = balls_df[balls_df['batsman_runs'].isin([4, 6])]
boundaries_season = boundaries.merge(matches_df[['id', 'season']], on='id')
runs_from_boundaries = boundaries_season.groupby('season')['batsman_runs'].sum()




# Q31: Run contribution from boundaries (percentage) per season
total_runs_season = merged_df.groupby('season')['total_runs'].sum()
boundary_contribution_percent = (runs_from_boundaries / total_runs_season) * 100

(
    run_scorers.head(5),
    most_fours.head(5),
    most_sixes.head(5),
    strike_rate.head(5),
    leading_wicket_taker.head(5),
    stadium_matches.head(5),
    mom_awards.head(5),
    fours_by_season,
    sixes_by_season,
    runs_from_boundaries,
    boundary_contribution_percent
)

# Visualization: Boundary Contribution (%) by Season (Q31)
merged_df = balls_df.merge(matches_df[['id', 'season']], on='id')
total_runs_season = merged_df.groupby('season')['total_runs'].sum()
boundaries = balls_df[balls_df['batsman_runs'].isin([4, 6])]
boundaries_season = boundaries.merge(matches_df[['id', 'season']], on='id')
runs_from_boundaries = boundaries_season.groupby('season')['batsman_runs'].sum()
boundary_contribution_percent = (runs_from_boundaries / total_runs_season * 100).fillna(0)
plt.figure()
sns.lineplot(x=boundary_contribution_percent.index, y=boundary_contribution_percent.values, marker='o')
plt.title("Boundary Run Contribution by Season (%)")
plt.xlabel("Season")
plt.ylabel("Percentage of Runs from Boundaries")
plt.tight_layout()
plt.show()









# Q32: Team with most runs in first 6 overs (powerplay)
powerplay_runs = balls_df[balls_df['over'] < 6]
powerplay_team_runs = powerplay_runs.groupby('batting_team')['total_runs'].sum().sort_values(ascending=False)

# Visualization: Powerplay Runs by Team (Q32)
powerplay_runs = balls_df[balls_df['over'] < 6]
powerplay_team_runs = powerplay_runs.groupby('batting_team')['total_runs'].sum().sort_values(ascending=False).head(5)
plt.figure()
sns.barplot(x=powerplay_team_runs.values, y=powerplay_team_runs.index, palette='cividis')
plt.title("Top Teams by Total Powerplay Runs")
plt.xlabel("Runs in Overs 1-6")
plt.ylabel("Team")
plt.tight_layout()
plt.show()






# Q33: Team with most runs in last 4 overs (overs 17-20)
death_overs_runs = balls_df[balls_df['over'] >= 16]
death_team_runs = death_overs_runs.groupby('batting_team')['total_runs'].sum().sort_values(ascending=False)

# Visualization: Death Overs Runs by Team (Q33)
death_overs_runs = balls_df[balls_df['over'] >= 16]
death_team_runs = death_overs_runs.groupby('batting_team')['total_runs'].sum().sort_values(ascending=False).head(5)
plt.figure()
sns.barplot(x=death_team_runs.values, y=death_team_runs.index, palette='rocket')
plt.title("Top Teams by Total Death Overs Runs")
plt.xlabel("Runs in Overs 17-20")
plt.ylabel("Team")
plt.tight_layout()
plt.show()






# Q34: Best scoring run-rate in first 6 overs (min 10 innings)
powerplay_innings = powerplay_runs.groupby(['id', 'batting_team'])['total_runs'].sum().reset_index()
pp_runrate = powerplay_innings.groupby('batting_team')['total_runs'].agg(['sum', 'count'])
pp_runrate['run_rate'] = pp_runrate['sum'] / (pp_runrate['count'] * 6)
pp_runrate = pp_runrate[pp_runrate['count'] >= 10].sort_values(by='run_rate', ascending=False)

# Q35: Best scoring run-rate in last 4 overs (min 10 innings)
death_innings = death_overs_runs.groupby(['id', 'batting_team'])['total_runs'].sum().reset_index()
death_runrate = death_innings.groupby('batting_team')['total_runs'].agg(['sum', 'count'])
death_runrate['run_rate'] = death_runrate['sum'] / (death_runrate['count'] * 4)
death_runrate = death_runrate[death_runrate['count'] >= 10].sort_values(by='run_rate', ascending=False)

(
    powerplay_team_runs.head(5),
    death_team_runs.head(5),
    pp_runrate[['run_rate']].head(5),
    death_runrate[['run_rate']].head(5)
)
