#include <Servo.h>

Servo turret;               // Objeto para controlar el servo
const int servoPin = 9;     // Pin digital al que está conectado el servo
const int camWidth = 640;   // Ancho de la imagen en píxeles (ajusta este valor según tu configuración)
const int servoMin = 0;     // Ángulo mínimo del servo
const int servoMax = 180;   // Ángulo máximo del servo

void setup() {
  Serial.begin(115200);     // Inicia la comunicación serial a 115200 baudios
  turret.attach(servoPin);  // Asocia el objeto servo al pin definido
  turret.write(90);         // Posición inicial (opcional)
  Serial.println("Arduino listo para recibir datos...");
}

void loop() {
  // Verifica si hay datos disponibles en el puerto serial
  if (Serial.available()) {
    // Lee la cadena hasta encontrar un salto de línea
    String data = Serial.readStringUntil('\n');
    Serial.print("Datos recibidos: ");
    Serial.println(data);
    
    // Si se recibe "NOD", significa que no hay detección y no se modifica la posición
    if (data.startsWith("NOD")) {
      return;
    }
    
    // Busca la coma que separa las coordenadas (se espera el formato "x,y")
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      // Extraer la coordenada horizontal "x"
      int posX = data.substring(0, commaIndex).toInt();
      
      // Mapear la posición x (de la imagen) al rango del servo
      int angle = map(posX, 0, camWidth, servoMin, servoMax);
      turret.write(angle);
      
      Serial.print("Servo movido a: ");
      Serial.println(angle);
    }
  }
}
