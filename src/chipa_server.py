#!/usr/bin/env python3

"""Version of Chipa that speaks fiforpc."""

import os
import preprocessing

SERVER_TO_CLIENT_PATH = "/tmp/server_to_client.fifo"
CLIENT_TO_SERVER_PATH = "/tmp/client_to_server.fifo"

def init_fifos():
    os.remove(SERVER_TO_CLIENT_PATH)
    os.remove(CLIENT_TO_SERVER_PATH)

    if not os.path.exists(SERVER_TO_CLIENT_PATH):
        os.mkfifo(SERVER_TO_CLIENT_PATH)
    if not os.path.exists(CLIENT_TO_SERVER_PATH):
        os.mkfifo(CLIENT_TO_SERVER_PATH)

def send_response(s):
    ## response should be tab-separated and include...
    ## sentence, index, translation, score
    with open(SERVER_TO_CLIENT_PATH, "w") as outfile:
        print(s, file=outfile)

def get_argparser():
    parser = argparse.ArgumentParser(description='chipa_server')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

def main():
    init_fifos()

    print("OK serving forever.")
    while True:
        line = ""
        with open(CLIENT_TO_SERVER_PATH, "r") as c2s:
            line = c2s.readline()
            line = line.strip()
        print("Received: " + line)
        sentence, index, translation = line.split('\t')
        index = int(index)

        preprocessed = preprocessing.preprocess(sentence, "es")
        send_response(line + '\t' + str(len(line)))

if __name__ == "__main__": main()
