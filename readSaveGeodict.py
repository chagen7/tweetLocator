import json

# If file 'geodict.json' exists in the current folder,
# reads the JSON-formatted geocoding information from the file
# and "loads" it into a Python dictionary, geoDict.
# 
# If 'geodict.json' does not already exist, global variable geoDict is set
# to an empty dictionary.

# 
def readGeoDict():
   global geoDict
   try:
      dictInFile = open('geodict.json')
   except:
      dictInFile = None
   if dictInFile != None:
      jsonString = dictInFile.read()
      geoDict = json.loads(jsonString)
      dictInFile.close()
   else:
      geoDict = {}

# Converts the dictionary with saved geocode information, geoDict,
# into JSON format and writes it to file 'geodict.json'
# 
def saveGeoDict():
   global jsonString
   print('saving geodict.json')
   dictOutFile = open('geodict.json', 'w')
   jsonString = json.dumps(geoDict)
   dictOutFile.write(jsonString)
   dictOutFile.close()
