#!/usr/bin/env python3

import os

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
    with open(SERVER_TO_CLIENT_PATH, "w") as outfile:
        print(s, file=outfile)

def main():
    init_fifos()

    print("OK serving forever.")
    while True:
        line = ""
        with open(CLIENT_TO_SERVER_PATH, "r") as c2s:
            line = c2s.readline()
            line = line.strip()
        print("Received: " + line)
        send_response(line + '\t' + str(len(line)))

if __name__ == "__main__": main()
