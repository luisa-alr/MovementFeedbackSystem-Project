import pickle as pkl
import argparse
import csv 
import pandas as pd

parser = argparse.ArgumentParser(description='cat pickled LSL streams.')
parser.add_argument("stream", type=str, help='pickled LSL streams to cat')
args = parser.parse_args()

with open(args.stream, 'rb') as fr:
    try:
        while True:
            tmp = pkl.load(fr)
            with open('Hydra7.csv', 'w', newline='') as out:
                writer = csv.writer(out)
                writer.writerow(['Time Stamp', 'Acc x', 'Acc y', 'Acc z'])
                for i in tmp:
                     writer.writerow(i)
            for element in tmp:
                print(str(element))
            #print("---------------------------------")
    except EOFError:
        pass