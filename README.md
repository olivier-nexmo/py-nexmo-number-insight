# py-nexmo-number-insight
Return number's phone information based on Nexmo's Number Insight APIs (basic, standard, advanced, advanced async).

# Pre-requisites
- Python 3
- Requests module `pip install requests`

# Run it

From a command line:

```python
python3 NumberInsightAllCliCsv.py -k <your_api_key> -s <your_api_secret> -c phone -i <input_file.csv> -o <output_file> -t <type> -n <y/n>
```

Where:

- `your_api_key` and `api_secret` are your api key and secret available in the Nexmo dashboard (Settings)
- `phone` is the name of the CSV column containing the list of phone numbers. Needs to be in international format
- `input_file.csv` is your CSV file containing the list of phone numbers
- `output_file` will be the file containing the results, in CSV format
- `type` is the level of the Number Insight API (basic, standard, advanced)
- `y/n` choose yes or no if you want to retrieve the user lastname and firstname (cnam). US only

API documentation: https://developer.nexmo.com/number-insight/overview

Note: the number insight advanced is using, in the script, the asynchronous version and requires a callback URL (set in the script on line 263). 
