# Detección de Personas con YOLO y Control de Torreta con Arduino 🤖🎯

Este proyecto utiliza un modelo YOLO (en este caso, **YOLOv5s**) para detectar personas en tiempo real a través de una cámara y enviar las coordenadas del centro del bounding box al Arduino mediante comunicación serial. El Arduino recibe esta información y controla un servo que gira en el eje horizontal para orientar una torre hacia la persona detectada.

---

## Características 🚀

- **Detección en tiempo real:** Utiliza YOLOv5 para detectar personas de forma rápida.
- **Comunicación serial:** Envía las coordenadas en formato `x,y` a través del puerto serial (115200 baudios).
- **Control de servo:** El Arduino recibe los datos y mapea la posición horizontal de la detección para mover un servo.
- **Visualización:** Se muestra en pantalla el video de la cámara con el bounding box y el centro de la detección para facilitar la depuración.

---

## Requisitos 📋

### Software

- **Python 3.7 o superior** 🐍
- **OpenCV:** Para captura y visualización de video.
- **PyTorch** y **torchvision:** Para cargar y utilizar el modelo YOLOv5.
- **PySerial:** Para la comunicación serial entre Python y Arduino.

## Configuración del Entorno Virtual 🐍

Para mantener aisladas las dependencias del proyecto, se recomienda utilizar un entorno virtual.

### Crear y Activar el Entorno Virtual

1. **Crear el entorno virtual:**

```bash
python -m venv venv
```

---

## Instalación ⚙️

### 1. Clonar el Repositorio

```bash
git clone https://github.com/DiegoK36/Proyecto-Yolo.git
cd Proyecto-Yolo
```

### 2. Instalar las Dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el Código

```bash
python3 yolo_serial.py
```