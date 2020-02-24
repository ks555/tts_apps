import time
import argparse
from files_to_text.files_to_text import iter_files
import utils.utils as utils
import requests
from bs4 import BeautifulSoup


def monitor(args):
    iter_files(args.path, args.language, args.gender, args.accent, args.strict_gender, \
                args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on yr.no')
    parser.add_argument('path', type=str, help='dir path with text files to convert')
    parser.add_argument('language', type=str, help='language')
    parser.add_argument('-g', '--gender', type=str, default='female', help='Preferred gender of speaker)')
    parser.add_argument('-a', '--accent', type=str, default=None, help='Preferred gender of speaker)')
    parser.add_argument('-sg', '--strict_gender', default=False, type=str, help='is preferred gender strict?')
    parser.add_argument('-sa', '--strict_accent', default=False, type=str, help='is preferred accent strict?')
    parser.add_argument('-sr', '--sample_rate', default=8000, type=int, help='sample rate')
    parser.add_argument('-af', '--audio_format', default='wav', type=str, help='is preferred accent strict?')
    parser.add_argument('-m', '--metadata', default=True, type=str, help='metadata true or false')


    args = parser.parse_args()
    iter_files(args.path, args.language, args.gender, args.accent, args.strict_gender, \
                args.strict_accent, args.sample_rate, args.audio_format, args.metadata)
