import requests
import smtplib

api_file = open("api-key.txt", "r")
api_key = api_file.read()
api_file.close()
#start point
home = input("Enter a home address\n")

#end point
work = input("Enter a work address\n")

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

r = requests.get(url + "origins=" + home + "&destinations=" + work + "&key=" + api_key)

time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
seconds = r.json()["rows"]



print("\nThe total travel time from home to work is", time)