import time
import board
import analogio
from adafruit_servokit import ServoKit
import adafruit_character_lcd.character_lcd as characterlcd

# Define as configurações do display LCD
lcd_columns = 16
lcd_rows = 2
lcd_rs = board.D12
lcd_en = board.D11
lcd_d4 = board.D5
lcd_d5 = board.D6
lcd_d6 = board.D7
lcd_d7 = board.D4
lcd_backlight = board.D10

# Inicializa o objeto do display LCD
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Define as configurações do sensor de temperatura
temperature_sensor = analogio.AnalogIn(board.A0)

# Define as configurações do sensor de luminosidade
brightness_sensor = analogio.AnalogIn(board.A1)

# Define as configurações do servo motor
servo_kit = ServoKit(channels=16)
servo = servo_kit.servo[0]
servo.angle = 0
servo_angle_increment = 15
servo_move_interval = 60

# Define o caractere customizado para o símbolo de grau Celsius
degree_char = bytearray([0b00110, 0b01001, 0b01001, 0b00110, 0b00000, 0b00000, 0b00000, 0b00000])
lcd.create_char(0, degree_char)

# Loop principal
while True:
    # Lê a tensão do sensor de temperatura e converte para graus Celsius e Fahrenheit
    temperature_voltage = temperature_sensor.value * 3.3 / 65536
    temperature_c = (temperature_voltage - 0.5) * 100
    temperature_f = temperature_c * 9 / 5 + 32
    
    # Imprime a temperatura no display LCD
    lcd.clear()
    lcd.cursor_position(0, 0)
    lcd.message = f"Temp: {temperature_c:.1f} \x00C"
    
    # Lê a tensão do sensor de luminosidade
    current_brightness = brightness_sensor.value
    
    # Move o servo a cada servo_move_interval segundos
    if time.monotonic() % servo_move_interval == 0:
        servo_angle = (servo_angle + servo_angle_increment) % 180
        servo.angle = servo_angle
    
    # Imprime a luminosidade no display LCD
    lcd.cursor_position(0, 1)
    lcd.message = f"Light: {current_brightness}"
    
    time.sleep(0.1)  # Aguarda 100ms antes de atualizar novamente
