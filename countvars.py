#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: Wed Jun 13 21:41:23 2018
@author: anton
Purpose:
1. count the frequency of SSB variables as defined in the GAP
(SSB=Stelsel van Sociaal Statische Bestanden, GAP = Globaal Analyse Plan)
Input:
    1. Base directory that contains subdir with years. In every year
    subdir there are GAP files converted tot txt of that year.
    2. List of variables to be searched for in a GAP
Output: frequency count of the SSB variables of the GAPs of a certain year,
    or all years, saved in a file and printed with matplotlib
"""

# ################ Imports #############################
import os
import sys
from collections import Counter
import matplotlib.pyplot as plt
import spacy
nlp = spacy.load('nl_core_news_sm')

# ################ Constants ##########################
basedir = "/home/anton/PycharmProjects/gapvar/"
otapdir = basedir
dataindir = otapdir + "data/GAP.txt1/"
year = "all"
# year = all, then cycly through all the years in basedir, otherwise if
# year = 2013, take only the GAP's from that subdir.
# the varlistfile.txt contains all the variables that are present in the SSB
varlistfile = otapdir + "data/varlistdir/varlist.txt"
destdir = otapdir + "data/out1_varfreq/"
maxvar = 200
# in the output the variables are sorted on descending frequency
# maxvar is the max number of variables we show in the output
mingapvar = 4
# a rather crude way to identify a suspicious GAP: print it if
# it has less then mingapvar SSB-variables
# ################# Functions #########################


def checkexist(fdlist):
    # exit if a file or directory in fdlist does not exist
    for d in fdlist:
        if not os.path.exists(d):
            print("checkexist: ", d, " does not exist")
            sys.exit("Exciting...")


def printsuspiciousgap(gapfile, nrofgapvars, min_var):
    # print GAP's that have few SSB-vars. They are likely candidates for
    # investigation
    if nrofgapvars < min_var:
        print("printsuspiciousgap: ", gapfile, ": aantal var:", nrofgapvars)


def getsubs(ddir):
    # return a list of subdirectories in dir
    return [ddir + _s for _s in sorted(os.listdir(ddir))]


def getfiles1deep(ddir):
    # return a list of files one level below ddir
    return [_d + '/' + _f for _d in getsubs(ddir) for _f in os.listdir(_d)]


def makefilelist(ddir, year):
    # return the list of the files to be processed. These are the files in
    # the subdir year of dir unless year = all, in which case we return
    # the files in all the subdirs of ddir
    if year == "all":
        return getfiles1deep(ddir)
    else:
        return [ddir + year + '/' + _f for _f in os.listdir(ddir + year)]


def makefreqtable(filelist, varlist):
    # Put for every variable in every file in filelist all those variables
    # in one big list (a bag of vars). Then return the variable frequencies
    # of that bag
    _varbag = []
    for _f in sorted(filelist):
        _doc = nlp(open(_f).read())
        _words = set(_token.text for _token in _doc)
        # print(_words)
        _doorsnede = _words & varlist
        # print(_doorsnede)
        printsuspiciousgap(_f, len(_doorsnede), mingapvar)
        _varbag.extend(_doorsnede)
    return Counter(_varbag).most_common()


def savevarfreq(varfreq, ddir, year):
    # save the dict varfreq in a file named year.txt in ddir
    _varfile = open(ddir+year+".txt", 'w')
    _varfile.write("VARNAAM, "+year+"\n")
    for key, item in varfreq:
        _varfile.write(key + ", " + (str(item)+"\n"))
    _varfile.close()


def plotfreqtable(values):
    plt.plot(values[2:maxvar])
    # this is a bit ugly: we leave out the two variables RINPERSOON and
    # RINPERSOONS that are almost always used
    plt.ylabel('GAP variabelen frequentie')
    plt.show()

# ################## Main ##############################


checkexist([basedir, otapdir, dataindir, destdir, varlistfile])
gapfilelist = makefilelist(dataindir, year)
varlist = set(open(varlistfile).read().split())
varfreq = makefreqtable(gapfilelist, varlist)
savevarfreq(varfreq, destdir, year)
plotfreqtable([values for key, values in varfreq])
