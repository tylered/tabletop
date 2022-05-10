
import kivy
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown


from urllib.parse import urlencode, quote_plus

import googlemaps
import requests
from bs4 import BeautifulSoup

kivy.require('1.9.0')



Window.size = (300, 100)

res = ""
addy = ""

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



class DropBut(Button):
    def __init__(self, **kwargs):
        super(DropBut, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.text = "Restaurants"

        self.background_color = [1, 0.2, 0.07, 1]

        t = restaurant_search(restaurant_app.res, restaurant_app.addy)
        print(t)

        self.types = {str(location['name'] + " - " + location['formatted_address']):location['formatted_address'] for location in restaurant_list(restaurant_app.res, restaurant_app.addy)}

        print(self.types)

        for i in self.types.keys():
            btn = Button(text=i, size_hint_y=None, height=50, background_color = [1, 0.2, 0.07, 1])
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))


class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)


        self.window = Sample()
        self.window.cols = 1
        self.window.size_hint = (0.3, 0.3)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # logo
        logo = Image(source="logo.png")
        self.window.add_widget(logo)

        self.greeting = Label(text="Enter location (Format: street address, city, state or city, state):", color=[0, 0, 0, 1], font_name='Arial')
        self.window.add_widget(self.greeting)

        # user input
        self.user_loc = TextInput(multiline=False)
        self.window.add_widget(self.user_loc)

        self.restaurant = Label(text="Enter restaurant name or type:", color=[0, 0, 0, 1])
        self.window.add_widget(self.restaurant)

        self.user_restaurant = TextInput(multiline=False)
        # self.user_restaurant.bind(text=self.on_text)
        self.window.add_widget(self.user_restaurant)

        self.Button = Button(text="Enter", background_color=[1, 0.2, 0.07, 0.8])
        self.Button.bind(on_press=restaurant_app.callback)
        self.window.add_widget(self.Button)

        self.Button3 = Button(text="Quit", background_color=[1, 0.2, 0.07, 0.8])
        self.Button3.bind(on_press=restaurant_app.quit)
        self.window.add_widget(self.Button3)

        self.add_widget(self.window)

