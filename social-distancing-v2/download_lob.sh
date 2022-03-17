#!/usr/bin/env sh

mkdir -p video

wget -O video/vid0.mp4 -nc "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files=vid0.mp4"
wget -O video/vid1.mp4 -nc "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files=vid1.mp4"  
wget -O video/vid2.avi -nc "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files=vid2.avi"

wget -O models/yolo3_tiny/n.weights -nc "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files=yolov3_tiny.weights"
wget -O models/yolo3/n.weights -nc "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files=yolov3.weights"
