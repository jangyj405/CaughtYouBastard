# License Plate Detection Model Traning
#### Transfer Learning with MobileNetV2-ATSS

## Prerequisite
```
Ubuntu 22.04 LTS
Python3.10.12
```

## Installation

### install packages
```
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### prepare the dataset
Download [Here](https://drive.google.com/file/d/1fpiujqxl5WOPYLY-e7LyymxUqilbyq8j/view?usp=sharing)

```bash
cp ~/Downloads/carplate.tar.gz \
$(git rev-parse --show-toplevel)/model/plate_detection/
cd $(git rev-parse --show-toplevel)/model/plate_detection
tar -zxvf carplate.tar.gz
```

### create workspace
```bash
otx build --workspace carplate-workspace \
--train-data-root carplate/ \
--val-data-root carplate/ \
--train-ann-files carplate/annotations/instances_train.json \
--val-ann-files carplate/annotations/instances_val.json \
Custom_Object_Detection_Gen3_ATSS
```


## Training
### train the model
```bash
cd carplate-workspace
cp ../template.yaml template.yaml
otx train
```

### evaluation
```bash
otx eval SSD --test-data-roots ../carplate/ \
--load-weights <WEIGHTS_PATH>/weights.pth
```

### export
```bash
otx export Custom_Object_Detection_Gen3_SSD \
--load-weights <WEIGHTS_PATH>/weights.pth \
--output <OUTPUT_PATH> --dump-features
```

### deploy
```bash
otx deploy SSD --load-weights <OUTPUT_XML_PATH>/openvino.xml \
--output <PATH_TO_OUTPUT>
```