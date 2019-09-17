from nsfw_detector import NSFWDetector
from utils import sort


class Detector:
    nsfw_prob_min_treshold = 0.05

    def __init__(self, model_path="./model/nsfw.299x299.h5"):
        self.detector = NSFWDetector(model_path)
        self.percentage_sum = {}
        self.total_data = 0

    def push_percentage(self, predictions):
        for label, value in predictions:
            if label not in self.percentage_sum:
                self.percentage_sum[label] = 0
            self.percentage_sum[label] += value
        self.total_data += 1

    def maybe(self, predictions):
        maybe = {}
        for label, value in predictions[1:]:
            if value >= Detector.nsfw_prob_min_treshold:
                maybe[label] = value
        return maybe

    def predict(self, image):
        predictions = self.detector.predict([image]).items()
        self.push_percentage(predictions)
        return sort(predictions)
