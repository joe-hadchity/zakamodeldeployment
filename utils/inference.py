# utils/inference.py
from typing import List, Dict, Tuple
import numpy as np
from PIL import Image
from ultralytics import YOLO

def load_model(path: str):
    model = YOLO(path)
    return model

def detect(model, pil_img: Image.Image) -> Tuple[Image.Image, List[Dict]]:
    results = model(np.array(pil_img), verbose=False)  
    res = results[0]

    bgr = res.plot()
    rgb = bgr[:, :, ::-1]
    annotated = Image.fromarray(rgb)

    boxes = []
    if res.boxes is not None:
        xyxy = res.boxes.xyxy.cpu().numpy()       
        cls = res.boxes.cls.cpu().numpy().astype(int)  
        conf = res.boxes.conf.cpu().numpy()
        for i in range(len(xyxy)):
            x1, y1, x2, y2 = xyxy[i].tolist()
            boxes.append({
                "x1": float(x1), "y1": float(y1),
                "x2": float(x2), "y2": float(y2),
                "cls": int(cls[i]),
                "score": float(conf[i])
            })
    return annotated, boxes
