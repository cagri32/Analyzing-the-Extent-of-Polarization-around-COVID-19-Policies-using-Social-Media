import networkx as nx
import pickle
import constants

def export(filepath):
    conversion_filenames = [
        "community1graph",
        "community2graph",
        "mainGraphUndirected",
    ]
    graph = nx.DiGraph()

    for filename in conversion_filenames:
        print("exporting " + filepath + filename)
        with open(filepath + filename + ".txt", 'rb') as f:
            pickled_graph = pickle.load(f)
            graph.update(pickled_graph)
            nx.write_gml(graph, filepath + filename + ".gml")
            print('... Done.')

def main():
    input_string = input("Enter a date in the format yyyy-mm-dd or 'all': ")

    if input_string == 'all':
        for date in constants.date_list:
            export(constants.data_path + date + "/")
    else:
        date = input_string
        export(constants.data_path + date + "/")
    
if __name__ == "__main__":
    main()
    print("export_to_gml.py... Done.")
