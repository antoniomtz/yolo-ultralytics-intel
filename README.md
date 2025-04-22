# yolo-ultralytics-intel

Script that showcases Ultralytics package using OpenVINO on CPU,GPU and NPU

## Instructions

### Step 0:

```
python3 -m venv venv
source venv/bin/activate
```

### Step 1:

```
pip install -r requirements.txt
```

### Step 2:


```
python main.py --model yolo11n.pt --cam-id 0 --device intel:gpu
```

Change device value to `intel:cpu` or `intel:npu`


