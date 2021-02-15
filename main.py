'''
This module creates a web map. The web map displays information about the
locations of films that were shot in a given year.
'''


def read_info(file_path: str, year: str) -> list():
    '''
    This function reads the movies of the desired year from the
    list, lists them, replaces them with coordinates and returns
    this new list.

    >>> type(read_info('locations.list', '1980'))
    <class 'list'>
    >>> len(read_info('locations.list', '1980')[:10])
    10
    '''

    values = [] 
    with open(file_path, "r", encoding = "utf-8", errors = 'ignore') as file:
        counter = 0
        for line in file:
            counter += 1
            if 'Federal' not in line and 'Highway' not in line and counter > 14:
                line = line.strip().split('\t')
                line = list(filter(lambda elem: elem != '', line))
                line[0] = line[0].replace('\'', '')
                line[0] = line[0].replace('\"', '')
                line[0] = line[0].split('(')
                line[0][1] = line[0][1][:4]
                line[0] = line[0][:2]
                if line[0][1] != year:
                    continue
                if len(line[0]) > 2:
                    line[0].pop(2)
                if len(line) > 2:
                    line.pop(2)
                geolocator = Nominatim(user_agent="film location", scheme='http')
                geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
                ctx = ssl.create_default_context(cafile=certifi.where())
                geopy.geocoders.options.default_ssl_context = ctx
                location = geolocator.geocode(line[1])
                if location == None:
                    continue
                else:
                    line[1] = (location.latitude, location.longitude)
                if line not in values:
                    values.append(line)
    return values


def find_closest_locations(file_path: str, year: str, user_x, user_y: float) -> list():
    '''
    This function returns a list of the 10 closest shooting scenes
    to the user's coordinates.

    >>> type(find_closest_locations('locations.list', '1980', 20, 20))
    <class 'list'>
    >>> len(find_closest_locations('locations.list', '1989', 49, 50))
    10
    '''

    values = read_info(file_path, year)
    for i in range(len(values)):
        distance = distance_between_points(user_x, user_y, values[i][1][0], values[i][1][1])
        values[i].append(distance)
    values.sort(key=lambda x:x[2])
    return values[:10]


def distance_between_points(user_x, user_y, scene_x, scene_y: float) -> int:
    '''
    This function returns distance between user's and scene's coordinates.

    >>> distance_between_points(20, 20, 50, 50)
    4253
    >>> distance_between_points(49.83826, 24.02324, 30.2686032, -97.7627732)
    9442
    '''
    userloc = (user_x, user_y)
    filmloc = (scene_x, scene_y)
    distance = geopy.distance.geodesic(userloc, filmloc).km
    return int(distance)


def create_map(values: list(), user_x: float, user_y: float):
    '''
    This function creates a map with 3 layers. The map shows 10 labels
    of the nearest filming locations.
    '''

    map = folium.Map(tiles="Stamen Terrain", location=[user_x,user_y])
    fg = folium.FeatureGroup(name='Scenes')
    fg_2 = folium.FeatureGroup(name='Distances')
    for film in values:
        distance = film[2]
        film_x = film[1][0]
        film_y = film[1][1]
        name = film[0][0]
        fg.add_child(folium.Marker(location=[film_x,film_y], popup=name, icon=folium.Icon()))
        fg_2.add_child(folium.CircleMarker(location=[film_x,film_y], radius=10,
            fill_color = color_creator(distance), color = 'black', fill_opacity = 1))
    map.add_child(folium.Marker(location=[user_x,user_y], popup='ME', icon=folium.Icon()))
    map.add_child(fg)
    map.add_child(fg_2)
    map.add_child(folium.LayerControl())
    map.save('Film_Scenes_Map.html')


def color_creator(distance : int) -> str:
    '''
    This function returns color depending on distance parameter.

    >>> color_creator(300)
    'green'
    >>> color_creator(1000)
    'yellow'
    >>> color_creator(2000)
    'red'
    '''

    if distance < 800:
        return 'green'
    elif 800 <= distance <= 1300:
        return 'yellow'
    else:
        return 'red'


if __name__ == "__main__":
    import pandas as pd
    import csv
    import folium
    import certifi
    import ssl
    import geopy.distance
    from geopy.distance import geodesic
    from geopy.exc import GeocoderUnavailable
    from geopy.exc import GeocoderTimedOut
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    
    print('Please enter a year you would like to have a map for:')
    year = str(input())
    print('Please enter latitude:')
    user_lat = input()
    print('Please enter longitude:')
    user_long = input()
    print('Map is generating...')
    values = find_closest_locations('locations.list', year, user_lat, user_long)
    print('Please wait...')
    create_map(values, user_lat, user_long)
    print('Finished. Please have a look at the map Film_Scenes_Map.html')
