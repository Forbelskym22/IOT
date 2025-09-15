import max7219
from machine import ADC, Pin, SPI
from time import sleep

# --- Nastavení počtu modulů ---
NUM = 1
WIDTH = NUM * 8
HEIGHT = 8

# --- SPI0 konfigurace ---
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))
cs  = Pin(17, Pin.OUT)

# --- Inicializace MAX7219 ---
display = max7219.Matrix8x8(spi, cs, NUM)
display.brightness(5)
display.fill(0)
display.show()

# --- Inicializace joysticku ---
x_axis = ADC(26)
y_axis = ADC(27)
button = Pin(22, Pin.IN, Pin.PULL_UP)

# --- Počáteční pozice tečky ---
x_pos = WIDTH // 2
y_pos = HEIGHT // 2

# --- Tolerance (deadzone) ---
DEADZONE = 0.1       # 10% středová zóna
CENTER = 32768
MIN_VAL = int(CENTER * (1 - DEADZONE))
MAX_VAL = int(CENTER * (1 + DEADZONE))

# --- Velikost kroku ---
STEP = 1
STEPX = 1
STEPY = 1
stepdelay = 0.1

while True:
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()
    btn = not button.value()
    
    #--- Omezení pro jednu osu ---
    
    # --- Po určení STEPX a STEPY ---

 
    
    #--- Pohyb ---#
    
    x_pos += STEPX
    y_pos += STEPY
    
    
    # --- Relativní pohyb podle joysticku ---
    if x_raw < MIN_VAL:
        STEPX = STEP
        STEPY =0
    elif x_raw > MAX_VAL:
        STEPX = -STEP
        STEPY =0
    if y_raw < MIN_VAL:
        STEPY = STEP
        STEPX =0
    elif y_raw > MAX_VAL:
        STEPY = -STEP
        STEPX =0
    
    
    
    # --- Omezení, aby tečka zůstala na displeji ---
    x_pos = max(0, min(WIDTH-1, x_pos))
    y_pos = max(0, min(HEIGHT-1, y_pos))

    # --- Vykreslení ---
    display.fill(0)
    display.pixel(x_pos, y_pos, 1)
    display.show()

    sleep(stepdelay)
