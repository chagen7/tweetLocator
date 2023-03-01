import tkinter
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json
import geocodeonly

GOOGLEAPIKEY = "AIzaSyDcHH6Xgo2ERPim8n2IoTOUNKQavZKWxx0"

class Globals:
   
   rootWindow = None
   mapLabel = None
   locationEntry = None
   keywordEntry = None
   choiceVar = None
   zoomLabel = None

   defaultLocation = "Mauna Kea, Hawaii"
   mapLocation = defaultLocation
   mapFileName = 'googlemap.gif'
   mapSize = 400
   zoomLevel = 9
   geoDict = {}
   selectedButtonText = "one"
   mapType = "terrain"

APIKey = "MFMqRHPgj2CL1FJJ9p37bDYAJ"
APISecretKey = "38S2x6uasYPCLatM4vkeZ3KMuYwFYIgqpwGDAWS1b0clA1jg63"
bearerToken = "AAAAAAAAAAAAAAAAAAAAANPRKQEAAAAA7H1137aS%2FwOiab3%2FDEhyxpacvJE%3DOxSpLzMH6YH48ZEeNNCQb0QnvnvvXnW8WS0GcjihvtrRxD0skZ"
#request = curl -X GET -H "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAANPRKQEAAAAA7H1137aS%2FwOiab3%2FDEhyxpacvJE%3DOxSpLzMH6YH48ZEeNNCQb0QnvnvvXnW8WS0GcjihvtrRxD0skZ" "https://api.twitter.com/2/tweets/20"

def authTwitter():
    global client
    client = OAuth1(API_KEY, API_SECRET,
                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def geocodeAddress(addressString):
   global geoURL
   global jsonResult
   if addressString in Globals.geoDict:
      return Globals.geoDict[addressString]
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   geoURL = urlbase + quote_plus(addressString)
   geoURL = geoURL + "&key=" + GOOGLEAPIKEY

   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      result = (0.0, 0.0) # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
   else:
      loc = jsonResult['results'][0]['geometry']['location']
      result = (float(loc['lat']),float(loc['lng']))
      Globals.geoDict[addressString]=result
   return result

def getMapUrl():
   lat, lng = geocodeAddress(Globals.mapLocation)
   urlbase = "http://maps.google.com/maps/api/staticmap?"
   args = "center={},{}&zoom={}&size={}x{}&maptype={}".format(lat,lng,Globals.zoomLevel,Globals.mapSize,Globals.mapSize, Globals.mapType)
   #args = args + "&markers=color:blue%7Clabel:S%7C{},{}".format(str(lat),str(lng))
   args = args + "&key=" + GOOGLEAPIKEY
   mapURL = urlbase + args
   return mapURL

def retrieveMapFromGoogle():
   url = getMapUrl()
   urlretrieve(url, Globals.mapFileName)

def displayMap():
   retrieveMapFromGoogle()    
   mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
   Globals.mapLabel.configure(image=mapImage)
   # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
   Globals.mapLabel.mapImage = mapImage
   
def readEntriesSearchTwitterAndDisplayMap():
   Globals.mapLocation = Globals.locationEntry.get()
   Globals.keywordEntry.get()
   displayMap()

def handleCloseRootWindow():
   rootWindow.destroy()
   geocodeonly.saveGeoDict()

def radioButtonChosen():
   if Globals.choiceVar.get() == 1:
      Globals.selectedButtonText = "one"
      Globals.mapType = "terrain"
      displayMap()
   elif Globals.choiceVar.get() == 2:
      Globals.selectedButtonText = "two"
      Globals.mapType = "roadmap"
      displayMap()
   elif Globals.choiceVar.get() == 3:
      Globals.selectedButtonText = "three"
      Globals.mapType = "satellite"
      displayMap()
   elif Globals.choiceVar.get() == 4:
      Globals.selectedButtonText = "four"
      Globals.mapType = "hybrid"
      displayMap()

def increaseBy1():
   Globals.zoomLevel = Globals.zoomLevel + 1
   Globals.zoomLabel.config(text="Zoom: {}".format(Globals.zoomLevel))
   displayMap()

def decreaseBy1():
   if Globals.zoomLevel > 0:
      Globals.zoomLevel = Globals.zoomLevel - 1
      Globals.zoomLabel.config(text="Zoom: {}".format(Globals.zoomLevel))
      displayMap()

def initializeEngine():
    Globals.rootWindow = tkinter.Tk()
    Globals.rootWindow.protocol("WM_DELETE_WINDOW",handleCloseRootWindow)
    Globals.rootWindow.title("HW10")

    Globals.choiceVar = tkinter.IntVar()
    Globals.choiceVar.set(1)

    mainFrame = tkinter.Frame(Globals.rootWindow) 
    mainFrame.pack()

    geocodeonly.readGeoDict()

    label = tkinter.Label(mainFrame, text="Enter the location (first box) and/or keyword (second box):")
    label.pack()
    Globals.locationEntry = tkinter.Entry(mainFrame)
    Globals.locationEntry.pack()
    Globals.keywordEntry = tkinter.Entry(mainFrame)
    Globals.keywordEntry.pack()
    button = tkinter.Button(mainFrame, text="Search", command=readEntriesSearchTwitterAndDisplayMap)
    button.pack()

    Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
    Globals.mapLabel.pack()

    Globals.zoomLabel = tkinter.Label(mainFrame, text="Zoom: {}".format(Globals.zoomLevel))
    Globals.zoomLabel.pack()
    increaseButton = tkinter.Button(mainFrame, text="+", command=increaseBy1)
    increaseButton.pack()
    decreaseButton = tkinter.Button(mainFrame, text="-", command=decreaseBy1)
    decreaseButton.pack()

    r1 = tkinter.Radiobutton(mainFrame, text="Terrain map", variable=Globals.choiceVar, value=1, command=radioButtonChosen)
    r1.pack()
    r2 = tkinter.Radiobutton(mainFrame, text="Road map", variable=Globals.choiceVar, value=2, command=radioButtonChosen)
    r2.pack()
    r3 = tkinter.Radiobutton(mainFrame, text="Satellite map", variable=Globals.choiceVar, value=3, command=radioButtonChosen)
    r3.pack()
    r4 = tkinter.Radiobutton(mainFrame, text="Hybrid map", variable=Globals.choiceVar, value=4, command=radioButtonChosen)
    r4.pack()

def TweetLocator():
    initializeEngine()
    displayMap()
    Globals.rootWindow.mainloop()
