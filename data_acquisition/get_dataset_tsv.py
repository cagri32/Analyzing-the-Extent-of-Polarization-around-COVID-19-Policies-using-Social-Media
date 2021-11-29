import gzip
import shutil
import os
import wget
import csv
import linecache
from shutil import copyfile
import sys
import argparse

# TODO - convert date like 2021-07-01 to dataset_url 
# TODO - flag for dataset and clean-dataset

url_example = 'https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/2021-01-20/2021-01-20-dataset.tsv.gz?raw=true'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action='help', default=argparse.SUPPRESS, help=f'Use --dataset_url flag OR --date flag')
parser.add_argument("--date", help="A date formatted like 2021-01-20")
parser.add_argument("--dataset_url", help=f'Github link to dataset tsv file like {url_example}')
args = parser.parse_args()
if args.date is None and args.dataset_url is None:
    parser.error("Please add 'dataset_url' or 'date' argument")

#Downloads the dataset (compressed in a GZ format)
#!wget dataset_URL -O clean-dataset.tsv.gz
raw_w_retweets = f'https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/{args.date}/{args.date}-dataset.tsv.gz?raw=true'
link = args.dataset_url if args.dataset_url is not None else raw_w_retweets
data_tsv_path = './data/tsv/'
tarball = wget.download(link, out=data_tsv_path)
tsv = tarball[:-3]
# wget.download(args.dataset_url, out='clean-dataset.tsv.gz')

#Unzips the dataset and gets the TSV dataset
with gzip.open(tarball, 'rb') as f_in:
    # with open('clean-dataset.tsv', 'wb') as f_out:
    with open(tsv, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

#Deletes the compressed GZ file
os.unlink(tarball)

filtered_language = 'en'

# #If no language specified, it will get all records from the dataset
# if filtered_language == "":
#   copyfile('clean-dataset.tsv', 'clean-dataset-filtered.tsv')

# #If language specified, it will create another tsv file with the filtered records
# else:
#   filtered_tw = list()
#   current_line = 1
#   with open("clean-dataset.tsv") as tsvfile:
#     tsvreader = csv.reader(tsvfile, delimiter="\t")

#     if current_line == 1:
#       filtered_tw.append(linecache.getline("clean-dataset.tsv", current_line))

#       for line in tsvreader:
#         if line[3] == filtered_language:
#           filtered_tw.append(linecache.getline("clean-dataset.tsv", current_line))
#         current_line += 1

#   print('\033[1mShowing first 5 tweets from the filtered dataset\033[0m')
#   print(filtered_tw[1:(6 if len(filtered_tw) > 6 else len(filtered_tw))])

#   with open('clean-dataset-filtered.tsv', 'w') as f_output:
#       for item in filtered_tw:
#           f_output.write(item)