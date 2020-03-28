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


class BlogReader:


    def __init__(self, station, language, gender="female", accent=None, strict_gender=False, \
            strict_accent=False, sample_rate=8000, audio_format='mp3', metadata=True, time_frame_count=2):
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
        self.time_frame_count = time_frame_count
        # self.generate_forecast_string()
        # if self.forecast_string is not None:
        #     self.generate_forecast_audio()


	def get_content(self, url, number_of_entries):
	    response = requests.get(url)
	    doc = Document(response.text)
	    summary = doc.summary(html_partial=True)
	    summary = summary.encode('UTF-8')
	    entry_list = summary.split('<div class="sf-content-block content-block">')
	    root = etree.fromstring(summary)
	    count = 0
	    for child in root: 
	    	while count < number_of_entries:
		        # find all identified 'posts' (content blocks)   
		        if child.attrib["class"] == "sf-content-block content-block":
		            # go through each element in the content section and add trailing whitespace to ensure proper spacing when combined
		            for element in child.iter():
		                if (element.text): element.text = element.text + " "
		            post = child.xpath("string()").encode('UTF-8')
		            print(post)
		            # get fname
		            # utils.get_cprc_tts(post, self.fname,  sample_rate = self.sample_rate, accent=self.accent)
		            count += 1