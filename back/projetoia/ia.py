from ultralytics import YOLO
import cv2
import os

async def analisar(image_path: str):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "runs", "detect", "train", "weights", "best.pt")
    model = YOLO(MODEL_PATH)

    EPIS_OBRIGATORIOS = ['Boots', 'Gloves', 'Hard Hat', 'Reflective Vest', 'Safety Glasses']

    img = cv2.imread(image_path)
    PADRAO = 700
    img_resized = cv2.resize(img, (PADRAO, PADRAO))

    results = model(img_resized, imgsz=PADRAO)
    r = results[0]

    epis_detectados = set()
    for box, conf, cls in zip(r.boxes.xyxy, r.boxes.conf, r.boxes.cls):
        nome_classe = r.names[int(cls.item())]
        epis_detectados.add(nome_classe)
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_resized, f"{nome_classe} ({conf:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    epis_faltando = [epi for epi in EPIS_OBRIGATORIOS if epi not in epis_detectados]
    status_text = "EM CONFORMIDADE" if not epis_faltando else "FORA DE CONFORMIDADE"
    status_color = (0, 255, 0) if not epis_faltando else (0, 0, 255)
    cv2.putText(img_resized, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, status_color, 3)

    if epis_faltando:
        faltando_text = "FALTANDO: " + ", ".join(epis_faltando)
        cv2.putText(img_resized, faltando_text, (20, PADRAO - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    resultado_path = image_path.replace(".jpg", "_resultado.jpg")
    cv2.imwrite(resultado_path, img_resized)

    return epis_faltando, status_text, resultado_path
