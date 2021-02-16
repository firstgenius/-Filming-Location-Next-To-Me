# -Filming-Location-Next-To-Me

This module creates a web map. The web map displays information about the locations of films that were shot in a given year.

## More about module

The result is a map with three layers: the films' locations, user's locations and distance between user's location and scene's location. You can add and remove layers on the map using the layer control. 


#### Module includes 5 different functions:

#### 1) read_info
This function reads the movies of the desired year from the list, lists them, replaces them with coordinates and returns this new list.

#### 2) find_closest_locations
This function returns a list of the 10 closest shooting scenes to the user's coordinates.

#### 3) distance_between_points
This function returns distance between user's and scene's coordinates.

#### 4) create_map
This function creates a map with 3 layers. The map shows 10 labels of the nearest filming locations.

#### 5) color_creator
This function returns color depending on distance parameter.

## Installation

Just download code and use it!)

## Usage

```python

Please enter a year you would like to have a map for:
2014
Please enter latitude:
49
Please enter longitude:
30
Map is generating...
Please wait...
Finished. Please have a look at the map Film_Scenes_Map.html
```
## RESULTS

![text](photo/map.png?raw=true "text")

Movie location markers have three different colors: green, yellow, red. The color depends on the farness of the location from the user.

1. If the location is at a distance of up to 800 km, the marker is green.
2. if the distance is from 800 to 1200 km, the marker becomes yellow. 
3. Accordingly, in all different situations the marker becomes red.

After clicking on a location marker, user receives a name of the movie that was filmed in that place.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
