import pandas as pd


def preprocess(df, region_df):

    # filtering for summer olympic
    df = df[df['Season'] == 'Summer']
    # merge with regions_df
    df = df.merge(region_df, on='NOC', how='left')
    # droping duplicate
    df.drop_duplicates(inplace=True)
    # one hot encoding meadl
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    # Removing year in olympic is not held
    df = df[df['Year'] != 1906]
    df = df[df['Year'] != 2002]
    df = df[df['Year'] != 2006]
    df = df[df['Year'] != 2010]
    df = df[df['Year'] != 2014]
    df = df[df['Year'] != 1994]
    df = df[df['Year'] != 1998]

    return df
