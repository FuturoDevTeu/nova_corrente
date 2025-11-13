from ultralytics import YOLO

model = YOLO("yolov8s.pt")

model.train(data="dataset/data.yaml", epochs=30, batch=6)

metrics = model.val()

if __name__ == "__main__":
    main()