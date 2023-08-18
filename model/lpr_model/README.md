# License Plate Recognition Model

## Prerequisite
```
WSL2 Ubuntu 18.04 LTS Distribution
Python3.6
TensorFlow 1.13.1
OpenVINO 2022.1.0
```

## Installation
```
cd $(git rev-parse --show-toplevel)/model/lpr_model
virtualenv venv -p python3.6 --prompt="(lpr)"
echo ". /opt/intel/openvino/setupvars.sh" >> venv/bin/activate
. venv/bin/activate

CPU_ONLY=true pip3 install -e .
pip3 install -e utils
pip3 install openvino-dev==2022.1.0
```

## Train an LPR Model

### Prepare a Dataset
```
cd data/
tar -zxvf team4_lpr.tar.gz
cd -
python3 data/make_train_val_split.py data/team4_lpr/annotation
# check the result
# data/team4_lpr
# ├── annotation
# ├── crops
# ├── test_infer
# ├── train
# └── val
```

### Train
```
python tools/train.py config_team4.py
```

### Export
```
 python3 tools/export.py --data_type FP32 \
 --output_dir model/export config_team4.py
```

### Test the exported IR model
```
python3 tools/infer_ie.py --model model/export/IR/FP32/lpr.xml --device=CPU \
--cpu_extension="${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/lib/intel64/libcpu_extension_avx2.so" \
--config config_team4.py <IMAGE_FILE_PATH>
```

