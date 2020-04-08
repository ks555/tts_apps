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

sys.path.append(os.path.dirname(os.path.dirname(__file__)))



class YrForecast:


    def __init__(self, station, language, gender="female", accent=None, strict_gender=False, \
            strict_accent=False, sample_rate=8000, audio_format='mp3', metadata=True, time_frame_count=2):
        # !! rootio has this as db entry, with set codes?
        self.stations = {"sg":"Sfântu Gheorghe", "vv":"Vourvourou", "cu":"Curral das Freiras", "be":"Bere Island"}
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
        self.generate_forecast_string()
        if self.forecast_string is not None:
            self.generate_forecast_audio()
            self.update_xml()


    def generate_forecast_string(self):
        self.set_yr_URL()
        self.bs = utils.getLXML(self.url)
        self.request_current_weather()


    def generate_forecast_audio(self):
        self.fpath = "weather/audio/" + self.station + "/" + self.get_file_name()
        self.forecast_audio = utils.get_cprc_tts(self.forecast_string, self.fpath, self.language, self.gender, self.accent, self.strict_gender, \
            self.strict_accent, self.sample_rate, self.audio_format, self.metadata)


    def request_current_weather(self):
        try:
            self.tz = self.bs.timezone["id"]
            self.day_part_idx = utils.get_day_part(self.tz)
            self.set_last_update(self.bs.find("lastupdate"))
            time_frames = self.bs.find_all("time")
            temperature = []
            wind_direction = []
            wind_speed = []
            percipitation = []
            weather = []
            forecast_time = []
            for i in range(0,self.time_frame_count):
                forecast_time.append(utils.get_time(time_frames[i]['from']))
                forecast_time.append(utils.get_time(time_frames[i]['to']))
                temperature.append(time_frames[i].temperature['value'])
                wind_direction.append(self.translate(time_frames[i].winddirection['code'], "direction"))
                wind_speed.append(time_frames[i].windspeed['mps'])
                percipitation.append(time_frames[i].precipitation['value'])
                weather.append(self.translate(time_frames[i].symbol['number'], "weather"))

            self.set_forecast_string(i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather)
        except Exception as e:
            print("Error with lxml parsing: {0}".format(str(e)))
            self.forecast_string = None

    def set_forecast_string(self, i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather):
        if self.language == "portuguese":
    		self.forecast_string = "Bom dia, são " + time + " este é o tempo para o Curral das Freiras nesta linda manhã " + date + " " + \
            todayDayPart + "," + todaySummary + " a temperatura atual é " + currentTemperture + " será sentido ao longo do dia uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  " espero que continuem connosco. Tenha uma boa manhã."
            
 
        elif self.language == "romanian":
            day_parts = [["dimineaţă","după amiază","astă seară", "la noapte"],["Buna Dimineata","Buna ziua","Bună seara", "Bună seara"]]
            next_part_idx = utils.next_index_loop(day_parts[0], self.day_part_idx)
            # Romaninan Cereproc voice does not say 'ora' when reading time, it needs to be added in the script.
            # howeverm 00:00 is read as midnight, so the ora does not make sense. Thus, converting 00:00 to 24
            forecast_time_0 = forecast_time[0].replace("00:00", "24")
            forecast_time_1 = forecast_time[1].replace("00:00", "24")
            forecast_time_2 = forecast_time[2].replace("00:00", "24")
            forecast_time_3 = forecast_time[3].replace("00:00", "24")

            self.forecast_string = day_parts[1][self.day_part_idx] + " " + self.stations[self.station] + ". Prognoza de " + \
                day_parts[0][self.day_part_idx] + " până la ora " + forecast_time_1 + ", astăzi " + weather[0] + ", cu o temperatură de " + temperature[0] + \
                " grade, cu vânt de " + wind_speed[0].replace(".", ",") + " metri pe secundă din direcția " + wind_direction[0] + \
                ". Prognoza de " + \
                day_parts[0][next_part_idx] + " la ora " + forecast_time_2 + " până la ora " + forecast_time_3 + \
                ", este " + weather[1] + ", cu o temperatură de " + temperature[1] + " grade, cu vânt de " + wind_speed[1].replace(".", ",") + \
                " metri pe secundă din direcția " + wind_direction[1] + \
                ". Prognoza meteo furnizată de aplicația wai ar, a institutilui meteorologic din norvegia și a en er ka."

        elif self.language == "english":
            day_parts = [["this morning","this afternoon","this evening", "tonight"],["Good morning","Good afternoon","Good evening", "Good eventing"]]
            next_part_idx = utils.next_index_loop(day_parts, self.day_part_idx)
            self.forecast_string = day_parts[1][self.day_part_idx] + " " + self.stations[self.station] + ". The weather for " + \
                day_parts[0][self.day_part_idx] + " until " + forecast_time[1] + ", is " + weather[0] + ", with a temperature of " + temperature[0] + \
                " degrees, with a windspeed of " + wind_speed[0] + " meters per second, in the direction " +  \
                wind_direction[0] + ". The forecast for " + \
                day_parts[0][next_part_idx] + " from " + forecast_time[2] + " to " + forecast_time[3] + \
                ", is " + weather[1] + ", with a temperature of " + temperature[1] + " degrees, and a windspeed of " + wind_speed[1] + \
                " meters per second, in the direction " + wind_direction[1] + \
                ". Weather forecast from Y R, delivered by the Norwegian Meteorological Institute and N R K."
        else:
            self.forecast_string = ""


    def translate(self, id, table):
        # !! translation tables to be in db
        file_dict = {"weather":'weather_translation_yrno.csv', "direction":"direction_translation_yrno.csv"}
        with open(os.path.join(os.path.dirname(__file__), file_dict[table]), mode='r') as infile:
            reader = csv.DictReader(infile, delimiter="\t")
            for row in reader: 
                if row['ID'] == str(id):
                    return row[self.language]

    def update_xml(self, location = "https://ttstestfeeds.s3.amazonaws.com/audio/weather"):
        # adujust path to fit S3 buckets. maybe should coordinate this script and EC2 to match s3 buckets
        audioFile = os.path.join(os.path.basename(self.fpath) + "." + self.audio_format)
        audioFileWeb = os.path.join(location, self.station, audioFile)
        xmlPath = os.path.join("podcasts", "weather_" + self.station + "_" + self.language + ".xml")
        print(xmlPath)
        if os.path.exists(xmlPath) is False:
            print("make an xml file for this podcast in the xml folder")
            return None

        # get file size in bytes
        length = str(utils.get_file_size(os.path.join("weather/audio", self.station, audioFile)))
        # open current xml file
        with open(xmlPath, 'r') as file:
            rss = file.read()
        # create new item, with subelements
        root = etree.fromstring(rss)
        items = root.findall(".//item")
        newItem = etree.Element("item")
        etree.SubElement(newItem, "title").text = os.path.splitext(os.path.basename(audioFileWeb))[0]
        etree.SubElement(newItem, "link").text = os.path.dirname(audioFileWeb)
        etree.SubElement(newItem, "guid").text = audioFileWeb
        etree.SubElement(newItem, "description").text = ""
        etree.SubElement(newItem, "enclosure", url=audioFileWeb, length=length, type="audio/mpeg")
        etree.SubElement(newItem, "category").text = "TTS"
        etree.SubElement(newItem, "pubDate").text = str(utils.get_local_time(self.tz)[0])
        # insert new item as first item (subelement of channel element)
        root[0].insert(10, newItem)
        # create element tree from updated root and write back to xml file
        et = etree.ElementTree(root)
        et.write(xmlPath, pretty_print=True)


    def get_file_name(self):
        day_part = utils.get_day_part(self.tz)
        filename = datetime.datetime.now(pytz.timezone(self.tz)).strftime("%Y-%m-%d") + "_" + str(day_part)
        return filename


    def set_last_update(self, last_update_tag):
        self.last_update = utils.get_time(last_update_tag.text)


    def set_yr_URL(self):
        if self.station == 'cu':
            self.url = 'https://www.yr.no/place/Portugal/Madeira/Curral_das_Freiras/forecast.xml'
        elif self.station == 'sg':
            self.url = 'https://www.yr.no/place/Romania/Tulcea/Sf%C3%A2ntu_Gheorghe/forecast.xml'
        elif self.station == 'vv':
            self.url = 'https://www.yr.no/place/Romania/Other/V%C3%A2rvoru/forecast.xml'
        elif self.station == 'be':
            self.url = 'https://www.yr.no/place/Ireland/Other/Bere_Island/forecast.xml'
        else: self.url = None


    def get_yr_URL(self):
        return self.url

    #Create podcast
    # call when audio gen is successful
    # This will call a utils method, takes filename? other required info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on yr.no')
    parser.add_argument('station', type=str, help='station location code (cu, ma)')
    parser.add_argument('language', type=str, help='language')
    parser.add_argument('-g', '--gender', type=str, default='female', help='Preferred gender of speaker)')
    parser.add_argument('-a', '--accent', type=str, default=None, help='Preferred gender of speaker)')
    parser.add_argument('-sg', '--strict_gender', default=False, type=str, help='is preferred gender strict?')
    parser.add_argument('-sa', '--strict_accent', default=False, type=str, help='is preferred accent strict?')
    parser.add_argument('-sr', '--sample_rate', default=8000, type=int, help='sample rate')
    parser.add_argument('-af', '--audio_format', default='mp3', type=str, help='is preferred accent strict?')
    parser.add_argument('-m', '--metadata', default=False, type=str, help='metadata true or false')
    parser.add_argument('-t', '--time_frame_count', default=2, type=int, help='number of time frames to forecast')


    args = parser.parse_args()
    YrForecast(args.station, args.language, args.gender, args.accent, args.strict_gender, \
            args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.time_frame_count)
