# -*- coding: UTF-8 -*
import time
import datetime
import argparse
from news.blog_reader import BlogReader
import utils.utils as utils
import requests
from bs4 import BeautifulSoup
from readability import Document
from random import randrange
from lxml import etree




# blogReader = BlogReader(args.station, args.language, args.gender, args.accent, args.strict_gender, \
#                 args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.time_frame_count)
blogReader = BlogReader('cc', 'English')
blogReader.get_content('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/events-as-they-happen', 1)



# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on yr.no')
#     parser.add_argument('station', type=str, help='station location code (cu, ma)')
#     parser.add_argument('language', type=str, help='language')
#     parser.add_argument('-g', '--gender', type=str, default='female', help='Preferred gender of speaker)')
#     parser.add_argument('-a', '--accent', type=str, default=None, help='Preferred gender of speaker)')
#     parser.add_argument('-sg', '--strict_gender', default=False, type=str, help='is preferred gender strict?')
#     parser.add_argument('-sa', '--strict_accent', default=False, type=str, help='is preferred accent strict?')
#     parser.add_argument('-sr', '--sample_rate', default=8000, type=int, help='sample rate')
#     parser.add_argument('-af', '--audio_format', default='mp3', type=str, help='audio format')
#     parser.add_argument('-m', '--metadata', default=True, type=str, help='metadata true or false')
#     parser.add_argument('-t', '--time_frame_count', default=2, type=int, help='number of time frames to forecast')


#     args = parser.parse_args()

#     monitor(args)