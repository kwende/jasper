import re
import urllib2
import libxml2
import random

WORDS = ["WEATHER", "TOMORROW"]

def isValid(text):
	if ("WEATHER" in text and ("TOMORROW" in text or "TODAY" in text)) or "TEMPERATURE" in text:
		return True

def handle(text, mic, profile):
	responses = ["Give me a second to check online", "Checking", "Hold on while I look that up", "One second, please"]

	response = random.choice(responses)

	mic.say(response)
	response = urllib2.urlopen('http://forecast.weather.gov/MapClick.php?lat=40.7844&lon=-96.655&unit=0&lg=english&FcstType=dwml')
	data = response.read()
	doc = libxml2.parseDoc(data)

	xpathStuff = doc.xpathNewContext()

	if "TODAY" in text:
		result = xpathStuff.xpathEval('//wordedForecast/text[1]')
		mic.say(result[0].content)
	elif "TOMORROW" in text:
		result = xpathStuff.xpathEval('//wordedForecast/text[2]')
		mic.say(result[0].content)
	elif "TEMPERATURE" in text:
		result = xpathStuff.xpathEval("//data[@type='current observations']/parameters/temperature[1]/value")
		tempValue = result[0].content
		result = xpathStuff.xpathEval("//data[@type='current observations']/parameters/temperature[2]/value")
		dewPoint = result[0].content
		mic.say("The current temperature is " + tempValue + " degrees with a dewpoint of " + dewPoint + " degrees.")
	else:
		mic.say("Sorry, all you've taught me so far is about weather today and tomorrow.")
