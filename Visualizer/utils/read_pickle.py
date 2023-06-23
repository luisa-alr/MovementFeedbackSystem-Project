import pickle
import argparse

parser = argparse.ArgumentParser(description='cat pickled LSL streams.')
parser.add_argument("stream", type=str, help='pickled LSL streams to cat')
args = parser.parse_args()

with open(args.stream, 'rb') as fr:
    try:
        while True:
            tmp = pickle.load(fr)
            for element in tmp:
                print(str(element))
            #print("---------------------------------")
    except EOFError:
        pass