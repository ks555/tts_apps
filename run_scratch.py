# -*- coding: UTF-8 -*
import utils.utils as utils


place, region, country, lat, lon = utils.get_place_names(u"Sfântu Gheorghe", "Tulcea", "RO")

print(utils.set_met_URL(lat, lon))

#now need to decide if I move to met.no for forecasting or not. This determines which URL I build, now that I have
#all the pieces. The only issue with met.no is that I think yr.no summarize the hourly data into 6 hour forecasts
#somehow. Maybe they will tell me...