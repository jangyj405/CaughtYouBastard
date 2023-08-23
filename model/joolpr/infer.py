from __future__ import print_function
from argparse import ArgumentParser
import logging as log
import sys
import os
import cv2
from openvino.inference_engine import IECore


class LPRModel():
  def __init__(self) -> None:
    self.r_vocab = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', \
          10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I',\
          19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R',\
          28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: '_', -1: ''}
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    self.exec_net, self.plugin, self.input_blob, self.out_blob, self.shape = self.load_ir_model(os.path.join(os.path.dirname(__file__) ,'ir_lpr_model/lpr.xml'), \
                                                                                                'CPU', None, '/opt/intel/openvino_2023.0.1/deployment_tools\
                                                                                                /inference_engine/lib/intel64/libcpu_extension_avx2.so')
    self.n_batch, self.channels, self.height, self.width = self.shape
    pass

  def decode_ie_output(self, vals, r_vocab):
    vals = vals.flatten()
    decoded_number = ''
    for val in vals:
      if val < 0:
        break
      decoded_number += r_vocab[val]
    return decoded_number
  
  def display_license_plate(self, number, license_plate_img):
    size = cv2.getTextSize(number, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    text_width = size[0][0]
    text_height = size[0][1]

    height, width, _ = license_plate_img.shape
    license_plate_img = cv2.copyMakeBorder(license_plate_img, 0, text_height + 10, 0,
                                           0 if text_width < width else text_width - width,
                                           cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cv2.putText(license_plate_img, number, (0, height + text_height + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

    return license_plate_img

  def load_ir_model(self, model_xml, device, plugin_dir, cpu_extension):
    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    # initialize plugin
    log.info("Initializing plugin for %s device...", device)
    ie = IECore()

    # read IR
    log.info("Reading IR...")
    net = ie.read_network(model=model_xml, weights=model_bin)

    # input / output check
    assert len(net.input_info.keys()) == 1, "LPRNet must have only single input"
    assert len(net.outputs) == 1, "LPRNet must have only single output topologies"

    input_blob = next(iter(net.input_info))
    out_blob = next(iter(net.outputs))
    log.info("Loading IR to the plugin...")
    exec_net = ie.load_network(network=net)
    shape = net.input_info[input_blob].input_data.shape# pylint: disable=E1136
    del net

    return exec_net,None, input_blob, out_blob, shape

  def infer(self, image):
    img_to_display = image.copy()
    in_frame = cv2.resize(image, (self.width, self.height))
    in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
    in_frame = in_frame.reshape((self.n_batch, self.channels, self.height, self.width))

    result = self.exec_net.infer(inputs={self.input_blob: in_frame})
    lp_code = result[self.out_blob][0]
    lp_number = self.decode_ie_output(lp_code, self.r_vocab)
    img_to_display = self.display_license_plate(lp_number, img_to_display)
    return lp_number, img_to_display

    

  def free(self,):
    del self.exec_net
    del self.plugin
    

def main():
  lpr = LPRModel()
  test_img = cv2.imread(os.path.join(os.path.dirname(__file__),'test.jpg'))
  output, img = lpr.infer(test_img)
  print('output : ', output)
  cv2.imshow('output img', img)
  cv2.waitKey(0)
  lpr.free()

if __name__ == '__main__':
  sys.exit(main() or 0)