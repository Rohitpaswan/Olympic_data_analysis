import streamlit as st
import pandas as pd
import helper
import preprocessor
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('logo.png')
# creaing radio buttton for user
user_menu = st.sidebar.radio('Select an Option',
                             ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis'))

# if user click on medal tally
if user_menu == 'Medal Tally':
    st.sidebar.header('Summer Olympic Analysis')
    # stroing country and years list
    years, country = helper.country_year_list(df)
    selected_country = st.sidebar.selectbox("Select the country", country)
    selected_year = st.sidebar.selectbox("Select the year", years)

    # different cases depand on user selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall performance")

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    # fetching data from df on the basis of year and country
    medal_tally = helper.fetch_medal_tally(selected_year, selected_country, df)
    st.table(medal_tally)

## Overall analysis

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    # creating column
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(editions)

    # creating column
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Plotting graph between  number of countries over the year
    st.title("Countries participated over the year")
    nations_over_year = helper.participating_data_over_time(df, 'region')
    flg = px.line(nations_over_year, x='Editions', y='region')
    st.plotly_chart(flg)

    # Plotting graph between  number of event vs year
    st.title("Events over the years")
    events_over_year = helper.participating_data_over_time(df, 'Event')
    flg = px.line(events_over_year, x='Editions', y='Event')
    st.plotly_chart(flg)

    # Plotting graph between  athletes vs year
    st.title("Athletes over the years")
    athletes_over_year = helper.participating_data_over_time(df, 'Name')
    flg = px.line(athletes_over_year, x='Editions', y='Name')
    st.plotly_chart(flg)

    # Plotting heatmap between  number of events in sports vs year
    st.title("No. of Events over time(Each sport)")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    # Country wise analysis

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    # Plotting line plot country and medal over the year
    # Extracting all of the country list
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select the country", country_list)
    st.title(selected_country + ' Medal Tally Over the years')
    country_df = helper.yearwise_country_medal(df, selected_country)

    # if country_df is empty
    if country_df.empty:
        # if country has zero number of medal over the year
        temp_df = df[df['region'] == 'Albania']
        new_df = temp_df.groupby('Year').count()['Medal'].reset_index()
        flg = px.line(new_df, x='Year', y='Medal')
        st.plotly_chart(flg)

    else:
        flg = px.line(country_df, x='Year', y='Medal')
        st.plotly_chart(flg)

    # hitmap visiozation of country between sport over the year
    hit_df = helper.country_heat_map(df, selected_country)
    st.title(selected_country+" Performance in the following sports")
    if hit_df.empty:
        temp_df2 = df[df['region'] == selected_country]
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(
            temp_df2.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(
                'int'), annot=True)
        st.pyplot(fig)

    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(
            hit_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int'),
            annot=True)
        st.pyplot(fig)

    #Top 10 Successful olympic athlete for selected country
    st.title("Top 10 athletes of "+ selected_country)
    top_athlete_list = helper.most_successful(df,selected_country)
    st.table(top_athlete_list)
