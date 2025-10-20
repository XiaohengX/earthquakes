# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    text_json = json.loads(text)
    with open('my_file.json', 'w') as f:
        json.dump(text_json, f, indent=4)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.load(open('my_file.json', 'r'))

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    magnitude= [earthquake['properties']['mag']]
    return magnitude


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    location = [earthquake['geometry']['coordinates'][0:2]]
    return location


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    magnitudes=[]
    locations=[]
    for earthquake in data['features']:
        magnitudes.append(get_magnitude(earthquake))
        locations.append(get_location(earthquake))
    
    max_magnitude = max(magnitudes)
    max_location = [
        locations[i] for i, mag in enumerate(magnitudes) 
        if mag == max_magnitude
    ]
    return max_magnitude, max_location

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Total number of earthquakes is {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
