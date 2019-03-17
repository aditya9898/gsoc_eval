import h5py
import numpy as np
import os
from datetime import datetime
from pytz import timezone
import csv
import scipy
from scipy import signal
import matplotlib.pyplot as plt


for file in os.listdir():
    if file.endswith('.h5'):
        fname=file
#fname=1541962108935000000_167_838.h5
print('\nfile name is : ',fname)



# CONVERTING TIMESTAMP TO UTC AND CET(CENTRAL EUROPIAN TIME) TIME
nano=int(fname[:19])
print('time stamp in nanoseconds : '+str(nano))

def nano_to_std(nano): #function to convert timestamp to utc and europian central time
    utc=datetime.utcfromtimestamp(int(nano//1e9))
    cet=utc.astimezone(timezone('CET'))
    return [utc,cet]


[utc,cet]=nano_to_std(nano)
print('time in utc:',utc)
print('time in cern local time(cet):',cet)


# TRAVERSING THE HDF5 FILE SYSTEM AND SAVING THE DATA ONTO A CSV NAMED 'datasetinfo.csv'
file=h5py.File(fname,'r')
file

def dataset_iterator(g): #function to recursively traverse through the hdf5 directory
    for f in list(g.keys()):
        if isinstance(g[f],h5py.Group):
            yield from dataset_iterator(g[f])
        if isinstance(g[f],h5py.Dataset):
            yield f,g[f].name

header_row=['name','path','size','shape','dtype']
with open('datasetinfo.csv','w') as f:
    cw=csv.writer(f)
    cw.writerow(header_row)
    for ds_name,path in dataset_iterator(file):
        try:
            size=file[path].size
            shape=file[path].shape
            dtype=str(file[path].dtype)
            cw.writerow([ds_name,path,size,shape,dtype])
        except Exception:
            pass
print('\ndataset info saved as datasetinfo.csv \n')

# CONVERTING 1D IMAGE INTO 2D AND SAVING AS A PNG
path='/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'
heightpath='/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight'
widthpath='/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth'

img1d=np.array(file[path])
h=np.array(file[heightpath])[0]
w=np.array(file[widthpath])[0]

img2d=img1d.reshape(h,w)
img2d=scipy.signal.medfilt(img2d)
plt.imshow(img2d)

plt.imsave('image.png',img2d)
print('image saved as (image.png)')