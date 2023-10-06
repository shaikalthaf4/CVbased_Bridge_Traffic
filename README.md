# CV based Real-Time Bridge People Detection and Visualization 
![Sample Bridge traffic monitoring on UIUC SmartBridge](bridge_anim.gif)
This repository contains Python scripts for real-time people detection and visualization for Bridge Traffic monitoring using the OpenPifPaf library. The project allows real-time pose detection on video streams and provides options to visualize these detections both in the video feed and in a plan view.

## Features
- Real-Time Pose Detection: Detects people in real-time video streams from an RTSP source.
- Facial Privacy Option: Provides an option to blur facial features for privacy concerns.
- Plan View Visualization: Visualizes the detected poses on a plan view image, offering a top-down perspective of the scene.

## Setup and Installation
### Prerequisites
- Python 3.6 or higher
- Ensure you have a working webcam or RTSP video source configured.

### Installation
```python
pip install -r requirements.txt
```
# Usage
## Real-Time Pose Detection
To run real-time pose detection in the video feed:
```
python main.py
```
By default, facial privacy is enabled. You can disable it by modifying the FACIAL_PRIVACY variable in main.py.

# Configuration
- main.py: Entry point of the application. Configure RTSP settings, image paths, and other parameters in this file.
- real_time_stream.py: Contains the RealTimeStream class, which handles real-time pose detection and plan view visualization.
- uiuc_my_540_30.png: UIUC banner image for overlay in the video feed.
- bridge_plan_new.png: Plan view image for visualizing detections.
- video_run_v1.avi: Video file for detection visualization.
- sstl_static.png: Static image for visualization in the plan view.
- requirements.txt: Contains the list of required packages and their versions.

# Customization
- Modify the RTSP settings in real_time_stream.py to use your specific video source.
- Adjust the plan view coordinates and images according to your setup in real_time_stream.py.

# License
This project is licensed under the MIT License.


