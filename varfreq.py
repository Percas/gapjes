#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: July 22 2018
@author: anton
Purpose:
Make a frequency count of the SSB variables mentioned in GAP's and for Sjoerd:
Generate a file with GAPs and the SSB variables used in a GAP

Input:
    1. Base directory that contains subdir with years. In every year
    subdir there are GAP files converted to txt of that year.
    2. List of variables to be searched for in a GAP
Output:
"""

# ################ Imports #############################
import os
import sys
from collections import Counter
import matplotlib.pyplot as plt
import spacy
nlp = spacy.load('nl')

# ################ Constants ##########################
basedir = "/home/anton/devel/"
otapdir = basedir + "prod/"
dataindir = otapdir + "data-in/GAP.txt1/"
year = "all"
# year = all, then cycly through all the years in basedir, otherwise if
# year = 2013, take only the GAP's from that subdir.
# the varlistfile.txt contains all the variables that are present in the SSB
varlistfile = otapdir + "data-in/varlistdir/varlist.txt"
destdir = otapdir + "data-out/01_varfreq/"
maxvar = 200

# ################# Functions #########################


def checkexist(fdlist):
    # exit if a file or directory in fdlist does not exist
    for d in fdlist:
        if not os.path.exists(d):
            print("checkexist: ", d, " does not exist")
            sys.exit("Exciting...")


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


def make_gapvar(filelist, vset):
    # filelist contains a list of gap files.
    # vset is the set of SSB vars
    # This function returns a dict with gapfilename as key and a set
    # of vars as item.
    # This set of vars contain the SSB vars in the GAP.
    _gapdict = dict()
    for _f in sorted(filelist):
        _doc = nlp(open(_f).read())
        words = list(_token.text for _token in _doc)
        _gapname = _f.split('/')[-1]
        print(_gapname)
        ssbvar = list(get_ssbvar(words, vset))
        ssbvar.insert(0, _f.split('/')[-2]) # add the year as well
        # print(ssbvar)
        _gapdict[_gapname] = ssbvar
    return _gapdict


def get_ssbvar(words, vset):
    # words is a list of words. vset a set of SSB vars
    # get_ssbvar returns a set of the SSB vars found in words.
    # We consider a word an SSB var if:
    #   1. word is in vset OR
    #   2. word.upper() is in vset AND word not in nl vocab OR
    #   3. word.upper() is in vset AND word in nl vocab AND \
    #      previousword.upper() OR nextword.upper() word are in vset
    # note: 3 is not implemented yet
    _wfound = []
    for _word in words:
        if _word in vset or (_word.upper() in vset \
           and _word not in nlp.vocab):
            _wfound.append(_word.upper())
    return set(_wfound)


def dict2freq(adict):
    # adict must be dictionary
    # values of adict must be sets or lists.
    # dict2freq puts all these values in one
    # (big) list, a bag of variables. Then return a frequency count of
    # those variables in that bag, using the Counter method.
    _bag = []
    for key in adict:
        _bag.extend(adict[key])
    return Counter(_bag).most_common()


def savevarfreq(varfreq, ddir, year):
    # save the dict varfreq in a file named year.txt in ddir
    _varfile = open(ddir + year + '.txt', 'w')
    _varfile.write('VARNAAM, ' + year + '\n')
    for key, item in varfreq:
        _varfile.write(key + ', ' + str(item) + '\n')
    _varfile.close()

def savegapvar(gapvar, ddir, year):
    # save the dict gapvar in a file named year.gap.txt in ddir
    _varfile = open(ddir + 'GAP_' + year + '.txt', 'w')
    _varfile.write('GAPNAAM, ' + 'year of GAP, ' + 'list of variables in that GAP' + '\n')
    for _key in gapvar:
        _varfile.write(_key + ',' + ','.join(gapvar[_key]) + '\n')
    _varfile.close()


def plotfreq(values, maxvar):
    plt.plot(values[2:maxvar])
    plt.ylabel('GAP variabelen frequentie')
    plt.show()


# ################## Main ##############################


checkexist([basedir, otapdir, dataindir, varlistfile, destdir])
gapfilelist = makefilelist(dataindir, year)
SSBvarset = set(open(varlistfile).read().split())
gapvar = make_gapvar(gapfilelist, SSBvarset)
varfreq = dict2freq(gapvar)
savevarfreq(varfreq, destdir, year)
savegapvar(gapvar, destdir, year)
values = [v for _, v in varfreq]
plotfreq(values, maxvar)
