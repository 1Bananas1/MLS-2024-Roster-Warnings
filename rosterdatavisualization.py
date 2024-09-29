import pandas as pd
import numpy as np
import time
import plotly.express as px

data = pd.read_csv('final_player_info_with_age.csv')
age_range = pd.read_csv('age_range.csv')

positions = ['GK', 'RB', 'CB', 'LB', 'CM', 'DM', 'AM', 'W', 'S','OB'] 
eras = ['breakthrough', 'development', 'peak', 'twilight']
teams = data['team'].unique()
player_data = []
warnings = []
for team in teams:
    print('')
    for position in positions:
        position_ranges = age_range[age_range['position'] == position]
        for _, row in position_ranges.iterrows():
            for i in range(1,len(eras) + 1):
                age_range_era = row.iloc[i].split('-')
                
                start_age = int(age_range_era[0])
                end_age = int(age_range_era[1])
                players_in_range = data[
                    (data['team'] == team)
                    & (data['primary_position'] == position)
                    & (data['age_decimal'] >= start_age)
                    & (data['age_decimal'] < end_age+1)
                ]
                count = len(players_in_range)
                player_data.append(
                    {
                        'Team': team,
                        'Position': position,
                        'Era': eras[i-1],
                        'Age Range': f"{start_age}-{end_age}",
                        'Player Count': count
                    }
                )    
                if count > 2:
                    players_in_range = players_in_range.drop('total_minutes', axis=1)
                    warnings.append(
                        f'Warning: Team {team} has more than 2 players in the {position} position '
                        f'within the age range {start_age} - {end_age} ({eras[i-1]}).\nCurrently: \n{players_in_range.to_string(index=False,header=False)}'
                    )

player_counts_df = pd.DataFrame(player_data)
# player_counts_df.to_csv('player_counts_df.csv')

print(player_counts_df)
for i in range(len(warnings)):
    print(warnings[i])
    print('')


def createStackedBarChart(team_name):
    team_data = player_counts_df[player_counts_df['Team'] == team_name]

    # Group by Position and Era
    team_data_grouped = team_data.groupby(['Position', 'Era'])['Player Count'].sum().reset_index()

    # Create the stacked bar chart
    fig = px.bar(
        team_data_grouped,
        x='Position',
        y='Player Count',
        color='Era',  # Now color by 'Era'
        barmode='stack',
        title=f'Player Distribution by Era for {team_name}',
        labels={'Player Count': 'Number of Players'}
    )

    fig.update_layout(
        xaxis={'categoryorder':'total ascending'},
        showlegend=True,
        legend_title='Age Era'
    )

    fig.show()

createStackedBarChart('San Jose Earthquakes')



