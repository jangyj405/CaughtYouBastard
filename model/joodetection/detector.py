from pathlib import Path
import os

from otx.api.usecases.exportable_code.demo.demo_package import (
    ModelContainer,
    SyncExecutor
)
from otx.api.usecases.exportable_code.demo.demo_package.model_container import ModelContainer
from otx.api.usecases.exportable_code.visualizers import Visualizer
import cv2

class Detector(SyncExecutor):
    def __init__(self, model: ModelContainer, visualizer: Visualizer) -> None:
        super().__init__(model, visualizer)

    def infer(self,frame, ):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predictions, frame_meta = self.model(frame)
        annotation_scene = self.converter.convert_to_annotation(predictions, frame_meta)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cropped = []
        if len(annotation_scene.get_labels()) > 0:
            for entity in annotation_scene.shapes:
                x1, y1 = int(entity.x1 * frame.shape[1]), int(entity.y1 * frame.shape[0])
                x2, y2 = int(entity.x2 * frame.shape[1]), int(entity.y2 * frame.shape[0])
                cropped.append(frame[y1:y2, x1:x2])
        return cropped

def get_detector():
    model = ModelContainer(Path(os.path.join(os.path.dirname(__file__), 'model/')), device='CPU')
    detector = Detector(model,None)
    return detector

if __name__ == "__main__":
    
    detector = get_detector()
    img = cv2.imread('/home/intel/workspace/carplate/images/0000_0001.png')
    cropped = detector.infer(img)
    for crop in cropped:
        cv2.imshow("asdf",crop)
        cv2.waitKey(0)


        