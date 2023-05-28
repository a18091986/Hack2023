from geopandas.tools import geocode


def get_coords(city, street):
    city = city.replace('город', '').replace('г.', '').replace('.', '').replace('Г.', '')
    try:
        loc = ','.join([city, street])
        dataframe = geocode(loc, provider="nominatim", user_agent='my_request')
        point = dataframe.geometry.iloc[0]
        return point.y, point.x
    except Exception as e:
        return None, None


