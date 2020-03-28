# -*- coding: UTF-8 -*
import requests
import argparse
import datetime
import utils.utils as utils
import json
from xml.etree import ElementTree as ET
from lxml import etree, html
import pytz
import csv
import sys
import os
from readability import Document

class BlogReader:

	def __init__(self, station, language, gender="female", accent=None, strict_gender=False, \
            strict_accent=False, sample_rate=8000, audio_format='mp3', metadata=True):
        # !! rootio has this as db entry, with set codes?
		self.stations = {"sg":"Sfântu Gheorghe", "vv":"Vourvourou", "cu":"Curral das Freiras"}
		self.station = station
		self.language = language
		self.accent = accent
		self.gender = gender
		self.strict_gender = strict_gender
		self.strict_accent = strict_accent
		self.sample_rate = sample_rate
		self.audio_format = audio_format
		self.metadata = metadata
		self.run_time = datetime.datetime.now(pytz.timezone('GMT')).strftime("%Y-%m-%d-%H%m%s")

# self.generate_forecast_string()
        # if self.forecast_string is not None:
        #     self.generate_forecast_audio()
	def get_content(self, url, number_of_entries, name):
		self.name = name
		response = requests.get(url)
		doc = Document(response.text)
		summary = doc.summary(html_partial=True)
		summary = summary.encode('UTF-8')
		entry_list = summary.split('<div class="sf-content-block content-block">')
		root = etree.fromstring(summary)
		count = 0
		print(len(root))
		for child in root: 
			# access identified 'posts' (content blocks)   
			if child.attrib["class"] == "sf-content-block content-block":
	            # go through each element in the post and add trailing whitespace to ensure proper spacing when text combined
				for element in child.iter():
					if (element.text): element.text = element.text + " "
				post = child.xpath("string()").encode('UTF-8')
				print(post)
				file_name = self.get_file_name(count)
				print(file_name)
	            # utils.get_cprc_tts(post, file_name,  sample_rate = self.sample_rate, accent=self.accent)
				count += 1
				if count>=number_of_entries | count>=len(root):
					break


	def get_file_name(self, count):
		# GTC datetime, source, post number
		filename =  self.run_time + "_" + self.name + "_" + str(count)
		return filename