import pandas as pd


vem_iter = pd.read_csv('/Users/michele/Documents/BigDive/Datasets/VEM/top_2018_01_01.csv',
                        chunksize=100000,
                        iterator=True,
                        header=None,
                        names=['id', 'date', 'lat', 'lon', 'speed', 'heading',
                              'quality', 'event', 'acceleration', 'distance'],
                        parse_dates=['date'],
                        infer_datetime_format=True,
                        date_parser=pd.to_datetime)

day = "28"
# start_date = pd.to_datetime("2018-01-19 00:00:01", infer_datetime_format=True)
start_date = pd.to_datetime("2018-01-" + day +  " 00:00:01", format="%Y-%m-%d %H:%M:%S")
end_date = pd.to_datetime("2018-01-" + day +  " 23:59:59", format="%Y-%m-%d %H:%M:%S")


df_vem = pd.concat([chunk[(chunk['date'] > start_date) & (chunk['date'] < end_date)]for chunk in vem_iter])


night_begin = pd.to_datetime("2018-01-" + day +  " 01:00:00", format="%Y-%m-%d %H:%M:%S")
night_end = pd.to_datetime("2018-01-" + day + " 05:00:00", format="%Y-%m-%d %H:%M:%S")
day_begin = pd.to_datetime("2018-01-" + day +  " 05:00:01", format="%Y-%m-%d %H:%M:%S")
day_end = pd.to_datetime("2018-01-" + day +  " 23:59:59", format="%Y-%m-%d %H:%M:%S")

df_vem_night = df_vem[(df_vem["date"]> night_begin) & (df_vem["date"] < night_end)]
df_vem_day = df_vem[(df_vem["date"]> day_begin) & (df_vem["date"] < day_end)]

df_vem_night.to_csv("/Users/michele/Documents/BigDive/Datasets/VEM/top_2018_01_" + day + "_night.csv")
df_vem_day.to_csv("/Users/michele/Documents/BigDive/Datasets/VEM/top_2018_01_" + day + "_day.csv")
