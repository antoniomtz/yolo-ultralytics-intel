# yolo-ultralytics-intel

Script that showcases Ultralytics package using OpenVINO on CPU,GPU and NPU

## Pre-requisites

- Install drivers for iGPU and NPU depending on your system
- USB webcam

## Instructions

### Step 1:

```
pip install -r requirements.txt
```

### Step 2:


```
python main.py --model yolo11n.pt --cam-id 0 --device intel:gpu
```

Change device value to `intel:cpu` or `intel:npu`

## Docker

### Build image

```
docker build -t yolo-cv-app .
```

### Run the image on intel:npu

```
docker run -it --rm \
  --name yolo_detector \
  --device=/dev/dri:/dev/dri \
  --device=/dev/accel:/dev/accel \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd):/app \
  yolo-cv-app \
  python main.py \
    --model yolo11n.pt \
    --cam-id 0 \
    --device intel:npu
```



