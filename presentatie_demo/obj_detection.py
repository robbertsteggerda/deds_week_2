from ultralytics import YOLO

# import cv2

model = YOLO("yolov8s.pt")

results = model.predict(source="0", show=True)

print(results)


# pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu