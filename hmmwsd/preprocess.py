#!/usr/bin/env python3

def get_argparser():
    parser = argparse.ArgumentParser(description='preprocess')
    parser.add_argument('--lang', type=str, required=True)
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    assert args.lang in ["es", "gn"]

    lang = args.lang
    infn = args.infn
    outfn = args.outfn

if __name__ == "main": main()
