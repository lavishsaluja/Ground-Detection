#### About?
A Flask based API to detect ground points in a given LiDAR data file that I wrote during my super-cool internship (Summers, 2019) at [Playment](https://playment.io/)

Here is how the magical output looks like:

![alt text](https://github.com/lavishsaluja/Ground-Detection/blob/master/segmented_ground.png)


#### To-do
- [ ] Write function to parse local pcd file and create new pcd on local along with doing it on AWS.
- [ ] Add a requirements.txt file with all the necessary packages so as to ease the setting-up time of project
- [ ] Add "how to setup & run" section.
- [ ] Add more To-dos (Lol!)


#### setting it up?
1. Enter your AWS KEYS in `functions.py`
2. Install all the dependencies.
3. run `python app.py`
4. visit `0.0.0.0:5000/segmentation?url=YOUR_URL&threshold=YOUR_THRESHOLD` on your browser.


#### License
MIT License
Copyright (c) 2019 Lavish Saluja

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.