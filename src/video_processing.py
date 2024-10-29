# video_processing.py
import cv2
import numpy as np
import time
from ultralytics import YOLO
from config import VIDEO_URL, COLLISION_THRESHOLD, FRAME_RATE, DETECTION_RATE, FILTERED_OBJECTS, OBJECT_PAIRS

model = YOLO("../yolov8n.pt")

class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_URL)
        self.frame_rate = 1.0 / FRAME_RATE
        self.detection_rate = 1.0 / DETECTION_RATE
        self.last_video_time = time.time()
        self.last_detection_time = time.time()
        self.persistent_detections = {}
        self.collision_flag = False
        self.last_results = []  # Cache de detecciones

    def get_frame(self):
        current_time = time.time()
        if (current_time - self.last_video_time) >= self.frame_rate:
            ret, frame = self.cap.read()
            if not ret:
                return None, "Failed to retrieve video"
            self.last_video_time = current_time
            return frame, None
        return None, None

    def detect_objects(self, frame):
        current_time = time.time()
        # Solo detecta si ha pasado suficiente tiempo desde la última detección
        if (current_time - self.last_detection_time) >= self.detection_rate:
            results = model(frame)
            self.last_detection_time = current_time
            self.last_results = results[0].boxes  # Actualiza cache de detección
            return self.last_results
        return self.last_results

    def filter_and_persist_detections(self, detections):
        current_detections = {}
        detections_to_check = []

        for detection in detections:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            conf = detection.conf[0]
            cls = int(detection.cls[0])
            label = model.names[cls]

            if not FILTERED_OBJECTS or label in FILTERED_OBJECTS:
                current_detections[label] = (x1, y1, x2, y2, conf)
                detections_to_check.append((label, (x1, y1, x2, y2)))

        # Actualiza solo detecciones presentes actualmente
        self.persistent_detections.update(current_detections)
        for label in list(self.persistent_detections):
            if label not in current_detections:
                del self.persistent_detections[label]

        return detections_to_check

    def check_collisions(self, detections_to_check):
        distances = []
        collision_detected = False

        for i, (label1, box1) in enumerate(detections_to_check):
            for j in range(i + 1, len(detections_to_check)):
                label2, box2 = detections_to_check[j]
                if (label1, label2) in OBJECT_PAIRS or (label2, label1) in OBJECT_PAIRS:
                    x1_a, y1_a, x2_a, y2_a = box1
                    x1_b, y1_b, x2_b, y2_b = box2
                    center_a = ((x1_a + x2_a) // 2, (y1_a + y2_a) // 2)
                    center_b = ((x1_b + x2_b) // 2, (y1_b + y2_b) // 2)
                    distance = np.sqrt((center_a[0] - center_b[0]) ** 2 + (center_a[1] - center_b[1]) ** 2)
                    distances.append(f"Distance between {label1} and {label2}: {distance:.2f}")

                    if distance < COLLISION_THRESHOLD:
                        collision_detected = True

        return collision_detected, distances
