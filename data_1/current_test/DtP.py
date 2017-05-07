from __future__ import division
import os 
import re
import copy
import numpy as np
from PIL import Image
from scipy import misc


recmax = open('1_max').readline().strip().split(',')
recmax = np.array(recmax)
recmax = recmax.astype(np.float)
maxrecmax = np.amax(recmax)

i = 0
for line in open('1_s_4'):
    line = line.strip().split(',')
    line = np.array(line)
    line = line.astype(np.float)
    print(line)
    line1 = line*255.0/maxrecmax
    print(line1)
    linemin = np.amin(line1)
    linemax = np.amax(line1)
    #if linemax > 200:
    print(str(i) + ': min- ' + str(linemin) + ' max- ' + str(linemax))
    line3 = line1.astype(np.uint8)
    linemin = np.amin(line3)
    linemax = np.amax(line3)
    print(str(i) + ': min- ' + str(linemin) + ' max- ' + str(linemax))

    line3 = np.reshape(line3, (2,541))
    im = Image.fromarray(line3)
    im.save(os.path.join('1_s_4_p',str(i) + '.png'))

    i = i + 1
    #raw_input('...')
print('end')
