from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import re
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("-s","--SourceDir", type=str,
                    help="directory for test raw samples",
                    default = 'rec')

args = parser.parse_args()
PicPath = args.SourceDir

Files = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f))]

for Fic in Files:
    g_loss = []
    d_loss = []
    fo = open(Fic)
    while 1:
        lines = fo.readlines(10000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                if re.match(r'^Epoch',line):
                    kline = line.replace(' ','')
                    kline = klinelace(':',',')
                    kline = kline.split(',')
                    d_loss.append(float(kline[-3]))
                    g_loss.append(float(kline[-1]))
    plt.figure()
    plt.plot(d_loss, 'ro', label='d_loss')
    plt.plot(g_loss, 'go', label='g_loss')
    plt.legend()
    plt.title(Fic)
    plt.show()