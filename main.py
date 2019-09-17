from detector import Detector
from video import Video, VideoWriter
from image import blur
from estimator import Estimator
from utils import clear_console, sort

import time
import argparse
import os
from pprint import pprint


class Finder:
    frame_filename = "frame.png"
    nsfw_categories = ('porn', 'hentai', 'sexy')

    def __init__(self, video_path, options):
        self.options = options

        self.detector = Detector()
        self.video = Video(video_path)
        self.video_writer = VideoWriter(self.options["outputfile"], self.video)
        self.summary = {}
        self.current_frame_category = ""

    def get_predictions(self, image):
        return self.detector.predict(image)

    def get_classification(self, predictions):
        return predictions[0][0]

    def get_maybe(self, predictions):
        return self.detector.maybe(predictions)

    def is_nsfw(self, predictions):
        classification = self.get_classification(predictions)
        self.current_frame_category = classification
        return classification in Finder.nsfw_categories

    def get_modus(self):
        return sort(self.detector.percentage_sum.items())[0]

    def maybe_nsfw(self, predictions):
        maybe = sort(self.get_maybe(predictions).items())
        if len(maybe) > 0:
            if maybe[0][0] in Finder.nsfw_categories:
                self.current_frame_category = maybe[0][0]
                return True
            else:
                modus = self.get_modus()
                if modus[0] in dict(maybe):
                    self.current_frame_category = modus[0]
                    return True

        return False

    def push_to_summary(self, key, value):
        if key not in self.summary:
            self.summary[key] = set()
        self.summary[key].update([round(value)])

    def find(self):
        estimator = Estimator()
        frame = self.video.get_next_frame()
        while frame is not None:
            start = time.time()

            # processing goes here
            predictions = self.get_predictions(frame)
            if not self.is_nsfw(predictions) and not self.maybe_nsfw(predictions):
                self.push_to_summary(
                    self.current_frame_category, self.video.current_seconds)
                self.video_writer.write(frame)
            else:
                self.push_to_summary(
                    self.current_frame_category, self.video.current_seconds)

                opt_blur = self.options["blur"]
                if opt_blur is not None:
                    x, y = opt_blur.split(",")
                    self.video_writer.write(blur(frame, (int(x), int(y))))

            end = time.time()
            estimator.log_progress(
                start, end, self.video.current_frame_num, self.video.frames_count)

            frame = self.video.get_next_frame()

    def output_summary(self):
        with open(self.options["outputsummary"], "w") as f:
            pprint(self.summary, stream=f)


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--inputfile", required=True,
                           help="Input video to be processed")
    argparser.add_argument("-o", "--outputfile",
                           required=True, help="Prcessed video output path")
    argparser.add_argument("-os", "--outputsummary",
                           help="Summary output txt file")
    argparser.add_argument(
        "-b", "--blur", help="Instead cutting the frame, blur it")
    options = vars(argparser.parse_args())
    return options


def main():
    options = parse_args()

    finder = Finder(options["inputfile"], options)
    try:
        clear_console()
        finder.find()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        os.system("stty sane")
        if (finder.options["outputsummary"]):
            finder.output_summary()


if __name__ == "__main__":
    main()
