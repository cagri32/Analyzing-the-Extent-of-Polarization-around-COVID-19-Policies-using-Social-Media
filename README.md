# Twitter COVID-19
In this project, we wish to explore the extent of polarization on Twitter. Our goal is to identify ideological communities corresponding to the pro-vs-anti vaccine movements, the nature of their interactions, to provide us with an approximate score of the extent of polarization, and to determine whether each of these communities share a common set of interests.

We are using the data from the GitHub Repository https://github.com/thepanacealab/covid19_twitter for this project.

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
Refer to [Issue #2](https://github.com/cagri32/Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media/issues/2#issuecomment-970665240)

Given that the media is a primary driver of the intensity of social media user response, the following countries are prioritized by widespread media coverage of COVID-19 events, in order, with their reasons;

* USA - Has significant global media and economic influence, strong interest in global media due to the Trump administration at the time
* China - Had the first identified cases, has significant economic influence, strong interest from Western media
* Italy - Was an epicentre of the pandemic in the early stages
* Australia - Specifically Melbourne, Victoria state, was eventually used as a example of authoritarian pandemic response, by critics
* The rest of the world.

It is possible that although later dates may seem relatively significant, there could be a weaker response to them. This is because some studies have identified that media coverage of the pandemic is decreasing in spite of a "deepening crisis" - possibly from information fatigue. [1](https://www.thelancet.com/journals/lanplh/article/PIIS2542-5196(20)30303-X/fulltext), [2](https://www.pewresearch.org/journalism/2020/05/06/fewer-americans-now-say-media-exaggerated-covid-19-risks-but-big-partisan-gaps-persist/#public-overall-says-media-have-done-well-covering-the-crisis-but-differences-by-party-and-ideology-are-pronounced), [3](https://onlinelibrary.wiley.com/doi/10.1002/hbe2.260), [4](https://apps.who.int/iris/bitstream/handle/10665/335820/WHO-EURO-2020-1160-40906-55390-eng.pdf)

## by Tweet Data Size in the [Dataset](https://github.com/thepanacealab/covid19_twitter/tree/master/dailies)

1. October 2nd 2020 (30.1 MB) - Donald and Melania Trump contract COVID-19, they were the then President and First Lady of the USA. [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=36)

2. May 21st 2020 (27 MB) - US and UK Form Vaccine Deal with AstraZeneca. [1](https://www.astrazeneca.com/media-centre/press-releases/2020/astrazeneca-advances-response-to-global-covid-19-challenge-as-it-receives-first-commitments-for-oxfords-potential-new-vaccine.html)

3. July 13th 2020 (25.9 MB) - President Donald Trump makes his first public appearance wearing a face-mask.
WHO reports that the United States and Brazil made up half of the daily increase in coronavirus cases globally. [1](https://www.bbc.com/news/world-us-canada-53378439)

4. July 27th 2020 (25 MB) - Moderna Vaccine Begins Phase 3 Trial, Receives $472M From Trump Administration. [1](https://www.politico.com/news/2020/07/26/trump-invests-moderna-vaccine-candidate-381690)

5. July 7th 2020 (24.2 MB) - Benedetta Allegranzi, technical leader of the WHO task force on infection control stated that the WHO should be open to evidence that COVID-19 could be airbourne. [1](https://www.nature.com/articles/d41586-020-02058-1)

6. June 4th 2020 (23.3 MB) - Hong Kong Tiananmen Square vigil cancelled due to COVID. [1](https://www.theguardian.com/world/2021/jun/03/tiananmen-june-4-events-china-hong-kong-taiwan-macao-crackdown-covid)

7. September 9th 2020 (22.7 MB) - The United States announces it will stop screening international arrivals for COVID-19. More than 500,000 U.S. children have been diagnosed with COVID-19. [1](https://abcnews.go.com/Politics/us-government-end-covid-19-screenings-international-passengers/story?id=72928883), [2](https://www.cnn.com/2020/09/08/health/half-million-us-children-covid-wellness/index.html)

8. December 21st 2020 (19.7 MB) - The European Union approves the Pfizer-BioNTech vaccine.
U.S. President-elect Joseph R. Biden receives the Pfizer-BioNTech coronavirus vaccine on live television. [1](https://www.pfizer.com/news/press-release/press-release-detail/pfizer-and-biontech-receive-authorization-european-union)

9. July 1st 2020 (21.9 MB) - Texas face mask mandate, among other states that results in "gunfights and other violence". [1](https://blog.cheapism.com/how-we-got-coronavirus/#slide=24)

10. January 27th 2021 (15.5 MB) - The US surpasses 1 million deaths from COVID-19. [1](https://www.paho.org/en/news/27-1-2021-americas-surpasses-one-million-deaths-covid-19)

# The Apparent 12 Persons behind ~65% of Vaccine Hoaxes (on Facebook, Instagram and Twitter)

According to Imran Ahmed, chief executive officer of the Center for Countering Digital Hate, "The 'Disinformation Dozen' produce 65% of the shares of anti-vaccine misinformation on social media platforms [1](https://252f2edd-1c8b-49f5-9bb2-cb57bb47e4ba.filesusr.com/ugd/f4d9b9_b7cedc0553604720b7137f8663366ee5.pdf). They identified the accounts to be (with their Twitter follower counts as of Nov 30th);

* [Robert F. Kennedy Jr.](https://twitter.com/RobertKennedyJr) - 355.5K Followers
* [Joseph Mercola](https://twitter.com/mercola) - 343K Followers
* [Christiane Northrup](https://twitter.com/DrChrisNorthrup) - 115.8K Followers
* [Rashid Buttar](https://twitter.com/DrButtar) - 88.9K Followers
* [Erin Elizabeth](https://twitter.com/unhealthytruth) - 55.4K Followers
* [Kelly Brogan](https://twitter.com/kellybroganmd) - 18.6K Followers
* [Sayer Ji](https://twitter.com/sayerjigmi) - 11.4K Followers
* Sherri Tenpenny [Suspended]
* Rizza Islam [Suspended]
* Ty & Charlene Bollinger [Not Found]
* Ben Tapper [Not Found]
* Kevin Jenkins [Not Found]

# Influencial Entities on COVID-19 Policy Approval

* [World Health Organization](https://twitter.com/WHO) - 10.2M Followers
* [Centers for Disease Control & Prevention](https://twitter.com/CDCgov) - 4.4M Followers
* [Tedros Adhanom Ghebreyesus](https://twitter.com/DrTedros) - 1.5M Followers
* [Eric Feigl-Ding](https://twitter.com/drericding) - 632.3K Followers
* [Scott Gottlieb, MD](https://twitter.com/ScottGottliebMD) - 522.5K Followers
* [Pfizer](https://twitter.com/pfizer) - 469.9K Followers
* [Ashish K. Jha, MD, MPH](https://twitter.com/ashishkjha) - 295.6K Followers
* [Dr. Tom Frieden](https://twitter.com/DrTomFrieden) - 245.2K Followers
* [Florian Krammer](https://twitter.com/florian_krammer) - 242.1K Followers
* [Isaac Bogoch](https://twitter.com/BogochIsaac) - 149.1K Followers
* [Moderna](https://twitter.com/moderna_tx) - 137.1K Followers

# Network Analysis
## Networks
directed graph (mention network and retweet network)
## Methods
connected components
pruning
closeness centrality 
community detection
* louvain modularity optimization
* label proprogation algo
* surprise community detection
* leiden community detection
* Walktrap Community Detection
* infomap
bridge nodes

## Community Detection
https://towardsdatascience.com/community-detection-algorithms-9bd8951e7dae
https://www.kernix.com/article/community-detection-in-social-networks/
https://graphsandnetworks.com/community-detection-using-networkx/

### Existing Solutions
https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255
https://towardsdatascience.com/how-isis-uses-twitter-598c2eb188a2

http://journal.unipdu.ac.id:8080/index.php/register/article/view/1595
http://journal.unipdu.ac.id:8080/index.php/register/article/download/1595/pdf

[Community detection in node-attributed social networks: A survey](https://pdf.sciencedirectassets.com/276226/1-s2.0-S1574013720X00037/1-s2.0-S1574013720303865/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjECgaCXVzLWVhc3QtMSJGMEQCIG71e2FmklZX9jqKM%2FZ5nedTYkyXEW30w%2B%2BXDN7%2BPX07AiA5NaFHeGVAUZGyX6vcsX9PfkKeLQ8S8J3DH%2BJP8V200SqDBAjx%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAQaDDA1OTAwMzU0Njg2NSIMo%2B1mWifF3Xq71JLEKtcDIfLB650QObs9hPQKGSWEL9eg2zFjCnOVj068j5S2VAPidT5h9sunKLFx68gOUSy10e8zwHjIpoGF65FZsx2laBYJn4zbY33u3Kdloxs7TaeZQ56pDrQnZ38k3%2Blgx4Rm%2FgjEOk4CLi6W%2F7rYn76a1LA1c2%2BjIR33rpBICrGsyx9twlmXNIiq2lX9gXhEtHTqPp3OTMMvPqoxUbO2JIBThdcLqXA4blzQ04Oc48vHuBR4WiWLuaChbyb6BfTY9YF3oOXjM4qC702M5UOF4GeUy%2BURCSqf6f3%2BMo1V20FZyNP%2BsmS0sfdK5%2FGXY8JCncAeO95eW1OYbiY1vbLjZZfZcFgC5jL5zKjNPHztu73lHB%2FoYuJINfhvQ5GSOo5juTKewnwyy5ti2ASRRNDd%2Baxh%2FKqf7StuyZuWB4gVLMrF%2B2F3lRJxtKvuiFga8wiOxh4ouzQFEsJLT67yTvgnMS5k4imnN%2FdzILmmOUT8787ym9kTwGUXobzepO6nhbxdme2X3eqDjTO3ZM51BMCXCCzBkXku02EqWsSERr9TKQ8ZtSIj1AjYvzj34oQ11J%2BXa882zAd5jcMBxWd2fpsNid%2FjlSloSO0WDO%2B7QTUz3y5mjvD2Gd3hcZXyMMeUmY0GOqYBomEaJJz8QrjdEHrnFNDC2uiKXYrCqRjWICNsPNnZ144laF75L6G5fAdowXmmFYNtTG3nlS%2FDbIWxG5Fix65V9dEqt%2Fb76ptBuBtAHYGzmolNE5DPhTbOBRX7bcaAT3AS5egxAxTgh0nIa8DqOmHQQpwrlQx%2BxlTiY961iHZ2Ykdls9lx3yxxCg93AJI1pTlemEqQWrZMTQd8ibDhNc4K7jv7X5SHxw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20211130T165642Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYXIBYC7TD%2F20211130%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=2720fd8a74216c557d2991ecdaeafed5f9e6f7267db92777d8282daa71beea85&hash=9905ae7f822b2dd02f5dfe4e886a70aa4528d15802758d973489153fe2081b8d&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1574013720303865&tid=spdf-a1a55a2c-77eb-4704-a42c-b7a2d781d0bb&sid=ff1d39bb1d0ef54cbe0bab09a7a7ac377c2bgxrqa&type=client)

https://github.com/MieszkoMakuch/twitter-community-detection
https://github.com/joan1971/twitter-community-detection-1

## Papers
### community detection for the twittersphere during kavanaugh hearings
in this paper, mentions and retweets are mainly unidirectional so networks used were undirected

# Tools
## Gephi
https://medium.com/@Luca/guide-analyzing-twitter-networks-with-gephi-0-9-1-2e0220d9097d