import pandas as pd 
import numpy as np

import folium
import requests
from geopy.geocoders import Nominatim


train = pd.read_csv("train.csv")

train_new = train[["아파트명", "좌표X", "좌표Y", "시군구", "번지"]]
train_new["주소명"] = train["시군구"] + ' ' + train["번지"]
apt_name = train_new["아파트명"].unique()

# print(train_new.iloc[0])

############### test ##################
# location_test = geolocator.geocode("서울시 강남구 개포동 658-1")
#######################################

geolocator = Nominatim(user_agent="geoapi")


def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        return location.latitude, location.longitude
    except:
        return None, None


unique_idx = train_new.drop_duplicates(subset="아파트명").index
apt_uniq = train_new.loc[unique_idx].reset_index(drop=True)
apt_uniq["주소명"] = apt_uniq["시군구"] + ' ' + apt_uniq["번지"]

############### test ##################

sample = apt_uniq[0:3]
new_x = []; new_y = []

# get_coordinates(sample["주소명"][1])
sample["주소명"]

geolocator.geocode("서울특별시 강남구 개포동 652")

for i in range(len(sample)):
    temp_coor = get_coordinates(sample["주소명"][i])
    new_x.append(temp_coor[0])
    new_y.append(temp_coor[1])


sample["좌표_X_new"] = new_x
sample["좌표_Y_new"] = new_y

#######################################

new_x = []; new_y = []

for i in range(len(apt_uniq)):
    temp_coor = get_coordinates(apt_uniq["주소명"][i])
    new_x.append(temp_coor[0])
    new_y.append(temp_coor[1])


