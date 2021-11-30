# Twitter COVID-19
In this project, we wish to explore the extent of polarization on Twitter. Our goal is to identify ideological communities corresponding to the pro-vs-anti vaccine movements, the nature of their interactions, to provide us with an approximate score of the extent of polarization, and to determine whether each of these communities share a common set of interests.

# Mention Network
The ```2021-07-01-hydrated_tweets.mention_network.gpickle``` file is in the google drive [2021-07-01 dataset - get_metadata output](https://drive.google.com/drive/u/0/folders/1xcFGbn6iHpBmGZ6CCSHjKHF_m5iZRgAZ)

# Environment Variables
The file twitter_api_investigation.py requires a .env file. Create one with the following structure:
```
CONSUMER_KEY=
CONSUMER_SECRET=

OAUTH_TOKEN=
OAUTH_TOKEN_SECRET=
```
Refer to [Twitter Developer documentation](https://developer.twitter.com/en/docs/apps/overview) for information about getting a dev account and proper access (e.g., a consumer key)

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
These are the runs I did. Note the directory. Follow this structure, but don't use these dates as I have already hydrated tweets for these days.
```
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-04-10-dataset.tsv -o ./data/tweets/2020-04-10/2020-04-10-hydrated_tweets -k api_keys.json
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-07-01-dataset.tsv -o ./data/tweets/2020-07-01/2020-07-01-hydrated_tweets -k api_keys.json
python ./data_acquisition/get_metadata.py -i ./data/tsv/2020-09-09-dataset.tsv -o ./data/tweets/2020-09-09/2020-09-09-hydrated_tweets -k api_keys.json
python ./data_acquisition/get_metadata.py -i ./data/tsv/2021-07-01-dataset.tsv -o ./data/tweets/2021-07-01/2021-07-01-hydrated_tweets -k api_keys.json
```
# Important Dates
refer to [Issue #2](https://github.com/cagri32/Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/issues/2#issuecomment-970665240)

Given that the media is a primary driver of the intensity of social media user response, the following countries are prioritized by widespread media coverage of COVID-19 events, in order, with their reasons;

- USA (Has significant global media and economic influence, strong interest in global media due to the Trump administration)
- China (Had the first identified cases, has significant economic influence, strong interest from Western media)
- Italy (Was an epicentre of the pandemic in the early stages)
- Australia (specifically Melbourne, Victoria state, was eventually used as a example of authoritarian pandemic response, by critics)
- The rest of the world.

## by Tweet count in the [dataset](https://github.com/thepanacealab/covid19_twitter/tree/master/dailies)





-----------------
In Progress

* January 27th 2021 - The US surpasses 1 million deaths from COVID-19 [1](https://www.paho.org/en/news/27-1-2021-americas-surpasses-one-million-deaths-covid-19)

* October 2nd 2020 - Donald and Melania Trump contract COVID-19, they were the then President and First Lady of the USA. [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=36)

* July 1st 2020 - Texas face mask mandate, among other states that results in "gunfights and other violence" [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=24)

* Late June 2020 - Travel quarantines for Americans in interstate travel begins [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=32)

* April 28th 2020 - The US reaches the 1 million total cases of COVID-19 [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=29),[2](https://www.npr.org/sections/coronavirus-live-updates/2020/04/28/846741935/u-s-surpasses-1-million-coronavirus-cases)

* April 17th 2020 - President Trump releases guidelines for reopening the USA [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=29)

* April 4th 2020 - President Trump endorses the use of the malaria drug hydroxychloroquine [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=28)

* March 26th 2020 - New York City becomes an epicentre of COVID-19 in the world (surpassing Italy and Spain at the time)[1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=27)