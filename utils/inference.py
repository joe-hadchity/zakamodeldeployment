# utils/inference.py
from typing import List, Dict, Tuple
import numpy as np
from PIL import Image
from ultralytics import YOLO

def load_model(path: str):
    """
    Works for yolo11n.pt, yolov8n.pt, or your custom weights.
    """
    model = YOLO(path)  # auto-loads & checks architecture
    return model

def detect(model, pil_img: Image.Image) -> Tuple[Image.Image, List[Dict]]:
    """
    Runs detection on a PIL image and returns (annotated_pil_image, boxes_json).
    """
    # Run inference
    results = model(np.array(pil_img), verbose=False)  # list of Results
    res = results[0]

    # Annotated image (res.plot() returns BGR numpy array)
    bgr = res.plot()
    rgb = bgr[:, :, ::-1]
    annotated = Image.fromarray(rgb)

    # Extract boxes
    boxes = []
    if res.boxes is not None:
        xyxy = res.boxes.xyxy.cpu().numpy()       # (N, 4)
        cls = res.boxes.cls.cpu().numpy().astype(int)  # (N,)
        conf = res.boxes.conf.cpu().numpy()       # (N,)
        for i in range(len(xyxy)):
            x1, y1, x2, y2 = xyxy[i].tolist()
            boxes.append({
                "x1": float(x1), "y1": float(y1),
                "x2": float(x2), "y2": float(y2),
                "cls": int(cls[i]),
                "score": float(conf[i])
            })
    return annotated, boxes
