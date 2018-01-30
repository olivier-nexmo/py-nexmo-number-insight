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


import csv, urllib, sys, getopt, json, datetime, time, requests
from requests_toolbelt.utils import dump

def main(argv):
    api_key = ''
    api_secret = ''
    column_header = 'phone'
    infile = ''
    outfile = ''
    country = 'none'

    try:
        opts, args = getopt.getopt(argv, "hk:s:c:i:o:t:n:y:", ["api_key", "secret_key", "column_header","infile", "outfile", "type", "cnam", "country"])
    except getopt.GetoptError:
        print('NumberInsightAllCliCsv.py -k <api_key> -s <api_secret> -c <column_header> -i <infile> -o <outfile> -t <type> -n <cnam> -y <country>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('NumberInsightAllCliCsv.py -k <api_key> -s <api_secret> -c <column_header> -i <infile> -o <outfile> -t <type> -n <cnam> -y <country>')
            sys.exit()
        elif opt in ("-k", "--api_key"):
            api_key = arg
        elif opt in ("-s", "--api_secret"):
            api_secret = arg
        elif  opt in ("-c", "--column_header"):
            column_header = arg
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg
        elif opt in ("-t", "--type"):
            type = arg
        elif opt in ("-n", "--cnam"):
            cnam = arg
        elif opt in ("-y", "--country"):
            country = arg

    print(type)

    if type == 'basic':
        print("NI basic")
        nibasic(api_key=api_key, api_secret=api_secret, column_header=column_header, infile=infile, outfile=outfile,
            cnam=cnam, country=country)
    elif type == 'standard':
        print("NI standard")
        nistandard(api_key=api_key, api_secret=api_secret, column_header=column_header, infile=infile, outfile=outfile,
               cnam=cnam, country=country)
    elif type == 'advanced':
        print("NI advanced")
        niadvanced(api_key=api_key, api_secret=api_secret, column_header=column_header, infile=infile, outfile=outfile,
               cnam=cnam, country=country)

def nibasic(api_key, api_secret, column_header, infile, outfile, cnam, country):
    script_start = datetime.datetime.now()
    print(script_start)
    count = 0
    with open(infile) as csvfile:
        outfile_csv = outfile + '.csv'
        outfile_log = outfile + '.log'
        with open(outfile_csv, 'w') as txtfile:

            txtfile.write('status;status_message;request_id;international_format_number;national_format_number;country_name;country_prefix;country_code;country_code_iso3\n')

            reader = csv.DictReader(csvfile)

            for row in reader:
                payload = {
                    'api_key':api_key,
                    'api_secret':api_secret,
                    'number':row[column_header],
                    'force-hlr-handler':'infobip'
                    #'force-hlr-handler' : 'vertex'
                }

                if country != 'none':
                    country_payload = {
                        'country':country
                    }
                    payload = dict(payload.items() | country_payload.items())

                #payload = dict(payload.items())
                url = 'https://api.nexmo.com/ni/basic/json?'
                headers = {'Accept':'application/json'}

                while True:
                    try:
                        response = requests.post(url, headers=headers, json=payload)
                        if response.status_code == 200:
                            break

                    except Exception as inst:
                        ts = time.time()
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                        csvfile.writerow(st,str(inst))

                decoded_response = response.json()

                # Check if your messages are succesful
                count = count + 1
                if decoded_response['status'] == 0:
                    txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + ";" + str(decoded_response['request_id']) + ";" + str(decoded_response['international_format_number']) + ";" + str(decoded_response['national_format_number']) + ";" + str(decoded_response['country_name']) + ";" + str(decoded_response['country_prefix']) + ";" + str(decoded_response['country_code']) + ";" + str(decoded_response['country_code_iso3']) + "\n"
                    #print(txtline)

                else:
                    txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + "\n"
                    #print(txtline)

                txtfile.write(txtline)
                print(count)

    script_end = datetime.datetime.now()
    print(script_end)
    diff = (script_end - script_start)
    diff_minutes = diff.seconds / 60
    print(str(count) + ' numbers processed in ' + str(diff_minutes) + ' minutes')

def nistandard(api_key, api_secret, column_header, infile, outfile, cnam, country):
    script_start = datetime.datetime.now()
    print(script_start)
    count = 0
    with open(infile) as csvfile:
        outfile_csv = outfile + '.csv'
        outfile_log = outfile + '.log'
        with open(outfile_csv, 'w') as txtfile:

            country_code = ''

            txtfile.write(
                'status;status_message;request_id;international_format_number;national_format_number;country_name;country_prefix;country_code;country_code_iso3;ported;roaming status;original_carrier network_type;original_carrier name;original_carrier network_code;original_carrier country;current_carrier network_type;current_carrier name;current_carrier network_code;current_carrier country;caller_type;caller_name;first_name;last_name\n')

            reader = csv.DictReader(csvfile)

            for row in reader:
                payload = {
                    'api_key':api_key,
                    'api_secret':api_secret,
                    'number':row[column_header],
                    'force-hlr-handler':'infobip'
                    #'force-hlr-handler' : 'vertex'
                }

                if country != 'none':
                    country_payload = {
                        'country':country
                    }
                    payload = dict(payload.items() | country_payload.items())

                #print(payload)

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
                            csvfile.writerow(st, str(inst))

                    decoded_response = response.json()

                    # Check if your messages are succesful
                    if decoded_response['status'] == 0:
                        country_name = str(decoded_response['country_name'])
                        country_code = str(decoded_response['country_code'])
                    else:
                        txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + "\n"
                        txtfile.write(txtline)
                
                if country_code == 'US':
                    cnam_payload = {
                        'cnam':'true'
                    }
                    payload = dict(payload.items() | cnam_payload.items())

                #print(payload)

                url = 'https://api.nexmo.com/ni/standard/json?'
                headers = {'Accept':'application/json'}

                while True:
                    try:
                        #response = requests.get(url, headers=headers, json=payload)
                        response = requests.post(url, headers=headers, json=payload)
                        if response.status_code == 200:
                            break

                    except Exception as inst:
                        ts = time.time()
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                        txtfile.write(st + " : " + str(inst) + "\n")

                decoded_response = response.json()

                # Check if your messages are succesful
                count = count + 1
                if decoded_response['status'] == 0:
                    try:
                        txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + ";" + str(decoded_response['request_id']) + ";" + str(decoded_response['international_format_number']) + ";" + str(decoded_response['national_format_number']) + ";" + str(decoded_response['country_name']) + ";" + str(decoded_response['country_prefix']) + ";" + str(decoded_response['country_code']) + ";" + str(decoded_response['country_code_iso3']) + ";" \
                              + str(decoded_response['ported']) + ";" + str(decoded_response['roaming']['status']) + ";" + str(decoded_response['original_carrier']['network_type']) + ";" + str(decoded_response['original_carrier']['name']) + ";" + str(decoded_response['original_carrier']['network_code']) + ";" + str(decoded_response['original_carrier']['country']) + ";" \
                              + str(decoded_response['current_carrier']['network_type']) + ";" + str(
                        decoded_response['current_carrier']['name']) + ";" + str(
                        decoded_response['current_carrier']['network_code']) + ";" + str(
                        decoded_response['current_carrier']['country'])  \
                        #print(txtline)
                    except KeyError:
                        txtline = str(decoded_response['status']) + ";Python KeyError:" + str(KeyError)
                else:
                    txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message'])
                    #print(txtline)

                if country_code == 'US':
                    txtline += ";" + str(decoded_response['caller_type']) + ";" + str(decoded_response['caller_name']) + ";" + str(decoded_response['first_name']) + ";" + str(decoded_response['last_name']) + "\n"
                else:
                    txtline += "\n"

                txtfile.write(txtline)

                print(count)

    script_end = datetime.datetime.now()
    print(script_end)
    diff = (script_end - script_start)
    diff_minutes = diff.seconds / 60
    print(str(count) + ' numbers processed in ' + str(diff_minutes) + ' minutes')

def niadvanced(api_key, api_secret, column_header, infile, outfile, cnam, country):
    script_start = datetime.datetime.now()
    print(script_start)
    count = 0
    with open(infile) as csvfile:
        outfile_csv = outfile + '.csv'
        outfile_log = outfile + '.log'
        with open(outfile_log, 'w') as txtfile:

            country_code=''

            reader = csv.DictReader(csvfile)

            for row in reader:
                payload = {
                    'api_key':api_key,
                    'api_secret':api_secret,
                    'number':row[column_header],
                    'callback':'<your_server_url>/ni_async_cnam_cb.php?filename=' + str(outfile_csv)
                }

                if country != 'none':
                    country_payload = {
                        'country':country
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
                            csvfile.writerow(st, str(inst))

                    decoded_response = response.json()

                    # Check if your messages are succesful
                    if decoded_response['status'] == 0:
                        country_name = str(decoded_response['country_name'])
                        country_code = str(decoded_response['country_code'])
                    else:
                        txtline = str(decoded_response['status']) + ";" + str(decoded_response['status_message']) + "\n"
                        txtfile.write(txtline)

                if country_code == 'US':
                    cnam_payload = {
                        'cnam':'true'
                    }
                    payload = dict(payload.items() | cnam_payload.items())

                #print(payload)

                #payload = dict(payload.items())
                url = 'https://api.nexmo.com/ni/advanced/async/json?'
                headers = {'Accept':'application/json'}

                while True:
                    try:
                        #response = requests.get(url, headers=headers, json=payload)
                        response = requests.post(url, headers=headers, json=payload)
                        #print(response)
                        #data = dump.dump_all(response)
                        #print(data.decode('utf-8'))
                        if response.status_code == 200:
                            break

                    except Exception as inst:
                        ts = time.time()
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                        txtfile.write(st + " : " + str(inst) + "\n")

                decoded_response = response.json()
                # Decode JSON response from UTF-8
                #decoded_response = json.loads(data.decode('utf-8'))
                # Check if your messages are succesful
                if decoded_response['status'] == 0:
                    count = count + 1
                    txtline= 'Success' + " : " + decoded_response['request_id'] + "\n"
                    txtfile.write(txtline)
                else:
                    #txtline = 'Error' + " : " + str(decoded_response['status']) + " : " + str(decoded_response['status_message']) + "\n"
                    txtline = 'Error' + " : " + str(decoded_response) + "\n"
                    txtfile.write(txtline)

                print(count)

    script_end = datetime.datetime.now()
    print(script_end)
    diff = (script_end - script_start)
    diff_minutes = diff.seconds / 60
    print(str(count) + ' numbers processed in ' + str(diff_minutes) + ' minutes')

if __name__ == "__main__":
  main(sys.argv[1:])