class ResList(Screen):
    def __init__(self, **kwargs):
        super(ResList, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.window2 = Sample()
        self.window2.cols = 1
        self.window2.size_hint = (0.3, 0.3)
        self.window2.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        logo1 = Image(source="logo.png")

        # logo
        self.window2.add_widget(logo1)

        new_text = ""
        self.greeting2 = Label(text="Choose a restaurant: ", color=[0, 0, 0, 1])
        self.window2.add_widget(self.greeting2)


        self.Button2 = Button(text="Find ratings", background_color=[1, 0.2, 0.07, 0.8])
        self.Button2.bind(on_press=restaurant_app.callback_rating)
        #self.window2.add_widget(self.Button2)

        self.Button4 = Button(text="Back to home", background_color=[1, 0.2, 0.07, 0.8])
        self.Button4.bind(on_press=restaurant_app.callback)
        # self.window2.add_widget(self.Button4)

        self.Button3 = Button(text="Quit", background_color=[1, 0.2, 0.07, 0.8])
        self.Button3.bind(on_press=restaurant_app.quit)
        # self.window2.add_widget(self.Button3)

        self.add_widget(self.window2)



class Window1(Screen):
    def __init__(self, **kwargs):
        super(Window1, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.window2 = Sample()
        self.window2.cols = 1
        self.window2.size_hint = (0.3, 0.3)
        self.window2.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        logo1 = Image(source="logo.png")

        # logo
        self.window2.add_widget(logo1)

        self.add_widget(self.window2)

class WindowManager(ScreenManager):
    pass

class Results(Screen):
    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.window2 = Sample()
        self.window2.cols = 1
        self.window2.size_hint = (0.3, 0.3)
        self.window2.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        logo1 = Image(source="logo3.png")

        # logo
        self.window2.add_widget(logo1)

        new_text = ""
        self.greeting2 = Label(text=new_text, color=[0, 0, 0, 1])
        self.window2.add_widget(self.greeting2)


        self.restaurant2 = Label(text=Home().user_restaurant.text,
                                 color=[0, 0, 0, 1])
        self.window2.add_widget(self.restaurant2)

        self.Button2 = Button(text="Confirm and search", background_color=[1, 0.2, 0.07, 0.8])
        self.Button2.bind(on_press=restaurant_app.callback_search)
        # self.window2.add_widget(self.Button2)

        self.Button4 = Button(text="Back to home", background_color=[1, 0.2, 0.07, 0.8])
        self.Button4.bind(on_press=restaurant_app.callback)
        # self.window2.add_widget(self.Button4)

        self.Button3 = Button(text="Quit", background_color=[1, 0.2, 0.07, 0.8])
        self.Button3.bind(on_press=restaurant_app.quit)
        # self.window2.add_widget(self.Button3)



        self.add_widget(self.window2)

class Sample(GridLayout):
    def __init__(self, **kwargs):
        super(Sample, self).__init__(**kwargs)

        with self.canvas.before:
            Rectangle(source='background.jpeg', pos=self.pos, size= [3600, 800])

class MyLayout(Widget):
    pass


class ButtonAnimation(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        self.bind(on_press=self.start_animation)

    def start_animation(self, *args):
        anim = Animation()
        anim.start(Window)

class DropList(Button):
    def __init__(self, **kwargs):
        super(DropList, self).__init__(**kwargs)
        self.drop = None
        self.drop = DropDown()

        types = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6']

        for i in types:
            btn = Button(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop.add_widget(btn)

        self.bind(on_release=self.drop.open)
        self.drop.bind(on_select=lambda instance, x: setattr(self, 'text', x))

class MyApp(App):

    def callback(self, event):
        self.res = self.home.user_restaurant.text
        self.addy = self.home.user_loc.text

        self.label_loc = Label(text="Location: " + self.addy, color=[0, 0, 0, 1])
        self.results.window2.add_widget(self.label_loc)

        self.label_res = Label(text="Restaurant: " + self.res, color=[0, 0, 0, 1])
        self.results.window2.add_widget(self.label_res)

        self.Button21 = Button(text="Confirm and search", background_color=[1, 0.2, 0.07, 0.8])
        self.Button21.bind(on_press=restaurant_app.callback_search)
        # self.window2.add_widget(self.Button2)

        self.Button41 = Button(text="Back to home", background_color=[1, 0.2, 0.07, 0.8])
        self.Button41.bind(on_press=restaurant_app.callback_menu)
        # self.window2.add_widget(self.Button4)

        self.Button31 = Button(text="Quit", background_color=[1, 0.2, 0.07, 0.8])
        self.Button31.bind(on_press=restaurant_app.quit)
        # self.window2.add_widget(self.Button3)

        self.results.window2.add_widget(self.Button21)
        self.results.window2.add_widget(self.Button41)
        self.results.window2.add_widget(self.Button31)
        self.sm.switch_to(self.results)

    def callback_rating(self, event):


        self.Rating = Label(text="Overall rating for {resty}:".format(resty=self.dropdown.text), color=[0, 0, 0, 1])


        the_rating, number_of_ratings, platform_list = ratings_return(self.dropdown.text, self.dropdown.types[self.dropdown.text])
        the_rating = str(the_rating)

        if number_of_ratings > 999:
            number_of_ratings = str(number_of_ratings)[0:-3] + "," +  str(number_of_ratings)[-3:]
        if number_of_ratings == 0:
            return "No ratings available"
        else:
            number_of_ratings = str(number_of_ratings)

            print(platform_list)

        for name in platform_list.keys():
            if name == "www.yelp.com":
                self.yelp = Label(text="Rating from Yelp: {value} based on {num_of_reviews} reviews.".format(value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.yelp)
            if name == "www.google.com":
                self.goog = Label(text="Rating from Google: {value} based on {num_of_reviews} reviews.".format(
                    value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.goog)
           # if name == "www.grubhub.com":
               # self.grub = Label(text="Rating from GrubHub: {value} based on {num_of_reviews} reviews.".format(
                   # value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
               # self.rating_window.window2.add_widget(self.grub)
            if name == "www.ubereats.com":
                self.uber = Label(text="Rating from UberEats: {value} based on {num_of_reviews} reviews.".format(
                    value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.uber)
           # if name == "www.tripadvisor.com":
            #   self.trip = Label(text="Rating from TripAdvisor: {value} based on {num_of_reviews} reviews.".format(
                   #  value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.trip)
            if name == "www.restaurantji.com":
                self.restji = Label(text="Rating from Restaurantji: {value} based on {num_of_reviews} reviews.".format(
                    value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.restji)
            if name == "www.restaurantguru.com":
                self.restguru = Label(text="Rating from RestaurantGuru: {value} based on {num_of_reviews} reviews.".format(
                    value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.restguru)
            if name == "www.doordash.com":
                self.dash = Label(text="Rating from RestaurantGuru: {value} based on {num_of_reviews} reviews.".format(
                    value=platform_list[name][0], num_of_reviews=platform_list[name][1]), color=[0, 0, 0, 1])
                self.rating_window.window2.add_widget(self.dash)

        # print(the_rating)

        self.display_rating = Label(text=the_rating[0:4] + "/5 stars based on " + number_of_ratings + " reviews", color=[0, 0, 0, 1])

        self.rating_window.window2.add_widget(self.Rating)
        self.rating_window.window2.add_widget(self.display_rating)

        self.Button43 = Button(text="Back to home", background_color=[1, 0.2, 0.07, 0.8])
        self.Button43.bind(on_press=restaurant_app.callback_menu)
        # self.window2.add_widget(self.Button4)

        self.Button33 = Button(text="Quit", background_color=[1, 0.2, 0.07, 0.8])
        self.Button33.bind(on_press=restaurant_app.quit)
        # self.window2.add_widget(self.Button3)

        self.Button5 = Button(text="Back to restaurant list", background_color=[1, 0.2, 0.07, 0.8])
        self.Button5.bind(on_press=restaurant_app.callback_list)

        try:
            self.rating_window.window2.remove_widget(self.Button5)
        except:
            pass

        self.rating_window.window2.add_widget(self.Button5)
        self.rating_window.window2.add_widget(self.Button43)
        self.rating_window.window2.add_widget(self.Button33)

        # self.sm.switch_to(self.results)

        self.sm.switch_to(self.rating_window)


    def callback_search(self, event):

        try:
            self.home.window.remove_widget(self.error)
        except:
            pass

        try:
            self.results.window2.remove_widget(self.Button21)
            self.results.window2.remove_widget(self.Button41)
            self.results.window2.remove_widget(self.Button31)

            self.results.window2.remove_widget(self.label_loc)
            self.results.window2.remove_widget(self.label_res)
        except:
            pass

        try:
            self.dropdown = DropBut()
            self.reslist.window2.add_widget(self.dropdown)

            self.Button22 = Button(text="Find ratings", background_color=[1, 0.2, 0.07, 0.8])
            self.Button22.bind(on_press=restaurant_app.callback_rating)
            # self.window2.add_widget(self.Button2)

            self.Button42 = Button(text="Back to home", background_color=[1, 0.2, 0.07, 0.8])
            self.Button42.bind(on_press=restaurant_app.callback_menu)
            # self.window2.add_widget(self.Button4)

            self.Button32 = Button(text="Quit", background_color=[1, 0.2, 0.07, 0.8])
            self.Button32.bind(on_press=restaurant_app.quit)
            self.reslist.window2.add_widget(self.Button22)
            self.reslist.window2.add_widget(self.Button42)
            self.reslist.window2.add_widget(self.Button32)
            self.sm.switch_to(self.reslist)
        except:

            # self.results.window2.remove_widget(self.restaurant2)
            self.results.window2.remove_widget(self.Button21)
            self.results.window2.remove_widget(self.Button41)
            self.results.window2.remove_widget(self.Button31)

            self.results.window2.remove_widget(self.label_loc)
            self.results.window2.remove_widget(self.label_res)

            self.error = Label(text="Error. Check for proper format or location.",
                           color=[255, 0, 0, 1])
            self.sm.switch_to(self.home)
            self.home.window.add_widget(self.error)



    def callback_menu(self, event):
        self.results.window2.remove_widget(self.Button31)
        self.results.window2.remove_widget(self.Button21)
        self.results.window2.remove_widget(self.Button41)
        self.results.window2.remove_widget(self.label_loc)
        self.results.window2.remove_widget(self.label_res)

        if (self.sm.current_screen == self.reslist):
            self.reslist.window2.remove_widget(self.Button22)
            self.reslist.window2.remove_widget(self.Button42)
            self.reslist.window2.remove_widget(self.Button32)

            self.reslist.window2.remove_widget(self.dropdown)

        if (self.sm.current_screen == self.rating_window):
            self.rating_window.window2.remove_widget(self.Rating)
            self.rating_window.window2.remove_widget(self.display_rating)
            self.rating_window.window2.remove_widget(self.Button43)
            self.rating_window.window2.remove_widget(self.Button33)
            self.rating_window.window2.remove_widget(self.Button5)

            self.reslist.window2.remove_widget(self.Button22)
            self.reslist.window2.remove_widget(self.Button42)
            self.reslist.window2.remove_widget(self.Button32)


            try:
                self.rating_window.window2.remove_widget(self.restguru)
            except:
                pass

            try:
                self.rating_window.window2.remove_widget(self.restji)
            except:
                pass
            try:
                self.rating_window.window2.remove_widget(self.goog)
            except:
                pass
            try:
                self.rating_window.window2.remove_widget(self.yelp)
            except:
                pass
            try:
                self.rating_window.window2.remove_widget(self.uber)
            except:
                pass
            try:
                self.rating_window.window2.remove_widget(self.uber)
            except:
                pass
            try:
                self.rating_window.window2.remove_widget(self.grub)
            except:
                pass
            try:
                self.rating_window.window2.remove_widget(self.trip)
            except:
                pass


            self.reslist.window2.remove_widget(self.dropdown)

        self.home.user_restaurant.text = ""
        self.home.user_loc.text = ""

        self.sm.switch_to(self.home)

    def callback_list(self, event):

        self.rating_window.window2.remove_widget(self.Rating)
        self.rating_window.window2.remove_widget(self.display_rating)
        self.rating_window.window2.remove_widget(self.Button43)
        self.rating_window.window2.remove_widget(self.Button33)
        self.rating_window.window2.remove_widget(self.Button5)


        try:
            self.rating_window.window2.remove_widget(self.restguru)
        except:
            pass

        try:
            self.rating_window.window2.remove_widget(self.restji)
        except:
            pass
        try:
            self.rating_window.window2.remove_widget(self.goog)
        except:
            pass
        try:
            self.rating_window.window2.remove_widget(self.yelp)
        except:
            pass
        try:
            self.rating_window.window2.remove_widget(self.uber)
        except:
            pass
        try:
            self.rating_window.window2.remove_widget(self.uber)
        except:
            pass

        self.sm.switch_to(self.reslist)


    def quit(self, event):
        self.stop()

    def build(self):
        Window.size = (600, 360)

        Window.clearcolor = (1, 1, 1, 1)

        # ------- second window


        # screen manager
        self.sm = ScreenManager()

        self.home = Home(name="home")
        self.sm.add_widget(self.home)

        self.results = Results(name="results")
        self.sm.add_widget(self.results)

        self.reslist = ResList(name="res_list")
        self.sm.add_widget(self.reslist)

        self.rating_window = Window1(name="rating")
        self.sm.add_widget(self.rating_window)

        return self.sm

#---- make it work

def restaurant_list(restaurant, address):
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

    def restaurant_search(restaurant, loc, key=key):
        restaurant_encoded = quote_plus(restaurant)
        # restaurant search
        url = f"""https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&input={restaurant_encoded}&inputtype=textquery&locationbias={loc}&key={key}"""
        url1 = f"""https://maps.googleapis.com/maps/api/place/textsearch/json?query={restaurant_encoded}&location={loc}&radius=2000&key={key}"""
        r1 = requests.get(url1).json()

        restaurant_dict = []
        restaurant_count = []

        for location in r1['results']:
            if location["business_status"] == "OPERATIONAL":
                if location['name'] not in restaurant_count.keys():
                    restaurant_count[location['name']] = 1
                else:
                    restaurant_count[location['name']] += 1

        for location in r1['results']:
            if location["business_status"] == "OPERATIONAL":
                if restaurant_count[location] > 1:
                    restaurant_dict.append((location['name'], location["formatted_address"]))
                else:
                    restaurant_dict.append(location['name'])

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

    return r1['results']
#---- make it work

def ratings_return(restaurant, address):
    query = restaurant + " " + address
    query = quote_plus(query)

    # google search parse
    response = requests.get(
        f'https://www.google.com/search?q={query}',
        headers=headers).text

    soup = BeautifulSoup(response, 'lxml')
    print(soup.prettify())

    # list of valid urls
    url_list = ["www.seamless.com", "www.yelp.com", "www.grubhub.com", "www.ubereats.com", "www.facebook.com",
                "www.doordash.com", "www.postmates.com", "www.restaurantji.com", "restaurantguru.com",
                "www.tripadvisor.com", "www.mapquest.com"]

    # find list of platforms
    restaurant_html = soup.find_all("div", class_="BNeawe UPmit AP7Wnd")
    restaurant_urls = ["www.google.com"]
    for url in restaurant_html:
        index = url.text.find(".com") + 4
        if url.text[0:index] in url_list:
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

                        # i'm changing this right here



                        new = l.text[1:cooma] + l.text[cooma + 1:-1]
                        review_list.append(int(new))
                        continue
                    review_list.append(int(l.text[1:-1]))

    # find all rating values
    rating_html = soup.find_all("span", class_="oqSTJd")
    ratings_list = []

    for l in rating_html:
        if "/" in l.text:
            if l.text[-2:-1] == 10:
                num = (float(l.text[0:2]) / 2)
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

    print("Weighted average:", weighted_average)
    print("Total number of ratings:", sum(review_list))
    return weighted_average, sum(review_list), restaurant_dict

def geocode(address):
    return maps.geocode(address)

def lat_lang(geocode_result):
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return lat, lng

def address_enocde(loc):
    lat, lng = lat_lang(geocode(loc))
    loc = "radius=2000&" + str(lat) + "," + str(lng)
    loc1 = str(lat) + "," + str(lng)
    loc = quote_plus(loc)
    loc1_encode = quote_plus(loc1)
    return loc1

def restaurant_search(restaurant, loc):
    address_encoded = address_enocde(loc)
    restaurant_encoded = quote_plus(restaurant)
    # restaurant search
    url = f"""https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&input={restaurant_encoded}&inputtype=textquery&locationbias={loc}&key={key}"""
    url1 = f"""https://maps.googleapis.com/maps/api/place/textsearch/json?query={restaurant_encoded}&location={address_encoded}&radius=2000&key={key}"""
    r1 = requests.get(url1).json()

    restaurant_dict = []

    for location in r1['results']:
        if location["business_status"] == "OPERATIONAL":
            print(location)
            restaurant_dict.append(location['name'])

    print(restaurant_dict)

    return restaurant_dict


if __name__ == '__main__':
    restaurant_app = MyApp()
    restaurant_app.run()

