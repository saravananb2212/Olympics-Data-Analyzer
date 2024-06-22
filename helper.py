import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def data_over_time(df, col):
    # Drop duplicates based on 'Year' and the specified column
    nations_over_time = df.drop_duplicates(['Year', col])

    # Count occurrences of 'Year' and reset index
    nations_over_time = nations_over_time['Year'].value_counts().reset_index()

    # Rename columns appropriately
    nations_over_time.columns = ['Edition', col]

    # Ensure 'Edition' column is sorted
    nations_over_time = nations_over_time.sort_values('Edition')

    return nations_over_time


def most_successful(df, sport):
    # Filter the DataFrame based on the selected sport if not 'Overall'
    temp_df = df
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Debugging: Check the contents of temp_df
    print(temp_df.head())

    # Count the occurrences of each athlete's name and reset index
    x = temp_df['Name'].value_counts().reset_index()
    
    # Debugging: Check the contents of x
    print(x.head())

    # Rename columns for clarity
    x.columns = ['Name', 'count']
    
    # Merge the count data with the original DataFrame
    x = x.merge(df, on='Name', how='left')
    
    # Debugging: Check the merged DataFrame
    print(x.head())

    # Drop duplicates and keep only necessary columns
    x = x.drop_duplicates(subset=['Name'])
    
    # Select top 15 most successful athletes
    x = x.head(15)
    
    # Debugging: Check the final DataFrame
    print(x.head())

    return x[['Name', 'count', 'Sport', 'Team', 'region', 'Medal']]

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Count occurrences of each athlete's name
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']  # Rename columns for clarity
    
    # Merge with original DataFrame to get additional details
    x = x.merge(df, left_on='Name', right_on='Name', how='left')
    
    # Drop duplicates and keep only necessary columns
    x = x.drop_duplicates(subset=['Name'])
    
    # Select top 10 most successful athletes
    x = x.head(10)[['Name', 'Medals', 'Sport']]
    
    return x

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
