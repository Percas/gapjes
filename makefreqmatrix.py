#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:29:54 2018
Purpose: make a frequency dataframe vars x years
    from the varfrequency files in a directory. The matrix gives the number
    of times the variable is used in that year.
    VARNAAM, all, 2016, 2017,
    RINPERSOON, xxx, xxx, xxx,
    RINPERSOONS, xxx, xxx, xxx

    also for every variable the owner is added from Varinfo.csv
@author: anton
"""
# ################ Imports #############################
import os
import sys
import pandas as pd
# import re

# ################ Constants ##########################
basedir = "/home/anton/PycharmProjects/gapvar/"
otapdir = basedir

dataindir = otapdir + "data/out1_varfreq/"
allvarfreqfile = dataindir + "all.txt"
varinfofile = otapdir + "data/varlistdir/Varinfo.csv"
destdir = otapdir + "data/out2_varyearfreq/"


# ################# Functions #########################


def checkexist(fdlist):
    # exit if a file or directory in fdlist does not exist
    for d in fdlist:
        if not os.path.exists(d):
            print("checkexist: ", d, " does not exist")
            sys.exit("Exciting...")


def readyears(dataindir):
    # in dataindir there should be a number of directories respresenting the
    # years 2010, 2011, etc. This function returns the years in a list.
    _years = []
    for _f in sorted(os.listdir(dataindir)):
        if _f.startswith("2"):      # this can be improved with re: tbd
            _f1, _f2 = os.path.splitext(_f)
            _years.append(_f1)
    return _years

# ################ Main ###########################


checkexist([dataindir, otapdir, destdir, allvarfreqfile, varinfofile])
varinfo = pd.read_csv(varinfofile, sep=';')
varyearfreqmatrix = pd.read_csv(allvarfreqfile)
varyearfreqmatrix = pd.merge(left=varyearfreqmatrix,
                             right=varinfo,
                             how='left',
                             on='VARNAAM')
years = readyears(dataindir)
for year in years:
    r = pd.read_csv(dataindir+year+".txt")
    varyearfreqmatrix = pd.merge(left=varyearfreqmatrix,
                                 right=r,
                                 how='left')
varyearfreqmatrix.to_csv(destdir+"varyearfreqmatrix.csv")
print("varyearfreqmatrix.csv written in dir", destdir)
