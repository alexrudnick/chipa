#!/usr/bin/env python3

import random

def main():
    with open("source.txt", "w") as source, open("target.txt", "w") as target:
        for sent_num in range(1000):
            source_sent = []
            target_sent = []
            for i in range(random.randint(5,20)):
                word = random.randint(1, 100)
                source_sent.append("s{0}".format(word)) 
                target_sent.append("t{0}".format(word)) 
            print(" ".join(source_sent), file=source)
            print(" ".join(target_sent), file=target)

if __name__ == "__main__": main()
