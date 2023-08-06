#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def extract_info(absolute_path_of_file):
    
    df = pd.read_csv(absolute_path_of_file)
    print("Shape of the loaded data file is\n", df.shape)
    print("\nColumn names are\n", df.columns)
    print("\nDescription of the data file\n", df.describe())    

    print("\n\n-----Basic Information has been extracted-----")





