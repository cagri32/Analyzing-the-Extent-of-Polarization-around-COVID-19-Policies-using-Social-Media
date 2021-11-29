# Twitter COVID-19
In this project, we wish to explore the extent of polarization on Twitter. Our goal is to identify ideological communities corresponding to the pro-vs-anti vaccine movements, the nature of their interactions, to provide us with an approximate score of the extent of polarization, and to determine whether each of these communities share a common set of interests.

# Twitter API Investigation
## Setup
The file twitter_api_investigation.py requires a .env file. Create one with the following structure:
```
CONSUMER_KEY=
CONSUMER_SECRET=

OAUTH_TOKEN=
OAUTH_TOKEN_SECRET=
```
Refer to [Twitter Developer documentation](https://developer.twitter.com/en/docs/apps/overview) for information about getting a dev account and proper access (e.g., a consumer key)

# Using Jupyter
``` bash
cd Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/
 
jupyter notebook
```
# Running get_metadata.py
This assumes you have the .env file set up.

get_dataset_tsv.py also has a --date flag for convenience.

NOTE: these are instructions for Windows using Git Bash
FYI: tweepy3.8.0 is a venv
``` bash
cd Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/
source tweepy3.8.0/Scripts/activate
pip install -r requirements.txt
python data_acquisition/create_api_keys_json_file.py
python data_acquisition/get_dataset_tsv.py --date 2021-07-01
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-04-10-dataset.tsv -o ./data/tweets/2020-04-10/2020-04-10-hydrated_tweets -k api_keys.json
```
## Sample
```
# These are the runs I did. Note the directory. Follow this structure, but don't use these dates as I have already hydrated tweets for these days.
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-04-10-dataset.tsv -o ./data/tweets/2020-04-10/2020-04-10-hydrated_tweets -k api_keys.json
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-07-01-dataset.tsv -o ./data/tweets/2020-07-01/2020-07-01-hydrated_tweets -k api_keys.json
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-09-09-dataset.tsv -o ./data/tweets/2020-09-09/2020-09-09-hydrated_tweets -k api_keys.json
python ./data_acquisition/get_metadata.py -i ./data/tsv/2021-07-01-dataset.tsv -o ./data/tweets/2021-07-01/2021-07-01-hydrated_tweets -k api_keys.json
```
# Important Dates
refer to [Issue #2](https://github.com/cagri32/Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/issues/2#issuecomment-970665240)

[a covid timeline](https://blog.cheapism.com/how-we-got-coronavirus/#slide=24)
"Face Mask Wars" July 1 2020 - Texas face mask mandate