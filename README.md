# Infrared internal defect intelligent detection system based on TWR

The infrared internal defect intelligent detection system based on TWR is a software specially used for the internal defect detection of materials. Its main functions include:
1) **Read temperature data file**: Support.dat format infrared temperature data file import.
2) **Display raw infrared images**: Display imported raw infrared images for users to view and analyze.
3) **Draw ROI regions **: Users can draw regions of interest (ROI) on the image for detailed analysis.
4) **Flaw feature extraction based on infrared Thermal Wave Radar (TWR)** : including time-delay feature extraction and phase feature extraction.
5) **Intelligent defect detection based on [YOLOv10]([THU-MIG/yolov10: YOLOv10: Real-Time End-to-End Object Detection (github.com)](https://github.com/THU-MIG/yolov10))**: Deep learning model is used for defect identification and detection.
6) **Count the number of defects**: automatically count and display the number of detected defects.
7) **Log printing**: Record the operation logs of the software in real time for subsequent analysis and tracking.

# GIF Presentation
<center><img src=".\data\img\twrD&E.gif" style="zoom: 100%" /></center>

# Installation

`conda` virtual environment is recommended.

```
conda create -n twrdetect python=3.9
conda activate twrdetect
pip install -r requirements.txt
```

# How To Run

```
1. Run twr.py
```