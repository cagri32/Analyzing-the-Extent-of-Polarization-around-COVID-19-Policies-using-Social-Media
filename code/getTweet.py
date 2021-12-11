import glob
import pickle
import networkx as nx

# IDs of the Users (Retweeter, Owner of Tweet)
id1 = "1548884455"
id2 = "18831926"

date = "2021-01-27"

inputdir = 'D:\\Users\\Cagri\\Desktop\\YORK\\4414\\Project\\Dataset to be used\\{}\\**\\hydrated_tweets_short.json'.format(date)

# Community Graphs Directories
community1dir = '.\\{}\\community1graph.txt'.format(date)
community2dir = '.\\{}\\community2graph.txt'.format(date)
community3dir = '.\\{}\\community3graph.txt'.format(date)

# Read Communities into graphs
with open(community1dir, 'rb') as f:
        comm1graph = pickle.load(f)      

with open(community2dir, 'rb') as f:
        comm2graph = pickle.load(f)  

with open(community3dir, 'rb') as f:
        comm3graph = pickle.load(f) 

maingraphdir = '.\\{}\\mainGraphUndirected.txt'.format(date)
with open(maingraphdir, 'rb') as f:
        maingraph = pickle.load(f)

if comm1graph.has_node(id1):
    print(id1, " is a member of ProVax")
elif comm2graph.has_node(id1):
    (print(id1, " is a member of AntiVax"))
elif comm3graph.has_node(id1):
    (print(id1, " is a member of Neutral"))

if comm1graph.has_node(id2):
    print(id2, " is a member of ProVax")
elif comm2graph.has_node(id2):
    (print(id2, " is a member of AntiVax"))
elif comm3graph.has_node(id2):
    (print(id2, " is a member of Neutral"))   


filelist = glob.glob(inputdir, recursive=True)

for file in filelist:  
    # opening a text file
    file1 = open(file, "r")
    # setting flag and index to 0
    index = 0
    # Loop through the file line by line
    for line in file1:
        if id1 in line and id2 in line:
            textlist = line.split("\"id_str\": ")
            tweetid = textlist[1].split('"')
            print("ID of who retweeted is:", id1)
            print("ID of the poster of the tweet is:", id2)
            print("The Tweet Link is:")
            print("twitter.com/anyuser/status/{}".format(str(tweetid[1])))
