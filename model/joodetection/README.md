# License Plate Detection using IR model

## Prerequisite
```
Ubuntu 22.04 LTS
OpenVINO 2023.0.1
Python3.10.12
```

## Installation
```bash
cd $(git rev-parse --show-toplevel)/model/joodetection
tar -zxvf model.tar.gz
python3 -m venv venv
source venv/bin/activate
pip3 install -U pip
pip3 install -r requirements.txt
```


## Usage
```Python
from model.joodetection.detector import get_detector
import cv2
import sys
sys.path.insert(1, 'model/joodetection/')
detector = get_detector()
img = cv2.imread('Some/Image/Path/IMAGE_NAME.png')
cropped = detector.infer(img)
for crop in cropped:
    cv2.imshow("crop",crop)
    cv2.waitKey(0)
```
