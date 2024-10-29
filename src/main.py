# main.py
import streamlit as st
from video_processing import VideoProcessor
from config import COLLISION_THRESHOLD
import cv2
import asyncio

# Inicializar procesador de video
processor = VideoProcessor()

# Título e información de la interfaz
st.title("Live Object Detection with Collision Alert")
st.sidebar.slider("Collision Threshold", min_value=50, max_value=500, value=COLLISION_THRESHOLD)
frame_placeholder = st.empty()
notification_placeholder = st.empty()
distance_placeholder = st.sidebar.empty()

# Procesamiento en vivo con asyncio
async def process_frames():
    while processor.cap.isOpened():
        frame, error = processor.get_frame()
        if error:
            st.write(error)
            break

        if frame is not None:
            for label, detection in processor.persistent_detections.items():
                x1, y1, x2, y2, conf = detection
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            frame_placeholder.image(frame, channels="BGR")

            detections = processor.detect_objects(frame)
            detections_to_check = processor.filter_and_persist_detections(detections)

            collision_detected, distances = processor.check_collisions(detections_to_check)
            distance_placeholder.write("\n".join(distances))

            if collision_detected and not processor.collision_flag:
                processor.collision_flag = True
                with notification_placeholder:
                    st.warning("Collision Alert! Objects are too close!", icon="⚠️")
            elif not collision_detected and processor.collision_flag:
                processor.collision_flag = False
                notification_placeholder.empty()

        await asyncio.sleep(processor.frame_rate)  # Tiempo para cargar el siguiente cuadro

# Inicia la función asincrónica
asyncio.run(process_frames())

processor.cap.release()
