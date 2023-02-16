"""
Created on Wed Jan 12 10:09:15 2023
Simple I/O routines.

"""
import requests
import spacepy.pycdf as cdf
import urllib

# Check if CDF existon the local hard drive

def file_exists(location):
    request = requests.head(location)
    return request.status_code == requests.codes.ok

# Download the CDF file from URL

def cdfDownload(url, cdfVersions, scFilePath):
    for ii in range(len(cdfVersions)):
        if file_exists(url + cdfVersions[ii] + '.cdf'):
            print('Downloading...')
            urllib.request.urlretrieve(url + cdfVersions[ii] + '.cdf', scFilePath)
            break
        else:
            continue
    return print("Download complete! Created file: " + scFilePath)

# Read ASCII file from path

def io(path):
  file = open(path,'r')
  data = file.readlines()
  file.close()
  return data
