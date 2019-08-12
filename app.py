from flask import Flask
from flask import request as req
from functions import *

app = Flask(__name__)

@app.route('/segmentation', methods=['GET'])
def Function():
	url = req.args.get('url')
	THRESHOLD = req.args.get('threshold')
	points = parse_url(url)
	ground_points, non_ground_points = getGround_World(points, float(THRESHOLD))
	ground_points = changeIntensity(ground_points, GROUND_COLOR)
	non_ground_points = changeIntensity(non_ground_points, NON_GROUND_COLOR)
	points = np.concatenate((ground_points, non_ground_points))
	sensor_url = getSensor_url(points, DESTPATH, url)
	print(sensor_url)
	return sensor_url
  
 
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)    
