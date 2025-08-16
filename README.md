## Object Detection Flask App 

This project is an **Object Detection Web App** built with **Flask** and **YOLOv8**.  
It allows users to upload images through a web interface, and the app will detect and highlight objects within those images.

## What the Model Does

- Uses a **YOLOv8 model** (`last.pt` or `best.pt`) for object detection.  
- Detects and classifies objects in uploaded images.  
- Outputs the same image with bounding boxes and labels drawn on detected objects.

```bash
git clone https://github.com/joe-hadchity/zakamodeldeployment.git
```

## build the docker image

```bash
docker build -t object-detection-flask .
```
## Run the Container

```bash
docker run -p 8080:8080 object-detection-flask
```

## Access the App

```bash
http://localhost:8080
```

## How to Use the Interface

Open the web app in your browser.

Upload an image using the Upload button.

The model will run inference and display the image with detected objects highlighted.
