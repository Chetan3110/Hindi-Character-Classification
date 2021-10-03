import random
import json
# from utils.io import write_json

def write_json(filename, result):
    with open(filename, 'w') as outfile:
        json.dump(result, outfile)

def read_json(filename):
    with open(filename, 'r') as outfile:
        data =  json.load(outfile)
    return data

def generate_sample_file(filename):
    res = {}
    for i in range(1,100):
        test_set = str(i) + '.png'
        res[test_set] = 3

    write_json(filename, res)

if __name__ == '__main__':
    generate_sample_file('./sample_result1.json')
