# -*- coding: UTF-8 -*
import os
import requests
import datetime
from cereproc.cerecloud_rest import CereprocRestAgent
from suds.client import Client
import ConfigParser
import pytz
from bs4 import BeautifulSoup


def get_cprc_tts(text, fpath="", language='english', gender='female',  accent=None, strict_gender=False, \
				 strict_accent=False, sample_rate='8000', audio_format='mp3', metadata=True):
		if os.path.exists(os.path.dirname(fpath)) is False:
			os.mkdir(os.path.dirname(fpath))
		# config = configparser.ConfigParser()
		# config.read('config.ini')
		# username = config['cerecloud']['CEREPROC_USERNAME']
		# password = config['cerecloud']['CEREPROC_PASSWORD']
		username = "5aec2e36c429d"
		password = "VkZmL42e5L"
		print(fpath)
		restAgent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", username, password, gender, language)
		voice = restAgent._choose_voice(language, gender, accent, strict_gender, strict_accent)
		url, transcript = restAgent.get_cprc_tts(text, voice, sample_rate, audio_format, metadata)
		r = requests.get(url)
		with open(fpath + "." + audio_format, 'wb') as f:
				f.write(r.content)
		with open(fpath + ".txt", 'wb') as f:
				f.write(text)


def getLXML(feed):
		try:
			response = requests.get(feed)
		except Exception as e:
			print("Error with url: {0}".format(str(e)))
			return None
		response = response.content
		HTMLFeed = BeautifulSoup(response, 'lxml')
		return HTMLFeed


def get_local_time(time_zone):
	tz = pytz.timezone(time_zone)
	local_time = datetime.datetime.now(tz)
	return(local_time, tz)


def get_day_part(time_zone):
	tz = pytz.timezone(time_zone)
	local_time = datetime.datetime.now(tz)
	if local_time.hour < 5:
		return 3
	elif local_time.hour < 11:
	    return 0
	elif 11 <= local_time.hour < 17:
	    return 1
	else:
	    return 2


def next_index_loop(items, idx):
	if idx >= len(items)-1:
		return(0)
	else:
		return(idx+1)


# Convert time string of a specific formate to time object, return 
def get_time(time_string):
    time = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    return(time.strftime("%H:%M"))