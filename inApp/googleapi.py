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
def giveExtraTime(time):
    newStr = ""
    output = ""
    if len(time) == 7:
        hours = 0
        newStr += time[0]
        newStr += time[1]
        for i in range(2,len(time),1):
            output += time[i]
        x = int(newStr) + 60
        finalOutput = str(x) + output
        if x > 60:
            while x > 60:
                x += -60
                hours += 1 
            if hours == 1:
                x = (str(hours) + " hour " + str(x))
            if hours > 1:
                x = (str(hours) + " hours " + str(x))
            finalOutput = x + output
        return finalOutput
    if len(time) == 14:
        newStr += time[0]
        for i in range(1,len(time),1):
            output += time[i]
        x = int(newStr) + 1
        finalOutput = str(x) + output
        print(str(x) + output)
        return finalOutput

x = giveExtraTime(time)
print("\nThe total travel time from home to work is", x)