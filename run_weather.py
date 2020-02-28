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


def check_if_update_time(current):
    update_times = [[datetime.time(5, 55), datetime.time(5, 58)], [datetime.time(11, 55), datetime.time(11, 58)],\
     [datetime.time(17, 55), datetime.time(17, 58)], [datetime.time(23, 55), datetime.time(23, 58)]]
    for update_time in update_times:
        if current >= update_time[0] and current < update_time[1]:
            return True
    return False


def monitor(forecast):
    # generate initial forecast audio and text
    forecast = YrForecast(args.station, args.language, args.gender, args.accent, args.strict_gender, \
                args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.time_frame_count)
    updated = False
    while True: # loop to maintain script active and monitoring
        # continously check whether it is update time (four periods daily, based on local time zone)
        while check_if_update_time(utils.get_local_time(forecast.tz)[0].time()) == False:
        #while utils.get_local_time(forecast.tz)[0].hour not in [5,11,17,23] and utils.get_local_time(forecast.tz)[0].minute not in range(44, 47):    
            updated = False
            time.sleep(60)
        # If it is updated time, complete forecast update     
        if updated == False:
            try:
                # re-generate audio and text
                forecast.generate_forecast_string()
                forecast.generate_forecast_audio()
                updated = True
            except:
            # if update fails, try again
            # !!Need alert mechanism if no update is made during the time period
                pass
        # wait 60 seconds before checking time again
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