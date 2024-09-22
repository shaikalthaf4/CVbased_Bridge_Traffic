# 🚀 CV-based Real-Time Bridge People Detection and Visualization 
![Bridge Traffic Monitoring on UIUC SmartBridge](bridge_anim_view.gif)

This repository showcases an advanced real-time people detection system designed for bridge traffic monitoring, leveraging state-of-the-art computer vision (CV) techniques. The system utilizes the OpenPifPaf library to detect and visualize people in both video streams and plan view, offering innovative solutions for monitoring traffic on bridges.

## 🌟 Key Features
- **Real-Time Pose Detection**: Detect people and poses in real-time from video streams (webcams, RTSP, etc.), enhancing safety and monitoring on bridges.
- **Facial Privacy Protection**: Automatically blurs facial features in the video stream for privacy-conscious deployments, ensuring ethical use in public areas.
- **Plan View Visualization**: Provides an intuitive top-down perspective of the detected poses over a plan view image, offering a bird’s-eye view of the bridge traffic.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.6 or higher
- OpenPifPaf installed
- A working RTSP source or webcam for video feed input

### Installation
Clone the repository and install dependencies:
```
git clone https://github.com/your-username/bridge-people-detection.git
cd bridge-people-detection
pip install -r requirements.txt
```
## 🚴‍♂️ Usage
# Real-Time Pose Detection
Run the real-time pose detection system on your video stream:
```
python main.py
```
- Facial Privacy: Enabled by default. To disable, simply modify the FACIAL_PRIVACY variable in main.py.
- RTSP Source Configuration: Customize the RTSP settings in real_time_stream.py to match your specific video source.

# Plan View Visualization
Visualize detected poses on a plan view of the bridge for better traffic monitoring insights.

## ⚙️ Configuration
```
main.py: The entry point for running the application. Configure paths, RTSP settings, and parameters.
real_time_stream.py: Handles the real-time pose detection logic and plan view visualization.
Images & Videos: The repository includes various assets for visualization:
uiuc_my_540_30.png: UIUC banner image for overlay.
bridge_plan_new.png: Plan view image for top-down visualization.
video_run_v1.avi: Sample video file for detection visualization.
sstl_static.png: Static image used for plan view visualization.
```
## 🎨 Customization
- RTSP Settings: Modify the RTSP URL and related parameters in real_time_stream.py to use your video source.
- Plan View Configuration: Adjust plan view coordinates to match your bridge setup by editing real_time_stream.py.

## 🧠 Why This Project Matters
This system provides an efficient solution for monitoring human traffic on bridges in real-time, with use cases in:

- **Urban Traffic Monitoring**: Analyze pedestrian activity for infrastructure planning and safety measures.
- **Smart Cities & IoT**: Integrate with other smart systems for automated incident detection and reporting.
- **Research & Academia**: Contribute to studies on human movement patterns in public spaces, improving safety and efficiency.

## 📄 License
This project is licensed under the MIT License, enabling free use, modification, and distribution.
