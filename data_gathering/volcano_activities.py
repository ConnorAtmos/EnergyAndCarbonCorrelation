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

        counter = {}

        for line in text_content.splitlines():

            # Remove the comments
            if line.startswith("%") or line.startswith("#") or line.startswith("\""):
                continue

            # strip line
            line = line.strip()

            # Remove duplicate spaces
            line = re.sub(' +', '', line)

            # Line split as array
            if method == 3:
                line = line.split(";")
            else:
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
            elif method == 3:
                year = line[0]
                if not (year in counter.keys()):
                    counter[year] = 0

                counter[year] += 1

        if method == 3:
            keys_integer = counter.keys()

            sorted_keys = []
            for key in keys_integer:
                sorted_keys.append(int(key))
            sorted_keys = sorted(sorted_keys)

            for key in sorted_keys:
                data.append(
                    dict(year=key, month=1, day=1, instances=counter[str(key)])
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

def get_volcano_eruption_instances():
    return daily_cache("volcano_activities", 3,"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/significant-volcanic-eruption-database/exports/csv?lang=en&timezone=America%2FChicago&use_labels=true&delimiter=%3B")

