import os
import requests
from lxml import objectify
from delorean import Delorean

BART_API_KEY = os.getenv('BART_API_KEY')

def build_request(**kwargs):
    cmd = kwargs.get('cmd', 'etd')
    orig = kwargs.get('orig', 'DBRK')
    direction = kwargs.get('direction', 's')
    key = kwargs.get('key', None)
    if key == None:
        raise Exception, "Bart api key must be provided"
    url_str = 'http://api.bart.gov/api/etd.aspx?cmd={0}&orig={1}&dir={2}&key={3}'.format(
            cmd, orig, direction, key)
    return url_str

def retrieve_api_object(**kwargs):
    url_str = build_request(**kwargs)
    r = requests.get(url_str)
    if r.status_code != 200:
        raise Exception, "Error getting request from BART api"
    try:
        request_text = str(r.text)
    except:
        raise Exception, "Error converting xml text to string"
    root = objectify.fromstring(request_text)
    return root

def retrieve_trains(lxml_request):
    if not hasattr(lxml_request, 'station'):
        raise Exception, "Error retrieving data from xml object"
    station_name = lxml_request.station.name
    abbr = lxml_request.station.abbr
    trains = [Train.from_xml(etd) for etd in lxml_request.station.etd]
    return trains

class Estimate:

    def __init__(self, minutes, platform, length):
        if minutes == 'Leaving':
            self.minutes = 0
        else:
            self.minutes = int(minutes)
        self.platform = int(platform)
        self.length = int(length)
        self.timestamp = Delorean()
        
    def time_departing(self):
        current = Delorean()
        timedelta = current - self.timestamp
        minutes_passed = timedelta.minutes / 60
        return self.minutes - minutes_passed
    
    @staticmethod
    def from_xml(lxml_estimate):
        estimate = Estimate(lxml_estimate.minutes, lxml_estimate.platform,
                            lxml_estimate.length)
        return estimate

    def __repr__(self):
        return "<Estimate: {0.length} cars in {0.minutes} minutes".format(self)

class Train:

    def __init__(self, abbr, name, direction, color):
        self.abbr = abbr
        self.name = name
        self.direction = direction
        self.color = color
        self.estimates = []

    @staticmethod
    def from_xml(lxml_etd):
        train = Train(lxml_etd.abbreviation, lxml_etd.destination, 
                      lxml_etd.estimate.direction, lxml_etd.estimate.color)
        for estimate in lxml_etd.estimate:
            train.estimates.append(Estimate.from_xml(estimate))
        return train

    def __repr__(self):
        return "<Train: {0.abbr}>".format(self)

if __name__ == '__main__':
    lxml_request = retrieve_api_object(cmd = 'etd', orig = 'DBRK', direction = 's', key = BART_API_KEY)
    for train in retrieve_trains(lxml_request):
        print train
        for estimate in train.estimates:
            print estimate
