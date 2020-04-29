"""Random events"""
import random
import requests
from flask import request

# -----------------------------DATA---------------------------------- #
rank_no = [x for x in range(1, 99)]
names = ["Liam", "Oliv", "Alex", "Luc", "Seba",
         "Jac", "Ben", "Jack", "Cart", "Dyl"]
types = ["Login", "Logout", "Purchase", "Sale"]
ids = [x for x in range(100)]
device = ["Desktop", "Laptop", "Mobile", "Tablet"]
os_version = ["Windows", "Ubuntu", "MacOS", "Fedora", "ChromeOS",
              "Android", "Windows", "iOS", "KaiOS", "Symbian"]
purchase_data = [x for x in range(9, 9999)]
sale_data = [x for x in range(9, 9999)]


# -----------------------------GEO----------------------------------- #
def get_location(location):
    try:
        response = requests.get("http://ip-api.com/json/")
        json_data = response.json()
        return json_data
    except Exception as e:
        return "Don't found location!"


def get_data():
    location = request.remote_addr
    data = get_location(location)
    data = {
        "country": data["country"],
        "city": data["city"],
        "lat": data["lat"],
        "lon": data["lon"],
        "timezone": data["timezone"],
        "query": data["query"],
    }
    return data


# ---------------------Events_data----------------------------------- #
def random_data(list_, n=1):
    result = random.sample(list_, n)
    if n == 1:
        return result[0]
    return result


def generate_buzz():
    username = random_data(names) + str(random_data(ids, 1))
    r_data = ' '.join(
        [
            str(random_data(rank_no, 1)),
            username,
            random_data(types),
            random_data(device),
            random_data(os_version),
            str(random_data(purchase_data, 1)) + "$",
            str(random_data(sale_data, 1)) + "$"
         ]
    )
    return r_data.split(" ")
