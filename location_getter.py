from flask import Flask, render_template, request
import requests
import folium
from pprint import pprint
from folium.plugins import MarkerCluster
from haversine import haversine
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="map_builder")
app = Flask(__name__)


def find_friends_location(screen_name: str, bearer_token: str) -> list:
    """
    Return the list of tuples with friends' twitter nicknames and theirs location.
    If user inputs wrong screen_name return an empty list.
    """
    base_url = "https://api.twitter.com/"
    search_url = f"{base_url}1.1/friends/list.json"
    search_headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    search_params = {
        "screen_name": screen_name,
        "count": 20
    }

    response = requests.get(
        search_url, headers=search_headers, params=search_params)
    json_response = response.json()
    # pprint(json_response)
    if not json_response or 'errors' in json_response:
        return []
    loc_and_names = []
    for info in json_response['users']:
        if not info['location']:
            continue
        loc_and_names.append((info['screen_name'], info['location']))
    return loc_and_names


def location_to_coordinates(friends_locations: list) -> list:
    """
    Return a list where all second elements of tuple
    from the friends_location are replaced with the coordinates of the certain place.
    """
    global geolocator
    coord_list = []
    # print(friends_locations)
    for friend in friends_locations:
        try:
            location = geolocator.geocode(friend[-1])
            if not location:
                continue
            coord_list.append([
                friend[0], (location.latitude, location.longitude)])
        except Exception:
            continue
    return coord_list[:15]


def map_builder(friends_location: list) -> object:
    """
    Return a folium Map object with markers on the locations from the given list
    with names-popups above them.

    friends_location list should be a list of tuples, where the first element
    is the twitter nickname and the second is a tuple with user's location coordinates.
    """
    mapa = folium.Map()
    lat = [x[-1][0] for x in friends_location]
    lon = [x[-1][1] for x in friends_location]
    names = [x[0] for x in friends_location]
    frnds = folium.FeatureGroup(name="Friends Markers")
    marker_cluster = MarkerCluster().add_to(frnds)

    for lt, ln, nm in zip(lat, lon, names):
        folium.Marker(location=[lt, ln],
                      popup=nm,
                      icon=folium.Icon(color='red')).add_to(marker_cluster).add_to(marker_cluster)

    mapa.add_child(frnds)
    return mapa


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    nickname = request.form.get("screen_name")
    user_token = request.form.get("bearer_token")
    if not nickname or not user_token:
        return render_template("failure0.html")

    friends_locations = find_friends_location(nickname, user_token)
    if not friends_locations:
        return render_template("failure.html")

    locations = location_to_coordinates(friends_locations)
    if not locations:
        return "cannot find any locations on the map , sorry :)"

    mapa = map_builder(locations)
    return mapa._repr_html_()


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8000)
