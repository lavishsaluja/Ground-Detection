import urllib
import copy
import requests
import pandas as pd
import statistics
import struct
import time
from urllib import request
import numpy as np
from aws_class import AWS

# Replace the ACCESS_KEY, SECRET_ACCESS_KEY variables.
BUCKET = 'YOUR BUCKET NAME HERE'
DESTPATH = 'YOUR FOLDER NAME HERE'
ACCESS_KEY = 'YOUR ACCESS_KEY TO S3 BUCKET HERE'
SECRET_ACCESS_KEY = 'YOUR SECRET_ACCESS_KEY TO S3 BUCKET HERE'
aws = AWS(access_key=ACCESS_KEY, secret_key=SECRET_ACCESS_KEY)


# VALUES FOR GROUND_POINTS COLOR & NON_GROUND_POINTS COLOR
GROUND_COLOR = 0
NON_GROUND_COLOR = 1

def parse_bin_data(url):
    '''
    parse bin file with lidar data to numpy array
    :param url: the s3 url to point cloud data
    '''
    points = []
    res = requests.get(url)
    if (res.status_code == 200):
        # print('fetching new lidar data...')
        bin_content = res.content
        if (res.status_code == 200):
            line_width = 16
            for lindex in  range(0, int(len(bin_content) / line_width)):
                points.append([struct.unpack('f', bin_content[lindex * line_width:(lindex * line_width) + 4])[0],
                               struct.unpack('f', bin_content[lindex * line_width + 4:lindex * line_width + 8])[0],
                               struct.unpack('f', bin_content[lindex * line_width + 8:lindex * line_width + 12])[0]])

    return np.array(points)


def parse_pcd_data(pcd_url):
    '''
    parse pcd file with lidar data to numpy array
    :param pcd_url: the s3 url to point cloud data
    '''
    print('fetching pcd data...')
    points = []
    data_type = ''
    data_reached = False
    data = urllib.request.urlopen(pcd_url).read()
    data = str(data, 'utf-8').split("\n")
    for line in data:
        if ('FIELDS' in line):
            headers = line.split(' ')[1:]
            # print("in field", headers)
        elif ('DATA' in line):
            data_type = line.split('DATA ')[1]
            # print("data", data_type)
            data_reached = True
        elif data_reached:
            if data_type == 'ascii':
                if len(headers) == len(line.split(' ')):
                    point = []
                    for i in range(0, len(headers) - 1, 1):
                        # point[headers[i]] = line.split(' ')[i]
                        point.append(line.split(' ')[i])
                    points.append(point)
            elif data_type == 'binary':
                points = parse_bin_data({'content': line, 'status_code': 200})
    return np.array(points)


def parse_url(url):
    '''
    a generic function to call parse_bin_data and parse_pcd_data
    :param url: the s3_url with point cloud data
    '''
    if(url.rsplit('.', 1)[1] == 'bin'):
        points = parse_bin_data(url)
        return points    
    elif(url.rsplit('.', 1)[1] == 'pcd'):
        points = parse_pcd_data(url)
        return points
    else:
        raise RuntimeError('Only .bin/.pcd file formats are parsed.')


def getGround_World(points, THRESHOLD):
    '''
    filter ground and non_ground points
    :param points array
    :param threshold value (varies between 0.1 to 0.3 generally)
    '''
    xyz = points
    height_col = int(np.argmin(np.var(xyz, axis = 0)))
    
    temp = np.zeros((len(xyz[:,1]),4), dtype= float)
    temp[:,:3] = xyz[:,:3]
    temp[:,3] = np.arange(len(xyz[:,1]))
    xyz = temp
    z_filter = xyz[(xyz[:,height_col]< np.mean(xyz[:,height_col]) + 1.5*np.std(xyz[:,height_col])) & (xyz[:,height_col]> np.mean(xyz[:,height_col]) - 1.5*np.std(xyz[:,height_col]))]
    
    max_z, min_z = np.max(z_filter[:,height_col]), np.min(z_filter[:,height_col])
    z_filter[:,height_col] = (z_filter[:,height_col] - min_z)/(max_z - min_z) 
    iter_cycle = 10
    for i in range(iter_cycle):   
        covariance = np.cov(z_filter[:,:3].T)
        w,v,h = np.linalg.svd(np.matrix(covariance))
        normal_vector = w[np.argmin(v)]
        filter_mask = np.asarray(np.abs(np.matrix(normal_vector)*np.matrix(z_filter[:,:3]).T )<THRESHOLD)
        z_filter = np.asarray([z_filter[index[1]] for index,a in np.ndenumerate(filter_mask) if a == True])

    z_filter[:,height_col] = z_filter[:,height_col]*(max_z - min_z) + min_z
    world = np.array([row for row in xyz if row[3] not in z_filter[:,3]])
    
    return z_filter, world


def getName(url):
    '''
    return the name of file with segmented ground on S3 
    :param url: s3 url with point cloud data
    '''
    return str(url.rsplit('.')[-2].rsplit('/')[-1]) + '.pcd'


def upload(data, DESTPATH, url):
    '''
    upload a pcd file on s3 with segmented ground
    :param data: the data with ground and non_ground_points with different intensity
    :param DESTPATH: the folder on s3 
    '''
    aws.upload_data(BUCKET, bytearray(data, 'utf-8'), DESTPATH + getName(url))   


def get_headers():
    '''
    return headers for the pcd file.
    '''
    return """VERSION 0.7
FIELDS x y z intensity ring
SIZE 4 4 4 4 2
TYPE F F F F U
COUNT 1 1 1 1 1
WIDTH 122006
HEIGHT 1
VIEWPOINT 0.0 0.0 0.0 1.0 0.0 0.0 0.0
POINTS 122006
DATA ascii\n"""


def append_point(point, data):
    '''
    append one point (X, Y, Z INTENSITY) in the data variable.
    :param point: point is (X, Y, Z, INTENSITY)
    :param data: data is collection of points
    '''
    return data + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + ' ' + str(point[3]) + '\n'


def get_lidar_data(points):
    '''
    returns the data generated above after appending all points (X, Y, Z)
    :param points: numpy array with all points generated by parse_url
    '''
    data = ""
    for point in points:
        data = append_point(point, data)
    return data


def getSensor_url(points, DESTPATH, url):
    '''
    return playment's sensorfusiondebugger.com url
    :param points: numpy array with all points generated by parse_url
    :param DESTPATH: the folder
    :param url: the original s3 url with lidar data 
    '''
	headers = get_headers()
	data = get_lidar_data(points)
	data = headers + data
	upload(data, DESTPATH, url)
	s3_url = aws.url(BUCKET, DESTPATH + getName(url))
	sensor_url = 'https://sensorfusiondebugger.netlify.com/?data=' + s3_url
	return sensor_url


def changeIntensity(points, new_intensity):
    '''
    changes the INTENSITY value in (X, Y, Z, INTENSITY)
    :param points: numpy array with all points generated by parse_url
    :param new_intensity: the INTENSITY value that we want to set for the ground or non_ground points.
    '''
	for point in points:
		point[3] = new_intensity
	return points


def PrevFunction(url, THRESHOLD):
    '''
    depreciated function (can be removed later)
    '''
	points = parse_url(url)
	ground_points, non_ground_points = getGround_World(points, THRESHOLD)
	ground_points = changeIntensity(ground_points, GROUND_COLOR)
	non_ground_points = changeIntensity(non_ground_points, NON_GROUND_COLOR)
	points = ground_points + non_ground_points
	sensor_url = getSensor_url(points, DESTPATH)
	return sensor_url
