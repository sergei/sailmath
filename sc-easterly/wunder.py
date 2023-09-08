import argparse
import csv
import datetime
import json
import os

import requests

WUNDERGROUND_API_KEY = '6532d6454b8aa370768e63d6ba5a832e'


def fetch_station_day_data(pws_id, day):
    url = 'https://api.weather.com/v2/pws/history/all'
    params = {
        'stationId': pws_id,
        'format': 'json',
        'units': 'e',
        'date': day.strftime('%Y%m%d'),
        'apiKey': WUNDERGROUND_API_KEY
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.wunderground.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    print response
    observations = None
    if response.status_code == 200:
        try:
            observations = response.json()['observations']
        except:
            print 'Failed to decode returned data {}'.format(response)

    return observations


def fetch_station_interval_data(pws_id, start_date, end_date):
    station_onservations = []
    for day in daterange(start_date, end_date):
        print 'Fetching station {} date for {}'.format(pws_id, day)
        day_observations = fetch_station_day_data(pws_id, day)
        if day_observations:
            print 'Got {} daily observations'.format(len(day_observations))
            station_onservations += day_observations

    print 'Got {} station observations'.format(len(station_onservations))
    return station_onservations


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def store_station_data(pws_id, start_date, end_date, work_dir):
    work_dir = os.path.expanduser(work_dir)
    output_file_name = work_dir + os.sep + pws_id + '.json'
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    with open(output_file_name, 'wt') as out_json_file:
        observations = fetch_station_interval_data(pws_id, start_date, end_date)
        json.dump(observations, out_json_file)
        print 'Created {} file with {} observations for station {}'.format(output_file_name, len(observations), pws_id)


def store_stations_data(stations_list_csv, day_from, day_to, work_dir):
    pws_id_list = []
    with open(os.path.expanduser(stations_list_csv), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if csv_reader.line_num > 1:  # Skip header
                pws_id_list.append(row[1])

    for pws_id in pws_id_list:
        store_station_data(pws_id, day_from, day_to, work_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--stations-list", help="CSV file containing the list of PWS", default='stations.csv')
    parser.add_argument("--work-dir", help="Directory to keep temporary files", default='~/tmp/sc-easterly')
    args = parser.parse_args()

    day_from = datetime.datetime(2018, 3, 1)
    day_to = datetime.datetime(2018, 11, 1)

    #
    # fetch_station_day_data('KCASANTA254', datetime.datetime(2018, 10, 11))
    # fetch_station_interval_data('KCAWATSO63', day_from, day_to)
    # store_stations_data(args.stations_list, args.work_dir)
    #

    store_stations_data(args.stations_list, day_from, day_to, args.work_dir)
