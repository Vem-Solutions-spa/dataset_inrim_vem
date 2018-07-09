import pandas as pd


vem_iter = pd.read_csv('../Datasets/VEM/top_2018_01_019_2018_01_23.csv', chunksize=100000, nrow=100000\
                        iterator=True, header=None,\
                        names=['id', 'date', 'lat', 'lon', 'speed', 'heading', \
                              'quality', 'event', 'acceleration', 'distance'],
                        parse_dates=['date'],infer_datetime_format=True, date_parser=pd.to_datetime)


start_date = pd.to_datetime("2018-01-19 00.00", unit='s')
end_date = pd.to_datetime("1516702403", unit='s')

start_date

df_vem = pd.concat([chunk[(chunk['date'] > start_date) & (chunk['date'] < end_date)]for chunk in vem_iter])
