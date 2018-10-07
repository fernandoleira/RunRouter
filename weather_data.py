import json
import urllib.request


API_KEY = "HackPSU2018"

# Function to search a city location
def search_location(api_key, q):
    # Parse query
    q = str.replace(q, ' ', '%20')
    # API url request
    url = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey={0}&q={1}&details=false&offset=10".format(
        api_key,
        q
    )
    with urllib.request.urlopen(url) as url:
        location_data = json.loads(url.read().decode())[0]

    # Format and Return Response
    res = {
        "Type": location_data["Type"],
        "Key": location_data["Key"],
        "City": location_data["EnglishName"],
        "State_Name": location_data["AdministrativeArea"]["ID"],
        "Zip_Code": location_data["PrimaryPostalCode"],
        "Longitude": location_data["GeoPosition"]["Longitude"],
        "Latitude": location_data["GeoPosition"]["Latitude"],
    }

    return res


def search_location_from_key(api_key, location_key):
    cities_url = "http://dataservice.accuweather.com/locations/v1/{0}?apikey={1}".format(
        location_key,
        api_key
    )
    with urllib.request.urlopen(cities_url) as url:
        cities = json.loads(url.read().decode())

    res = {
        "CityName": cities["EnglishName"],
        "State": cities["AdministrativeArea"]["ID"],
        "Country": cities["Country"]["EnglishName"],
        "Longitude": cities["GeoPosition"]["Longitude"],
        "Latitude": cities["GeoPosition"]["Latitude"]
    }

    return res

# Function to return current conditions
def current_conditions(api_key, location_key):
    curr_weather = "http://dataservice.accuweather.com/currentconditions/v1/{0}?apikey={1}&details=true".format(
        location_key,
        api_key
    )
    with urllib.request.urlopen(curr_weather) as url:
        current_data = json.loads(url.read().decode())[0]

    res = {
        "WeatherText": current_data["WeatherText"],
        "IsDay": current_data["IsDayTime"], # True
        "TempC": current_data["Temperature"]["Metric"]["Value"], # ºC
        "TempF": current_data["Temperature"]["Imperial"]["Value"], # ºF
        "Precipitation": current_data["PrecipitationSummary"]["Precipitation"]['Imperial']['Value'], # inch
        "Wind": current_data["Wind"]["Speed"]["Imperial"]["Value"], # mi/hr
        "Visibility": current_data["Visibility"]["Imperial"]["Value"], # mi
        "WebLink": current_data["Link"]
    }


    return res


def hourly_forecast(api, location_id):
    url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{0}?apikey={1}&details=true".format(
        location_id,
        api
    )
    with urllib.request.urlopen(url) as url:
        forecasts = json.loads(url.read().decode())

    res = {
        "TempC": [],
        "TempF": [],
        "Precipitation": [],
        "Wind": [],
        "Visibility": []
    }

    for f in forecasts:
        res["TempC"].append(round((f["Temperature"]["Value"] - 32) * 5/9, 1))
        res["TempF"].append(f["Temperature"]["Value"])
        res["Precipitation"].append(f["Rain"]['Value'])
        res["Wind"].append(f["Wind"]["Speed"]["Value"])
        res["Visibility"].append(f["Visibility"]["Value"])

    for k in res.keys():
        res[k] = round(sum(res[k])/len(res[k]), 1)

    return res
