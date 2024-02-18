import os, requests, re, datetime
import pickle as pkl

cache_folder = os.path.join(os.path.abspath(os.curdir), "cache")

def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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

            if not is_convertible_to_int(line[0]):
                continue

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
            elif method == 2:
                accululation = float(line[1]) + float(line[2]) + float(line[3]) + float(line[4]) + float(line[5])

                # Add datapoint
                data.append(
                    dict(year=int(line[0]), month=1, day=1, billion_btu=accululation)
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

def get_eia_us_energy_consumption():
    return daily_cache("us_energy_consumption", 2,"https://www.eia.gov/energyexplained//us-energy-facts/charts/primary-consumption-by-major-source.csv")
