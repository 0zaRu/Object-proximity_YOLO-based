# Using this instead of the rest because it is much faster and more efficient.

import streamlit as st
import cv2
from ultralytics import YOLO
import time
import numpy as np

# Lista de objetos a reconocer; si está vacía, se muestran todos
filtered_objects = ["bottle", "cat", "mouse", "keyboard", "guitar", "person", "tv"]

# Cargar el modelo YOLOv8
model = YOLO("../yolov8n.pt")

# Pares de objetos para detección de colisión
object_pairs = [("bottle", "keyboard"), ("mouse", "keyboard"), ("tv", "cat"), ("person", "tv"), ("cat", "guitar"), ("person", "guitar")]

# URL del video
rute = "http://172.23.96.6:4748"

# Interfaz de Streamlit
st.title("Live Object Detection with Collision Alert")
st.text(f"Streaming webcam video from {rute}/video")

# Configurar el umbral de colisión en la interfaz
collision_threshold = st.sidebar.slider("Collision Threshold", min_value=50, max_value=500, value=200)

# Acceso al flujo de video
cap = cv2.VideoCapture(f"{rute}/video")

# Placeholder para el video y la notificación
frame_placeholder = st.empty()
notification_placeholder = st.empty()
distance_placeholder = st.sidebar.empty()  # Placeholder para mostrar distancia

# Variables de control de tasa de fotogramas
frame_rate = 15
detection_rate = 2

# Calcular intervalos de tiempo
video_interval = 1.0 / frame_rate
detection_interval = 1.0 / detection_rate

last_video_time = time.time()
last_detection_time = time.time()

# Almacenar detecciones persistentes
persistent_detections = {}
collision_flag = False

# Bucle de procesamiento de video
while cap.isOpened():
    # Captura cuadro a cuadro
    current_time = time.time()
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to retrieve video")
        break

    # Mostrar video a la tasa de fotogramas deseada
    if (current_time - last_video_time) >= video_interval:
        # Dibujar detecciones persistentes
        for label, detection in persistent_detections.items():
            x1, y1, x2, y2, conf = detection
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        frame_placeholder.image(frame, channels="BGR")
        last_video_time = current_time

    # Realizar detección de objetos a la tasa deseada
    if (current_time - last_detection_time) >= detection_interval:
        results = model(frame)
        last_detection_time = current_time

        # Almacenamiento temporal para detecciones
        current_detections = {}
        detections_to_check = []

        for detection in results[0].boxes:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            conf = detection.conf[0]
            cls = int(detection.cls[0])
            label = model.names[cls]

            if not filtered_objects or label in filtered_objects:
                current_detections[label] = (x1, y1, x2, y2, conf)
                detections_to_check.append((label, (x1, y1, x2, y2)))

        # Actualizar detecciones persistentes
        persistent_detections.update(current_detections)

        # Remover detecciones no presentes en el cuadro actual
        for label in list(persistent_detections):
            if label not in current_detections:
                del persistent_detections[label]

        # Detección de colisión entre pares de objetos especificados
        collision_detected = False
        distances = []  # Lista para almacenar distancias para la interfaz

        for i, (label1, box1) in enumerate(detections_to_check):
            for j in range(i + 1, len(detections_to_check)):
                label2, box2 = detections_to_check[j]
                if (label1, label2) in object_pairs or (label2, label1) in object_pairs:
                    x1_a, y1_a, x2_a, y2_a = box1
                    x1_b, y1_b, x2_b, y2_b = box2
                    center_a = ((x1_a + x2_a) // 2, (y1_a + y2_a) // 2)
                    center_b = ((x1_b + x2_b) // 2, (y1_b + y2_b) // 2)
                    distance = np.sqrt((center_a[0] - center_b[0]) ** 2 + (center_a[1] - center_b[1]) ** 2)
                    
                    distances.append(f"Distance between {label1} and {label2}: {distance:.2f}")

                    if distance < collision_threshold:
                        collision_detected = True
                        break
            if collision_detected:
                break

        # Mostrar distancias en el lateral de la interfaz
        distance_placeholder.write("\n".join(distances))

        # Mostrar alerta de colisión
        if collision_detected and not collision_flag:
            collision_flag = True
            with notification_placeholder:
                st.warning("Collision Alert! Objects are too close!", icon="⚠️")
        elif not collision_detected and collision_flag:
            collision_flag = False
            notification_placeholder.empty()

cap.release()