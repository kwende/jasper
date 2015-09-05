import re
import urllib2
import libxml2

WORDS = ["WEATHER", "TOMORROW"]

def isValid(text):
	if "WEATHER" in text and ("TOMORROW" in text or "TODAY" in text):
		return True

def handle(text, mic, profile):
	mic.say("Give me a second sir, I'm checking online")
	response = urllib2.urlopen('http://forecast.weather.gov/MapClick.php?lat=40.7844&lon=-96.655&unit=0&lg=english&FcstType=dwml')
	data = response.read()
	doc = libxml2.parseDoc(data)

	xpathStuff = doc.xpathNewContext()

	if "TODAY" in text:
		result = xpathStuff.xpathEval('//wordedForecast/text[1]')
		mic.say(result[0].content)
	else if "TOMORROW" in text:
		result = xpathStuff.xpathEval('//wordedForecast/text[2]')
		mic.say(result[0].content)
	else
		mic.say("Sorry, all you've taught me so far is about weather today and tomorrow.")
