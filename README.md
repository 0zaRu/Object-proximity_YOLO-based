# Live Object Detection with Collision Alerts

This project implements real-time object detection and collision alerts using Streamlit, OpenCV, and YOLOv8. Designed for efficient processing, it streams video from a webcam or IP camera, detects specific objects, and raises alerts when specified object pairs come within a user-defined collision threshold.


## Features

* **Efficient Object Detection** : Uses YOLOv8 for fast, accurate recognition.
* **Customizable Object Filtering** : Filters detections based on a user-defined list.
* **Collision Detection** : Defines pairs of objects for collision alerts and calculates the distance between them.
* **Real-Time Stream and Alert Display** : Uses Streamlit to display video and alert notifications in real-time.
* **User Controls** : Adjustable collision threshold through a sidebar slider.

## How It Works

1. **Object Detection** : Processes video at a set frame rate, detects objects, and displays them on the video stream.
2. **Persistent Detections** : Maintains object detections across frames to ensure smoother tracking.
3. **Collision Calculation** : Checks distances between defined pairs of objects and displays alerts if they are too close.
4. **Dynamic Interface** : Displays live video feed, collision alerts, and object distance information.

## Requirements

 **Important** : This application requires a webcam or an IP camera that streams video. Ensure that the camera is set up to provide a video stream via a specific IP address.


## Environment Variables

The following environment variables are used to configure the application:

* `VIDEO_URL`: URL of the video web cam stream
* `COLLISION_THRESHOLD`: The distance threshold for triggering collision alerts (default: `200`). In px.
* `FRAME_RATE`: The rate at which video frames are processed (default: `15`)
* `DETECTION_RATE`: The rate at which object detections are processed (default: `2`)


## Running the Project

To run the application using Docker Compose, follow these steps:

* **Clone the Repository** :

```
git clone <repository-url>
cd <repository-directory>
```

* **Build and Start the Docker Container** :

```
docker-compose up --build
```

* **Access the Application :** 

Open your web browser and navigate to `http://localhost:8501` to access the live object detection interface.

Make sure you have Docker and Docker Compose installed on your machine before running the commands above. The application will start streaming video and providing collision alerts as configured.
