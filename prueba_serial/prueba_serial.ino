#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// LCD I2C (usa la dirección que encontraste)
LiquidCrystal_I2C lcd(0x20, 16, 2);

// Pines
const int botones[] = {3, 4, 5, 6, 7};
const int leds[] = {8, 9, 10, 11, 12};
const int NUM_BOTONES = 5;

// Temporizador
const int tiempo_funcionamiento = 270; // segundos
unsigned long tiempoInicio = 0;

// Estados del sistema
enum EstadoSistema { APAGADO, HABILITADO, CONTANDO };
EstadoSistema estado = APAGADO;

// Control de botones
bool anteriorBoton[NUM_BOTONES] = {false};

// Variables de tiempo
int ultimoSegundo = -1;
int tiempoRestante = tiempo_funcionamiento;

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Sistema listo");

  for (int i = 0; i < NUM_BOTONES; i++) {
    pinMode(botones[i], INPUT);
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }

  habilitar();
}

void loop() {
  unsigned long ahora = millis();

  // Leer botones
  for (int i = 0; i < NUM_BOTONES; i++) {
    bool estadoActual = digitalRead(botones[i]);

    if (estadoActual && !anteriorBoton[i]) {

      switch (estado) {

        case HABILITADO:
          // Iniciar conteo
          tiempoInicio = ahora;
          estado = CONTANDO;
          Serial.println("⏱️ Temporizador iniciado");

          for (int j = 0; j < NUM_BOTONES; j++) {
            digitalWrite(leds[j], (i == j) ? HIGH : LOW);
          }
          break;

        case CONTANDO:
          // Solo cambia el LED activo
          for (int j = 0; j < NUM_BOTONES; j++) {
            digitalWrite(leds[j], (i == j) ? HIGH : LOW);
          }
          break;
      }
    }

    anteriorBoton[i] = estadoActual;
  }

  // Lógica del temporizador
  if (estado == CONTANDO) {
    tiempoRestante = tiempo_funcionamiento - ((ahora - tiempoInicio) / 1000);
    if (tiempoRestante < 0) tiempoRestante = 0;

    if (tiempoRestante != ultimoSegundo) {
      ultimoSegundo = tiempoRestante;
      mostrarTiempo(tiempoRestante);
    }

    if (tiempoRestante <= 0) {
      detenerContador();
    }
  } 
  else if (estado == HABILITADO) {
    mostrarTiempo(tiempo_funcionamiento);
  }
}

// ======================================================
// FUNCIONES
// ======================================================

void habilitar() {
  estado = HABILITADO;
  tiempoRestante = tiempo_funcionamiento;
  mostrarTiempo(tiempo_funcionamiento);
  Serial.println("✅ Sistema habilitado (esperando boton)");
}

void mostrarTiempo(int segundosTotales) {
  int minutos = segundosTotales / 60;
  int segundos = segundosTotales % 60;

  lcd.setCursor(0, 0);
  lcd.print("Tiempo: ");

  // Limpia solo donde va el tiempo
  lcd.setCursor(8, 0);
  lcd.print("     ");
  lcd.setCursor(8, 0);

  if (minutos < 10) lcd.print("0");
  lcd.print(minutos);
  lcd.print(":");
  if (segundos < 10) lcd.print("0");
  lcd.print(segundos);

  lcd.setCursor(0, 1);
  if (estado == CONTANDO) {
    lcd.print("Modo: EN USO     ");
  } else {
    lcd.print("Modo: LISTO      ");
  }
}

void detenerContador() {
  Serial.println("🛑 Tiempo finalizado");
  estado = APAGADO;
  ultimoSegundo = -1;
  tiempoRestante = 0;

  for (int i = 0; i < NUM_BOTONES; i++) {
    digitalWrite(leds[i], LOW);
  }

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Tiempo agotado");
  lcd.setCursor(0,1);
  lcd.print("Reiniciando...");
  delay(2000);

  habilitar();
}

