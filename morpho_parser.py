#!/usr/bin/python3
# -*- coding: utf-8 -*-

#==========================================================================

import argparse
import os
import re
import sys

#==========================================================================

def ParseArgs():
    parser = argparse.ArgumentParser(description="""This script special for Alina.""")
    parser.add_argument('-i', '--input_path',     help='Path to the input file with iw_cas_config_compiler output')
    parser.add_argument('-o', '--output_path',    help='Path to the result file')

    args = parser.parse_args()

    if not args.input_path or not args.output_path:
        parser.print_help()
        sys.exit(2)

    return args

def ReadCasConfigCompilerOutput(path):
    if not os.path.exists(path):
        print("iw_cas_config_compiler out file not found")
        return dict()

    morpho_dict = dict()
    with open(path, "r") as file:
        forms = set()
        current_key = ""
        for line in file:
            m = re.search("^Token: \'.*\'", line)
            if m:
                if current_key:
                    morpho_dict[current_key] = forms
                m = re.search("\'.*\'", line)
                if m:
                    current_key = m.group(0)[1:-1]
                    forms = morpho_dict.get(current_key, set())

            m = re.search("^Add Form \'.*\'", line)
            if m:
                m = re.search("\'.*\'", line)
                if m:
                    form = m.group(0)[1:-1]
                    forms.add(form)
    if current_key:
        morpho_dict[current_key] = forms

    return morpho_dict

def WriteResults(morpho_dict, path):
    with open(path, "w") as file:
        for key in morpho_dict.keys():
            forms = morpho_dict[key]
            forms.add(key)
            for form in forms:
                file.write(form + "\n")

#==========================================================================

def main():
    args = ParseArgs()

    print ""
    print "*************************************************"
    print ""
    print "Configuration:"
    print " -  input_path     = %s" % args.input_path
    print " -  output_path    = %s" % args.output_path
    print ""

    morpho_dict = ReadCasConfigCompilerOutput(args.input_path)
    WriteResults(morpho_dict, args.output_path)

    print "*************************************************"
    print ""

if __name__ == "__main__":
    main()

