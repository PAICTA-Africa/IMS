from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="my-app")

location = geolocator.geocode("me")
final = "{:.6f} {:.6f}".format(location.latitude, location.longitude)
print(final)

# time.sleep(5)

