import pandas as pd
import os

files = os.listdir("/Users/michele/Documents/BigDive/Datasets/VEM/")
files =[k for k in files if ("top" in k) & (("night" in k) | ("day" in k))]


for file in files:
    df = pd.read_csv("/Users/michele/Documents/BigDive/Datasets/VEM/" + file)

    df = df[(df['acceleration'] == 0) & (df['event'] == 1)]
    df = df[((df['lat'] < 45.0942) & (df['lat'] > 45.0155)) & ((df['lon'] > 7.65) & (df['lon'] < 7.6954))]

    df.to_csv("/Users/michele/Documents/BigDive/Datasets/VEM/cleaned_data/clean" + file)
