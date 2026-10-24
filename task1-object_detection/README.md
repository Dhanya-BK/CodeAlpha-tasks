# CodeAlpha_ObjectDetectionTracking
Real-time object detection with **YOLOv8** and multi-object tracking with **Deep SORT**. Each object gets a label and a persistent tracking ID.

## Run
```bash
pip install -r requirements.txt
python detect_track.py                       # webcam
python detect_track.py --source video.mp4 --save output.mp4
```
Press `q` to quit.
