import geocoder
import gmaps.datasets
from geopy.geocoders import Nominatim
import requests, json





class map():
    api_key = "AIzaSyCQKcBfUp_IbSpgy-GpPHl0F3fDOSYtGvQ"
    url = "https://maps.googleapis.com/maps/api/staticmap?"

    def __init__(self, username):
        self.username = username
        self.center = "iowa city"
        self.lat = 41.661129
        self.lng = -91.530167

    def getMapUrl(self, lat, lng, zoom=13, mapType="roadmap", api=api_key):

        urlbase = "http://maps.google.com/maps/api/staticmap?"
        args = "&center={},{}&zoom={}&size={}x{}&maptype={}&markers=color:red%7Clabel:S%7C{},{}".format(lat, lng, zoom,
                                                                                                        800, 800,
                                                                                                        mapType, lat,
                                                                                                        lng)
        # newone="center={},{}&zoom={}&size={}x{}&maptype={}".format(lat,lng,zoom,800, 800, mapType)
        car = "&markers=color:blue%7Clabel:S%7C{},{}".format(str(41.669129), str(-91.537167))

        return urlbase + "&maptype=roadmap&key=" + api + args + car

    def set_des(self, lat, lng):
        des = "&markers=color:blue%7Clabel:S%7C{},{}".format(str(lat), str(lng))
        return des

    def des(self, olat, olng, dlat, dlng):
        a = self.getMapUrl(olat, olng) + self.set_des(dlat, dlng)
        return a

    def getlocationmyself(self):

        send_url = "http://api.ipstack.com/check?access_key=5f65c6c7cf2aa79e40dd1c20b1dc127a"
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        # print(lat)
        # print(lon)
        print(r.text)

        return (lat, lon)
        #return j

    def getlocationdes(self, location):

        address = str(location)
        geolocator = Nominatim(user_agent="zhangbohan039@gmail.com")
        location = geolocator.geocode(address)
        # print(location.address)
        # print((location.latitude, location.longitude))

        return (location.latitude, location.longitude)

    def mapinfo(self, source, des, api=api_key):
        i = 0
        ns = ""
        while (i < len(source)):

            if (source[i] == " "):
                ns += "+"
            else:
                ns += source[i]
            i += 1
        print(ns)
        ds = ""
        i = 0;
        while (i < len(des)):

            if (des[i] == " "):
                ds += "+"
            else:
                ds += des[i]
            i += 1
        #print(des)

        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        u = url + 'origins=' + ns + '&destinations=' + ds + '&key=' + api

        r = requests.get(url + 'origins=' + ns + '&destinations=' + ds + '&key=' + api)
        #print(u)
        print(r.text)
        return r.json()




gmaps.configure(api_key="AIzaSyCQKcBfUp_IbSpgy-GpPHl0F3fDOSYtGvQ")

# print(g.latlng)
# a = map("a")
# print(a.getMapUrl(a.lat,a.lng))
# a.getlocationdes("chicago")
# a.mapinfo("iowa city","chicago")
#
#print(a.des(41.8755616, -87.6244212,41.0755616, -87.0244212))
a = map("a")
# print(a.getlocationdes("the University of Iowa"))
print(a.getlocationmyself()[0])
print(a.getlocationmyself()[1])
print(a.getlocationmyself()[0],a.getlocationmyself()[1])
location=('%s , %s')%(a.getlocationmyself()[0] ,a.getlocationmyself()[1])
print('***')
# print(location)
print(a.mapinfo(str(location),"Catlett"))


# j=a.mapinfo("350 N Madison St, Iowa City, IA 52242","university of iowa")
# print(j)

# j=a.mapinfo("41.903289794921875, -87.66058349609375","350 N Madision st iowa city")

# print(j['rows'][0].get('elements')[0].get('distance').get('text'))
# print(j['rows'][0].get('elements')[0].get('duration').get('text'))
