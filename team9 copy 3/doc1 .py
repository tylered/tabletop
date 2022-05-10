import geopy.geocoders
import gmaps
import json
from urllib.parse import urlencode, quote_plus
# import pgeocode
from geopy.geocoders import Nominatim
import googlemaps
import requests
from bs4 import BeautifulSoup
import lxml

headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    # api key
key = "AIzaSyC_cqV4iujjvKWCEBHmrLIZszE7CRwTL0I"

    # engine
engine_id = "71fdf0e83dd55e919"
engine_key = "AIzaSyC_cqV4iujjvKWCEBHmrLIZszE7CRwTL0I"

    # find address's longitude and latitude

maps = googlemaps.Client(key)


def controller(restaurant, address):
    key = "AIzaSyC_cqV4iujjvKWCEBHmrLIZszE7CRwTL0I"

    def geocode(address):
        return maps.geocode(address)


    geocode_result = maps.geocode(address)


    def lat_lang(geocode_result):
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng

    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    def address_enocde(loc):
        loc = "radius=2000&" + str(lat) + "," + str(lng)
        loc1 = str(lat) + "," + str(lng)
        loc = quote_plus(loc)
        loc1_encode = quote_plus(loc1)
        return loc1_encode


    # address encode
    loc = "radius=2000&" + str(lat) + "," + str(lng)
    loc1 = str(lat) + "," + str(lng)
    loc = quote_plus(loc)
    loc1_encode = quote_plus(loc1)


    def restaurant_search(restaurant, loc):
        restaurant_encoded = quote_plus(restaurant)
        # restaurant search
        url = f"""https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&input={restaurant_encoded}&inputtype=textquery&locationbias={loc}&key={key}"""
        url1 = f"""https://maps.googleapis.com/maps/api/place/textsearch/json?query={restaurant_encoded}&location={loc1}&radius=2000&key={key}"""
        r1 = requests.get(url1).json()

        restaurant_dict = []

        for location in r1['results']:
            if location["business_status"] == "OPERATIONAL":
                print(location)
                restaurant_dict.append(location['name'], location['formatted_address'])

        return restaurant_dict


    # restaurant input & encode
    restaurant_encoded = quote_plus(restaurant)

    # restaurant search
    url = f"""https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&input={restaurant_encoded}&inputtype=textquery&locationbias={loc}&key={key}"""

    # restaurant results
    url1 = f"""https://maps.googleapis.com/maps/api/place/textsearch/json?query={restaurant_encoded}&location={loc1}&radius=2000&key={key}"""

    r1 = requests.get(url1).json()

    for location in r1['results']:
        if location["business_status"] == "OPERATIONAL":
            print(location['name'], location["formatted_address"])

    # let user pick restaurant
    user_choice = int(input("Enter your option (1, 2, 3): "))
    desired_restaurant = r1['results'][user_choice - 1]
    print(desired_restaurant["name"])
    ind = desired_restaurant["name"].index("Restaurant")
    name = desired_restaurant["name"][0:ind - 1]
    print(name)



    # the search query you want

    def restaurant_query(restaurant):
        query = name + " " + desired_restaurant['formatted_address']
        query = quote_plus(query)
        response = requests.get(
            f'https://www.google.com/search?q={query}',
            headers=headers).text

    query = name + " " + desired_restaurant['formatted_address']
    query = quote_plus(query)

    # google search parse
    response = requests.get(
        f'https://www.google.com/search?q={query}',
        headers=headers).text

    soup = BeautifulSoup(response, 'lxml')
    # print(soup.prettify())

    # list of valid urls
    url_list = ["www.seamless.com", "www.yelp.com", "www.grubhub.com", "www.ubereats.com", "www.facebook.com",
                "www.doordash.com", "www.postmates.com", "www.restaurantji.com", "restaurantguru.com", "www.tripadvisor.com", "www.mapquest.com"]

    # find list of platforms
    restaurant_html = soup.find_all("div", class_="BNeawe UPmit AP7Wnd")
    restaurant_urls = ["www.google.com"]
    for url in restaurant_html:
        index = url.text.find(".com") + 4
        if url.text[0:index] in url_list:
            print(url)
            restaurant_urls.append(url.text[0:index])


    # find number of ratings for each platform
    review_html = soup.find_all("span", class_=None)

    review_list = []

    for l in review_html:
        if "(" in l.text:
            if "-" not in l.text:
                if "." not in l.text and ":" not in l.text and not any(letter.isalpha() for letter in l.text):
                    if "," in l.text:
                        cooma = l.text.index(",")
                        new = l.text[1:cooma] + l.text[cooma + 1:-1]
                        review_list.append( int(new ) )
                        continue
                    review_list.append(int(l.text[1:-1]))

    # find all rating values
    rating_html = soup.find_all("span", class_="oqSTJd")
    ratings_list = []

    for l in rating_html:
        if "/" in l.text:
            if l.text[-2:-1] == 10:
                num = ( float(l.text[0:2]) / 2 )
                print(num)
                ratings_list.append(float(l.text))
            if l.text[-2:-1] == 5:
                num = float(l.text[0:2])
                print(num)
                ratings_list.append(float(l.text))
            continue
        ratings_list.append(float(l.text))

    # for l, r in zip(review_list, ratings_list):
        # print(l, r)


    # dictionary of restaurants with rating and number of reviews
    restaurant_dict = {key: value for key, value in zip(restaurant_urls, zip(ratings_list, review_list))}

    for key, value in restaurant_dict.items():
        print("Platform:", key)
        print("Rating:", value[0])
        print("Number of reviews:d", value[1])


    # calculate ratings
    sum_of_ratings = sum(review_list)
    weighted_average = 0
    for x, r in zip(review_list, ratings_list):
        weighted_average += (x / sum_of_ratings) * r

    print("Weighted average:")
    return weighted_average
# print(review_list, ratings_list)

user_rest = input("Enter a restaurant or restaurant type: ")
user_loc = input("Enter a location (format: City, State or Street Address, City, State): ")


print(restaurant_search(user_rest, user_loc))


