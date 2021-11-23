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

NOTE: these are instructions for Windows
``` bash
cd Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/tutorial
source tweepy3.8.0/Scripts/activate
pip install -r requirements.txt
python create_api_keys_json_file.py
python get_dataset_tsv.py --dataset_url https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/2021-01-20/2021-01-20_clean-dataset.tsv.gz?raw=true
python get_metadata.py -i clean-dataset.tsv -o hydrated_tweets -k api_keys.json
```
## Sample
```
python get_metadata.py -i 2021-11-01_clean-dataset.tsv -o 2021-11-01_hydrated_tweets -k api_keys.json
```
# Important Dates
refer to [Issue #2](https://github.com/cagri32/Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/issues/2#issuecomment-970665240)

[a covid timeline](https://blog.cheapism.com/how-we-got-coronavirus/#slide=24)
"Face Mask Wars" July 1 2020 - Texas face mask mandate