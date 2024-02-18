import requests
import re
import pickle as pkl
import os, datetime

cache_folder = os.path.join(os.path.abspath(os.curdir), "cache")
def retreive_data(url, method:int):
    # Fetch the content of the URL
    response = requests.get(url)

    data = []
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract text content from the response
        text_content = response.text

        for line in text_content.splitlines():

            # Remove the comments
            if line.startswith("%") or line.startswith("#") or line.startswith("\""):
                continue

            # strip line
            line = line.strip()

            # Remove duplicate spaces
            line = re.sub(' +', '', line)

            # Line split as array
            line = line.split(",")

            if method == 0:
                # Add datapoint
                data.append(
                    dict(year=int(line[0]), month=int(line[1]), day=int(line[2]), ppm=float(line[3]))
                )
            elif method == 1:
                dmt = line[0].split("-")
                # Add datapoint
                data.append(
                    dict(year=int(dmt[0]), month=int(dmt[1]), day=int(dmt[2]), ppm=float(line[6]))
                )

        # Rotate dictionary such that it is a dictionary with lists instead of a list with dictionaries.
        rotated_dict = {}
        # Iterate through each dictionary in the list
        for dictionary in data:
            # Iterate through each key-value pair in the dictionary
            for key, value in dictionary.items():
                # Append the value to the list associated with the key in the rotated dictionary
                rotated_dict.setdefault(key, []).append(value)

        # Return data
        return rotated_dict
    else:
        # Print an error message if the request was not successful
        print("Failed to fetch data from the URL.")


def daily_cache(name: str, method:int, url: str):
    cache_file = f"{cache_folder}\\{name}_cache.pkl"
    today_date = datetime.date.today()

    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as file:
            last_retrieval_date, cached_data = pkl.load(file)
            if last_retrieval_date == today_date:
                return cached_data

    data = retreive_data(url, method)

    if data:
        with open(cache_file, 'wb') as file:
            pkl.dump((today_date, data), file)

    return data


def get_situ_co2_ppm():
    return daily_cache("situ_co2_ppm", 0,"https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/daily/daily_in_situ_co2_mlo.csv")


def get_flask_c13_ppm():
    return daily_cache("flask_c13_ppm", 1,"https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/flask_isotopic/daily/daily_flask_c13_mlo.csv")


def get_flask_o18_ppm():
    return daily_cache("flask_o18_ppm", 1,"https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/flask_isotopic/daily/daily_flask_o18_mlo.csv")


def get_flask_co2_ppm():
    return daily_cache("flask_co2_ppm", 1,"https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/flask_co2/daily/daily_flask_co2_mlo.csv")