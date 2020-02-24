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
import glob


def generate_audio(text_string, file_name, language, gender="female", accent=None, strict_gender=False, \
            strict_accent=False, sample_rate=8000, audio_format='wav', metadata=True):
	forecast_audio = utils.get_cprc_tts_iter(text_string, file_name, language, gender, accent, strict_gender, 
		strict_accent, sample_rate, audio_format, metadata)


def iter_files(path, language, gender, accent, strict_gender, \
                strict_accent, sample_rate, audio_format, metadata):
	print(language)
	os.chdir(path)
	text_strings = glob.glob('*.txt')
	for  text_string in text_strings:
		t = open(text_string, 'r')
		text_for_audio = t.read()
		generate_audio(text_for_audio, text_string, language)
