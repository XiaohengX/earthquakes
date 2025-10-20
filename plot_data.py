import requests
import json
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

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

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    magnitude = earthquake['properties']['mag']
    return magnitude


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = {}
    for quake in earthquakes:
        year = get_year(quake)
        magnitude = get_magnitude(quake)
        if year not in magnitudes_per_year:
            magnitudes_per_year[year] = []
        magnitudes_per_year[year].append(magnitude)
    return magnitudes_per_year


def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())

    # Fill in missing years with 0 values
    if years:
        all_years = list(range(min(years), max(years) + 1))
        average_magnitudes = []
        for year in all_years:
            if year in magnitudes_per_year:
                magnitudes = magnitudes_per_year[year]
                average_magnitude = sum(magnitudes) / len(magnitudes)
                average_magnitudes.append(average_magnitude)
            else:
                average_magnitudes.append(0)
    else:
        all_years = []
        average_magnitudes = []

    plt.bar(all_years, average_magnitudes)

    # Add value labels above each bar
    for year, value in zip(all_years, average_magnitudes):
        if value > 0:  # Only show label if there's data
            plt.text(year, value, f'{value:.2f}', ha='center', va='bottom', fontsize=8)

    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.title('Average Earthquake Magnitude per Year')
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_number_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())

    # Fill in missing years with 0 values
    if years:
        all_years = list(range(min(years), max(years) + 1))
        number_of_earthquakes = []
        for year in all_years:
            if year in magnitudes_per_year:
                number_of_earthquakes.append(len(magnitudes_per_year[year]))
            else:
                number_of_earthquakes.append(0)
    else:
        all_years = []
        number_of_earthquakes = []

    plt.bar(all_years, number_of_earthquakes)

    # Add value labels above each bar
    for year, value in zip(all_years, number_of_earthquakes):
        if value > 0:  # Only show label if there's data
            plt.text(year, value, str(value), ha='center', va='bottom', fontsize=8)

    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.title('Number of Earthquakes per Year')
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)