#!/usr/bin/python
# Olivier Salmon
#
# Loop though a list of numbers from a CSV file and return Number Insight results
#
# Usage ./python3 NiAdvancedAsyncCsvCli.py -k <api_key> -s <api_secret> -c <column_header> -i <infile> -o <outfile> -t <type> -y <country>
# column header: name of the column containing the phone numbers
# type: basic / standard / advanced
# country: specify ISO2 country if the phone numbers are not in international format
# cnam: yes/no


import csv
import urllib
import sys
import getopt
import json
import datetime
import time
import requests
from requests_toolbelt.utils import dump
from requests import get

ip_address = get('https://api.ipify.org').text
print('My public IP address is:', ip_address)


def main(argv):
    api_key = ''
    api_secret = ''
    column_header = 'phone'
    infile = ''
    outfile = ''
    country = 'none'

    try:
        opts, args = getopt.getopt(argv, "hk:s:p:t:n:y:", [
                                   "api_key", "secret_key", "phone_number", "type", "cnam", "country"])
    except getopt.GetoptError:
        print('NumberInsightAllCliCsv.py -k <api_key> -s <api_secret> -p <phone_number> -t <type> -n <cnam> -y <country>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('NumberInsightAllCliCsv.py -k <api_key> -s <api_secret> -p <phone_number> -t <type> -n <cnam> -y <country>')
            sys.exit()
        elif opt in ("-k", "--api_key"):
            api_key = arg
        elif opt in ("-s", "--api_secret"):
            api_secret = arg
        elif opt in ("-p", "--phone_number"):
            phone_number = arg
        elif opt in ("-t", "--type"):
            type = arg
        elif opt in ("-n", "--cnam"):
            cnam = arg
        elif opt in ("-y", "--country"):
            country = arg

    print(type)
    

    if type == 'basic':
        print("NI basic")
        nibasic(api_key=api_key, api_secret=api_secret, phone_number=phone_number, cnam=cnam, country=country)
    elif type == 'standard':
        print("NI standard")
        nistandard(api_key=api_key, api_secret=api_secret, phone_number=phone_number, cnam=cnam, country=country)
    elif type == 'advanced':
        print("NI advanced")
        niadvanced(api_key=api_key, api_secret=api_secret, phone_number=phone_number, cnam=cnam, country=country, ip_address=ip_address)


def nibasic(api_key, api_secret, phone_number, cnam, country):
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'number': phone_number,
        'force-hlr-handler': 'infobip'
        #'force-hlr-handler' : 'vertex'
    }

    if country != 'none':
        country_payload = {
            'country': country
        }
        payload = dict(payload.items() | country_payload.items())

    #payload = dict(payload.items())
    url = 'https://api.nexmo.com/ni/basic/json?'
    headers = {'Accept': 'application/json'}

    while True:
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                break

        except Exception as inst:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            print(st, str(inst))

    decoded_response = response.json()

    # Check if your messages are succesful
    if decoded_response['status'] == 0:
        txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + ";" + str(decoded_response['request_id']) + ";" + str(decoded_response['international_format_number']) + ";" + str(
                        decoded_response['national_format_number']) + ";" + str(decoded_response['country_name']) + ";" + str(decoded_response['country_prefix']) + ";" + str(decoded_response['country_code']) + ";" + str(decoded_response['country_code_iso3']) + "\n"
        print(txtline)
        print(response)
    else:
        txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + "\n"
        print(txtline)


def nistandard(api_key, api_secret, phone_number, cnam, country):
    country_code = ''

    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'number': phone_number,
        'force-hlr-handler': 'infobip'
    }

    if country != 'none':
        country_payload = {
            'country': country
        }
        payload = dict(payload.items() | country_payload.items())

    # Do we need to get cnam? US only
    if cnam == 'yes':
        url = 'https://api.nexmo.com/ni/basic/json?'
        headers = {'Accept': 'application/json'}

        while True:
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    break

            except Exception as inst:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                print(st, str(inst))

        decoded_response = response.json()

        # Check if your messages are succesful
        if decoded_response['status'] == 0:
            country_name = str(decoded_response['country_name'])
            country_code = str(decoded_response['country_code'])
        else:
            txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message'])
            print(txtline)

        if country_code == 'US':
            cnam_payload = {
                'cnam': 'true'
            }
        payload = dict(payload.items() | cnam_payload.items())


    url = 'https://api.nexmo.com/ni/standard/json?'
    headers = {'Accept': 'application/json'}

    print(payload)

    while True:
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                break

        except Exception as inst:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            print(st + " : " + str(inst))

    decoded_response = response.json()

    # Check if your messages are succesful
    if decoded_response['status'] == 0:
        print(response)
    else:
        txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message'])
        print(txtline)


def niadvanced(api_key, api_secret, phone_number, cnam, country, ip_address):
    country_code = ''
    
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'number': phone_number,
        'ip': ip_address
    }

    if country != 'none':
        country_payload = {
            'country': country
        }
        payload = dict(payload.items() | country_payload.items())       

    # Do we need to get cnam? US only
    if cnam == 'yes':
        url = 'https://api.nexmo.com/ni/basic/json?'
        headers = {'Accept': 'application/json'}

        while True:
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    break

            except Exception as inst:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                print(st, str(inst))

        decoded_response = response.json()

        # Check if your messages are succesful
        if decoded_response['status'] == 0:
            country_name = str(decoded_response['country_name'])
            country_code = str(decoded_response['country_code'])
        else:
            txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message'])
            print(txtline)

        if country_code == 'US':
            cnam_payload = {
                'cnam': 'true'
            }
            payload = dict(payload.items() | cnam_payload.items())

    print(payload)

    url = 'https://api.nexmo.com/ni/advanced/json?'
    headers = {'Accept': 'application/json'}

    while True:
        try:
            #response = requests.get(url, headers=headers, json=payload)
            response = requests.post(url, headers=headers, json=payload)
            print(response)
            data = dump.dump_all(response)
            print(data.decode('utf-8'))
            if response.status_code == 200:
                break

        except Exception as inst:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            print(st + " : " + str(inst))

    decoded_response = response.json()
    # Decode JSON response from UTF-8
    #decoded_response = json.loads(data.decode('utf-8'))
    # Check if your messages are succesful
    if decoded_response['status'] == 0:
        txtline = 'Success' + " : " + decoded_response['request_id'] + "\n"
        print(txtline)
        print(response)
    else:
        txtline = 'Error' + " : " + str(decoded_response) + "\n"
        print(txtline)


if __name__ == "__main__":
    main(sys.argv[1:])
