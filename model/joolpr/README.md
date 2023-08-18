# LPR using IR model

## Prerequisite
```
Ubuntu 22.04 LTS
OpenVINO 2023.0.1
Python3.10.12
```

## Installation
```bash
cd $(git rev-parse --show-toplevel)/model/joolpr
tar -zxvf ir_lpr_model.tar.gz
python3 -m venv venv
echo ". /opt/intel/openvino/setupvars.sh" >> venv/bin/activate
source venv/bin/activate
pip3 install -U pip
pip3 install -r requirements.txt
```


## Usage
```Python
from model.joolpr.infer import LPRModel
lpr_model = LPRModel()
number, output_img = lpr_model.infer(image)
# before program exit call 'LPRModel.free()'
lpr_model.free()
```