import cv2
import torch
import serial
import time

# ---------------------------
# Configuración del Serial 📡
# ---------------------------
ser = serial.Serial('COM3', 115200, timeout=1)

# -------------------------------
# Cargar el modelo YOLOv5s 🔥
# -------------------------------
# Se utiliza torch.hub para cargar el modelo pre-entrenado de Ultralytics.
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.5  # Umbral de confianza (Ajustable)

# Usamos GPU si está disponible para acelerar la inferencia
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model.to(device)

# --------------------------------
# Inicializar la captura de video 🎥
# --------------------------------
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Ancho reducido
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Alto reducido

# Para medir el FPS
prev_frame_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar la detección con YOLO
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # Formato: [x1, y1, x2, y2, conf, class]

    person_found = False
    # Procesar detecciones: se busca la primera persona detectada (clase 0 en COCO)
    for det in detections:
        if int(det[5]) == 0:
            x1, y1, x2, y2, conf, cls = det
            # Calcular el centro del bounding box
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            person_found = True

            # Enviar las coordenadas al Arduino en formato "x,y\n"
            data = f"{center_x},{center_y}\n"
            ser.write(data.encode())

            # Dibujar para depuración: rectángulo y centro
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            break  # Se procesa solo la primera detección para optimizar el tiempo

    # Si no se detecta ninguna persona, enviar "NOD"
    if not person_found:
        ser.write("NOD\n".encode())

    # Calcular y mostrar FPS
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
    prev_frame_time = new_frame_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Mostrar el frame con las detecciones
    cv2.imshow("Deteccion YOLO", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
