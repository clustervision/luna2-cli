# mytool.py
import argcomplete
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("action", choices=["start", "stop", "restart"])
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()
