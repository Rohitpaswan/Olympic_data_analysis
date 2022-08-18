import numpy as np


def medal_tally(df):
    # creating new datafram 'meadl_tally' by removing duplicates
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Grouping on basis of region
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally["Bronze"].astype('int')
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


# creating year list and country list
def country_year_list(df):
    # extracting list of all unique year (year in which olympic played)
    years = df['Year'].unique().tolist()

    years.sort()
    years.insert(0, 'Overall')

    # dropping all nun value and extracting  list of country
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


# fetching the data from medal tally based on of year and country by fetch_medal function
def fetch_medal_tally(years, country, df):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == years]
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == years) & (medal_df['region'] == country)]

    # grouping on the basis of year
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    # grouping on the basis of region
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=True).reset_index()
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x["Bronze"].astype('int')
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


# creating
def participating_data_over_time(df, cl):
    # removing duplicate rows having same years and region
    nations_over_year = df.drop_duplicates(['Year', cl])
    nations_over_year = nations_over_year['Year'].value_counts().reset_index().sort_values('index')
    nations_over_year = nations_over_year.rename(columns={'index': 'Editions', 'Year': cl})
    return nations_over_year


def yearwise_country_medal(df, selected_country):
    temp_df = df.dropna(subset=['Medal'])
    # removing duplicates
    new_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # selecting country from datafram
    new_df = temp_df[temp_df['region'] == selected_country]
    # storing number of medal year wise in new_df
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_heat_map(df, selected_country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == selected_country]

    return new_df


def most_successful(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(9)
    x.rename(columns={'index': 'Name', 'Name': 'Medals'}, inplace=True)
    return x
