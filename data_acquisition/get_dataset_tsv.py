import gzip
import shutil
import os
import wget
from shutil import copyfile
import argparse

url_example = 'https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/2021-01-20/2021-01-20-dataset.tsv.gz?raw=true'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action='help', default=argparse.SUPPRESS, help=f'Use --dataset_url flag OR --date flag')
parser.add_argument("--date", help="A date formatted like 2021-01-20")
parser.add_argument("--dataset_url", help=f'Github link to dataset tsv file like {url_example}')
args = parser.parse_args()
if args.date is None and args.dataset_url is None:
    parser.error("Please add 'dataset_url' or 'date' argument")

raw_w_retweets = f'https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/{args.date}/{args.date}-dataset.tsv.gz?raw=true'
link = args.dataset_url if args.dataset_url is not None else raw_w_retweets
data_tsv_path = './data/tsv/'
tarball = wget.download(link, out=data_tsv_path)
tsv = tarball[:-3]

with gzip.open(tarball, 'rb') as f_in:
    with open(tsv, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.unlink(tarball)