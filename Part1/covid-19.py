#!pip install dstack
import datetime
import numpy as np
import pandas as pd
#import plotly.express as px
from urllib.error import HTTPError
#from dstack import create_frame

now = datetime.datetime.now()

def validate(date_string):
    try:
        datetime.datetime.strptime(date_string, '%m-%d-%Y')
        return True
    except ValueError:
        return False



# Датафрейм для формирования агрегированных данных за день по странам
df_stats_row = pd.DataFrame(np.array([["", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),
                            columns=["Date", "Country", "Confirmed", "Recovered", "Deaths", "Active",
                                     "ConfirmedDiff", "RecoveredDiff", "DeathsDiff", "ActiveDiff"])

# Итоговый датафрейм для всех данных по дням и странам
df_stats = pd.DataFrame(columns=df_stats_row.columns)

# Датафрейм для хранения предыдущих данных
#prev_data = pd.DataFrame(np.array([["", 0.0, 0.0, 0.0, 0.0]]),
#                         columns=["Country", "Confirmed", "Recovered", "Deaths", "Active"])


print(df_stats_row.head())
print(df_stats.head())
print("====================")
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{0}.csv"
for mm in range(7, 7+1):
#for mm in range(1, now.month+1):
    #print("месяц:{0:02d}".format(mm))
    for dd in range(1, 12+1):
    #for dd in range(1, 31+1):
        #print("{0:02d}".format(dd))
        date_string = "{0:02d}-{1:02d}-{2:02d}".format(mm, dd, now.year)
        if validate(date_string):
            print(url.format(date_string))
            #try:
            if True:
                print("Попытка считать данные по дате {0}...".format(date_string), end=" ")
                df = pd.read_csv(url.format(date_string)) # загружаем датафрейм из URL
                print("[+] - всего строк:{0}.".format(len(df)))


                #print("===>", df[df["Country_Region"]=="Russia"].mean(column)[[column]])
                #print("===>", df[df["Country_Region"]!="Russia"].groupby("Country_Region").mean()[[column]])
                #df_per_country = df.groupby("Country_Region").mean()
                #print("===>", df_per_country.dtypes)
                #print("===>", df_per_country.columns)
                column = ""
                if "Country/Region" in df.columns:
                    column = "Country/Region"
                if "Country_Region" in df.columns:
                    column = "Country_Region"
                if column != "":
                    #for col in df_stats_row.columns:
                    df_stats_row[["Confirmed", "Recovered", "Deaths", "Active"]] = df.groupby(column).sum()[["Confirmed", "Recovered", "Deaths", "Active"]]
                    df_stats_row[["ConfirmedDiff", "RecoveredDiff", "DeathsDiff", "ActiveDiff", "Confirmed", "Recovered", "Deaths", "Active"]].sub(df_stats_row["Confirmed", "Recovered", "Deaths", "Active"], axis=0)

                    for df_country in df.groupby(column):
                        #print("df_country", df_country)
                        #print("df_country[0]", df_country[0])
                        #print("df_country[1]", df_country[1])
                        if len(df_country[1]) > 0:
                            df_stats_row["Date"] = date_string
                            df_stats_row["Country"] = df_country[0]
                            #print("df_country[0] ======>\""+df_country[0]+"\"")
                            #print("[df_country[0]] ======>\""+[df_country[0]]+"\"")
                            for column in df_stats_row.columns:
                                if column in df_country[1].columns:
                                    #column_diff = column + "Diff"
                                    #print("column_diff:", column_diff)
                                    #df_stats_row[column + "Diff"] = float(df_country[1][column].sum()) - float(df_stats_row[column][0])
                                    print("1. df_country[1][column].sum()=\'", float(df_country[1][column].sum()),"\' dtypes:", type(float(df_country[1][column].sum())))
                                    print("2. float(df_stats_row[column][0])=\'",  float(df_stats_row[column][0]),"\' dtypes:", type(float(df_stats_row[column][0])))
                                    #print(df_stats_row[column + "Diff"])
                                    print("3. df_stats_row[column + Diff]=\'", df_stats_row[column + "Diff"], "\' dtypes:", type(df_stats_row[column + "Diff"]))
                                    print("4. df_stats_row[column]=\'", df_stats_row[column], "\' dtypes:", type(df_stats_row[column]))
                                    #print("df_stats_row[column][0]=\'", df_stats_row[column][0],"\' dtypes:", type(df_stats_row[column][0]))
                                    #df_stats_row[column + "Diff"] = df_country[1][column].sum() - 0.0
                                    #print("df_stats_row[column_diff]=\'", df_stats_row[column + "Diff"][0], "\', dtypes:", df_stats_row[column + "Diff"].dtypes)
                                    df_stats_row[column] = df_country[1][column].sum()
                                    #print("=======>", prev_data.loc[prev_data["Country"] == df_country[0]], "column:",column)
                                    #print("=======>", prev_data.loc[prev_data["Country"] == df_country[0], column])
                                    #df_stats_row[column + "Diff"] = df_stats_row[column] - prev_data.query('Country == ' + df_country[0])[column]
                                    #prev_data.query('Country == ' + df_country[0])[column] = df_stats_row[column]
                                    #prev_data.loc[prev_data["Country"] == df_country[0], column] = df_stats_row[column]
                                    #df_stats_row[column + "Diff"] = df_stats_row[column + "Diff"] - df_stats_row[column]
                            df_stats_row[[column + "Diff", column]].sub(df_stats_row[column], axis=0)
                            df_stats = df_stats.append(df_stats_row, ignore_index=True)
                            #print(df_stats_row)


            #except HTTPError as err:
                #if err.code == 404:
                    #print("[-] - данные отсутствуют.")
            #except Exception:
                #print("[-] - непредвиденная ошибка.")



print(df_stats.head(300)) # отображаем первые N строк, чтобы понять что мы скачали
print(df_stats.query('Country == "Russia"')) # отображаем строки для страны NAME, чтобы понять что мы скачали
