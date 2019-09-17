import math
import os
import sys
import cv2
import utils


class Video:
    def __init__(self, video_path, starttime=0):
        if utils.exists(video_path):
            self.video = cv2.VideoCapture(video_path)
        else:
            raise NotADirectoryError()

        self.video_path = video_path
        self.frames_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.duration = self.frames_count / self.fps
        self.frame_width, self.frame_height = (
            int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        self.starttime = starttime
        self.endtime = self.duration

        self.current_frame_num = 0
        self.current_seconds = self.starttime

    def get_next_frame(self, capture_per=2):
        if self.video.isOpened():
            success, frame = self.video.read()
            if success:
                self.current_frame_num += 1
                self.current_seconds += 1 / self.fps
                return frame
            return None

        return None

    def write_image(self, pathname, image):
        cv2.imwrite(pathname, image)


class VideoWriter:
    def __init__(self, output, video):
        self.fourcc = cv2.VideoWriter_fourcc(*"DIVX")
        self.size = (video.frame_width, video.frame_height)
        self.writer = cv2.VideoWriter(
            output, self.fourcc, video.fps, self.size)

    def write(self, image):
        self.writer.write(image)
