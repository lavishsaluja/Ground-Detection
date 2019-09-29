#### About?
A Flask based API to detect ground points in a given LiDAR data file that I wrote during my super-cool internship (Summers, 2019) at [Playment](https://playment.io/)

Here is how the magical output looks like:

![alt text](https://github.com/lavishsaluja/Ground-Detection/blob/master/segmented_ground.png)


#### To-do
- [ ] Write function to parse local pcd file and create new pcd on local along with doing it on AWS.
- [ ] Add a requirements.txt file with all the necessary packages so as to ease the setting-up time of project
- [x] Add "how to setup & run" section.


#### setting it up?
1. Enter your AWS KEYS in `functions.py`
2. Install all the dependencies.
3. run `python app.py`
4. visit `0.0.0.0:5000/segmentation?url=YOUR_URL&threshold=YOUR_THRESHOLD` on your browser.


[LICENSE](https://github.com/lavishsaluja/Ground-Detection/blob/master/LICENSE)
