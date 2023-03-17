#!/usr/bin/env python3
import socket

import depthai as dai

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and output
camRgb = pipeline.create(dai.node.ColorCamera)
videoEnc = pipeline.create(dai.node.VideoEncoder)
xout = pipeline.create(dai.node.XLinkOut)

xout.setStreamName('h265')

# Properties
camRgb.setImageOrientation(dai.CameraImageOrientation.ROTATE_180_DEG)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
videoEnc.setDefaultProfilePreset(
    30, dai.VideoEncoderProperties.Profile.H265_MAIN)

# Linking
camRgb.video.link(videoEnc.input)
videoEnc.bitstream.link(xout.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    assert isinstance(device, dai.Device)  # gimme typing

    # Output queue will be used to get the encoded data from the output defined above
    q = device.getOutputQueue(name="h265", maxSize=30, blocking=True)

    # The .h265 file is a raw stream file (not playable yet)
    while True:
        try:
            h265Packet = q.get()  # Blocking call, will wait until a new data has arrived
            assert isinstance(h265Packet, dai.Buffer)
            print(f"Sending {h265Packet.getData().size}")
            sock.sendto(h265Packet.getData().data, (UDP_IP, UDP_PORT))
        except KeyboardInterrupt:
            # Keyboard interrupt (Ctrl + C) detected
            break

    print("To view the encoded data, convert the stream file (.h265) into a video file (.mp4) using a command below:")
    print("ffmpeg -framerate 30 -i video.h265 -c copy video.mp4")
