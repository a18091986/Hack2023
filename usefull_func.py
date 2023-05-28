from geopandas.tools import geocode
import math


def get_coords(city, street):
    city = city.replace('город', '').replace('г.', '').replace('.', '').replace('Г.', '')
    try:
        loc = ','.join([city, street])
        dataframe = geocode(loc, provider="nominatim", user_agent='my_request')
        point = dataframe.geometry.iloc[0]
        return point.y, point.x
    except Exception as e:
        return None, None


def get_dist(x1, y1, x2, y2):
    p1 = (x1, y1) if not math.isnan(x1) and x1 and not math.isnan(y1) and y1 else 0
    p2 = (x2, y2) if not math.isnan(x2) and x2 and not math.isnan(y2) and y2 else 0
    # print(p1, p2)
    return GD(p1, p2).km if p1 and p2 else 0


