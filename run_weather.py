import time
import datetime
import argparse
from weather.yr_forecast import YrForecast
import utils.utils as utils
import requests
from bs4 import BeautifulSoup
from random import randrange



def check_for_update(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.content, 'lxml')
    last_update = utils.get_time(bs.find("lastupdate").text)
    return last_update


def monitor(forecast):
    forecast = YrForecast(args.station, args.language, args.gender, args.accent, args.strict_gender, \
                args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.time_frame_count)
    while True:
        while utils.get_local_time[0].hour not in [5,11,17,23] and datetime.datetime.now().minute not in range(55, 57):    
            time.sleep(60)
        try:
            forecast.generate_forecast_string()
            forecast.generate_forecast_audio()
        except:
            forecast = YrForecast(args.station, args.language, args.gender, args.accent, args.strict_gender, \
                args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.time_frame_count)
        time.sleep(60)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on yr.no')
    parser.add_argument('station', type=str, help='station location code (cu, ma)')
    parser.add_argument('language', type=str, help='language')
    parser.add_argument('-g', '--gender', type=str, default='female', help='Preferred gender of speaker)')
    parser.add_argument('-a', '--accent', type=str, default=None, help='Preferred gender of speaker)')
    parser.add_argument('-sg', '--strict_gender', default=False, type=str, help='is preferred gender strict?')
    parser.add_argument('-sa', '--strict_accent', default=False, type=str, help='is preferred accent strict?')
    parser.add_argument('-sr', '--sample_rate', default=8000, type=int, help='sample rate')
    parser.add_argument('-af', '--audio_format', default='mp3', type=str, help='audio format')
    parser.add_argument('-m', '--metadata', default=True, type=str, help='metadata true or false')
    parser.add_argument('-t', '--time_frame_count', default=2, type=int, help='number of time frames to forecast')


    args = parser.parse_args()

    monitor(args)