#! /usr/bin/env python

from pylingva import pylingva
import argparse

def translate():
    translate = pylingva()
    arg = argparse.ArgumentParser()
    arg.add_argument("-s", "--source", type=str, help="Source Language to translate")
    arg.add_argument("-t", "--target", type=str, help="Target Language to translate")
    arg.add_argument("-txt", "--text", type=str, help="Text to translate")
    arg.add_argument("-ll", "--list-languages",  help="List Languages support", action="store_true")
    args = arg.parse_args()

    if args.list_languages:
        lang = translate.languages()
        print("{:<25} {:<25}".format('Name', 'Code'))
        for key, value in lang.items():
            x = key
            y = value
            print("{:<25} {:<25}".format(x, y))
    else:
        result = translate.translate(args.source, args.target, args.text)
        print(result)
