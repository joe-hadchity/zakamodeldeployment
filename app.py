# app.py
import os, uuid
from flask import Flask, render_template, request, jsonify
from PIL import Image
from utils.inference import load_model, detect

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/outputs'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 MB uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---- choose your weights here ----
MODEL_PATH = "models/yolo11n.pt"  # or "models/yolov8n.pt" or your best.pt
# ----------------------------------
model = load_model(MODEL_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/api/detect", methods=["POST"])
def api_detect():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    try:
        img = Image.open(file.stream).convert("RGB")
    except Exception:
        return jsonify({"error": "Invalid image"}), 400

    annotated, boxes = detect(model, img)
    fname = f"{uuid.uuid4().hex}.jpg"
    out_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
    annotated.save(out_path, format="JPEG", quality=90)

    return jsonify({
        "boxes": boxes,
        "image_url": f"/static/outputs/{fname}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
