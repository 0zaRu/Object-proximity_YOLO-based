import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

VIDEO_URL = os.getenv("VIDEO_URL", "http://172.23.96.6:4748/video")
COLLISION_THRESHOLD = int(os.getenv("COLLISION_THRESHOLD", 200))
FRAME_RATE = int(os.getenv("FRAME_RATE", 15))
DETECTION_RATE = int(os.getenv("DETECTION_RATE", 2))
FILTERED_OBJECTS = ["bottle", "cat", "mouse", "keyboard", "guitar", "person", "tv"]
OBJECT_PAIRS = [
    ("bottle", "keyboard"), ("mouse", "keyboard"),
    ("tv", "cat"), ("person", "tv"),
    ("cat", "guitar"), ("person", "guitar")
]
