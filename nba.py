import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.model_selection import train_test_split

file # = Insert file for player data
file2 # = Insert file for team data

draftRoundMap = {
    "1": 1,
    "2": 2,
    "3": 3, 
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "0": 8,
    "Undrafted": 8,
}

draftYearMap = {
    '2009': 2009, 
    '1996': 1996, 
    '2014': 2014, 
    '2018': 2018, 
    '2012': 2012, 
    '1997': 1997, 
    '2007': 2007, 
    '2008': 2008,
    '2003': 2003, 
    '2013': 2013, 
    '2017': 2017, 
    '1995': 1995, 
    '2001': 2001, 
    '2011': 2011, 
    '1992': 1992, 
    '2010': 2010,
    '2015': 2015, 
    '1998': 1998, 
    '2019': 2019, 
    '1993': 1993, 
    '2000': 2000, 
    '2016': 2016, 
    '2002': 2002, 
    '2005': 2005,
    '1999': 1999, 
    '2004': 2004, 
    '2020': 2020, 
    '2006': 2006, 
    '1985': 1985, 
    '1990': 1990, 
    '1984': 1984, 
    '1994': 1994,
    '2021': 2021, 
    'Undrafted': 0, 
    '2022': 2022, 
    '1987': 1987, 
    '1989': 1989, 
    '1988': 1988, 
    '1991': 1991,
    '1986': 1986, 
    '1982': 0, 
    '1963': 0,
}

teamMap = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Bobcats": "CHA",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "LA Clippers": "LAC",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Jersey Nets": "NJN",
    "New Orleans Hornets": "NOH",
    "New Orleans/Oklahoma City Hornets": "NOK",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Seattle SuperSonics": "SEA",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Vancouver Grizzlies": "VAN",
    "Washington Wizards": "WAS",
}

seasonMap = {
    "2000-01": 2000,
    "2001-02": 2001,
    "2002-03": 2002,
    "2003-04": 2003,
    "2004-05": 2004,
    "2005-06": 2005,
    "2006-07": 2006,
    "2007-08": 2007,
    "2008-09": 2008,
    "2009-10": 2009,
    "2010-11": 2010,
    "2011-12": 2011,
    "2012-13": 2012,
    "2013-14": 2013,
    "2014-15": 2014,
    "2015-16": 2015,
    "2016-17": 2016,
    "2017-18": 2017,
    "2018-19": 2018,
    "2019-20": 2019,
    "2020-21": 2020,
    "2021-22": 2021,
    "2022-23": 2022,
}

df = pd.read_csv(file)
df = df.iloc[1757:, 1:]
collegeMap = {}
for i in range(len(df['college'].unique())):
    college = df['college'].unique()[i]
    collegeMap[college] = i
for i in range(len(df)):
    college = df.iloc[i].college
    df.at[i+1757, 'college'] = collegeMap[college]
countryMap = {}
for i in range(len(df['country'].unique())):
    country = df['country'].unique()[i]
    countryMap[country] = i
for i in range(len(df)):
    country = df.iloc[i].country
    df.at[i+1757, 'country'] = countryMap[country]
for i in range(len(df)):
    draftYear = df.iloc[i].draft_year
    df.at[i+1757, 'draft_year'] = draftYearMap[draftYear]
for i in range(len(df)):
    draftRound = df.iloc[i].draft_round
    df.at[i+1757, 'draft_round'] = draftRoundMap[draftRound]
for i in range(len(df)):
    draftNumber = df.iloc[i].draft_number
    if draftNumber != 'Undrafted':
        df.at[i+1757, 'draft_number'] = int(draftNumber)
    else:
        df.at[i+1757, 'draft_number'] = 0
for i in range(len(df)):
    season = df['season'].iloc[i]
    df.at[i+1757, 'season'] = seasonMap[season]
df = df.sort_values('pts', ascending=False)

df2 = pd.read_csv(file2)
df2 = df2[["Team", "win_percentage", "season"]]
for i in range(len(df2)):
    teamName = df2['Team'].iloc[i]
    df2.at[i, 'Team'] = teamMap[teamName]
for i in range(5):
    for k in range(18):
        col_name = df.columns[k+2]
        df2.insert(i*18+k+3, 'Player ' + str(i+1) + ' ' + col_name, ['N/A' for x in range(716)], True)
df2 = df2.iloc[30:]
for s in range(len(df2)):
    season = df2['season'].iloc[s]
    df2.at[s+30, 'season'] = seasonMap[season]
for i in range(len(df)):
    player = df.iloc[i]
    name = player.player_name
    team = player.team_abbreviation
    season = player.season
    res = df2.loc[df2['Team'] == team].loc[df2['season'] == season]
    if res.iloc[0]['Player 1 age'] == 'N/A':
        for k in range(18):
            col_name = df2.columns[k+3]
            df2.at[res.index[0], col_name] = player.iloc[k+2]
    elif res.iloc[0]['Player 2 age'] == 'N/A':
        for k in range(18):
            col_name = df2.columns[k+21]
            df2.at[res.index[0], col_name] = player.iloc[k+2]
    elif res.iloc[0]['Player 3 age'] == 'N/A':
        for k in range(18):
            col_name = df2.columns[k+39]
            df2.at[res.index[0], col_name] = player.iloc[k+2]
    elif res.iloc[0]['Player 4 age'] == 'N/A':
        for k in range(18):
            col_name = df2.columns[k+57]
            df2.at[res.index[0], col_name] = player.iloc[k+2]
    elif res.iloc[0]['Player 5 age'] == 'N/A':
        for k in range(18):
            col_name = df2.columns[k+75]
            df2.at[res.index[0], col_name] = player.iloc[k+2]
df2

df3 = df2.iloc[:, 1:]
filename = "nbadata.csv"
df3.to_csv(filename, sep=',', index=False, encoding='utf-8')

df0 = pd.read_csv(filename)
df0 = df0.sample(frac=1)

df_train = df0.iloc[:550] # ~80%
df_test = df0.iloc[550:] # ~20%

X_train = df_train.copy()
y_train = X_train.pop('win_percentage')

X_test = df_test.copy()
y_test = X_test.pop('win_percentage')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.metrics import MeanAbsolutePercentageError

model = keras.Sequential([
    layers.Input([91]),
    layers.Dense(units=512, activation='relu'),
    layers.Dense(units=512, activation='relu'),
    layers.Dense(units=512, activation='relu'),
    layers.Dense(units=512, activation='relu'),
    layers.Dense(units=512, activation='relu'),
    layers.Dense(units=1),
])

model.compile(
    optimizer='adam',
    loss='mae',
    metrics = [MeanAbsolutePercentageError()]
)

history = model.fit(
    X_train, y_train,
    validation_data=(X_train, y_train),
    batch_size=128,
    epochs=150,
)

model = tf.keras.models.load_model('nba-model.keras')

def makePrediction(players, season):
    data = np.array([[0.0 for x in range(91)]])
    data[0][0] = season
    for i in range(5):
        player = df.loc[df['player_name'] == players[i]].loc[df['season'] == season]
        for k in range(18):
            data[0][i*18+k+1] = player.iloc[0, k+2]
    pred = round(model.predict(data)[0][0], 3)
    print("Estimated win percentage: ", end="")
    print(pred)
    print("Estimated record: ", end="")
    print(round(pred*82), end="")
    print("-", end="")
    print(round((1-pred)*82))