import max7219
from machine import ADC, Pin, SPI
import time
from time import sleep
import urandom


# --- Nastavení počtu modulů ---
NUM = 1
WIDTH = NUM * 8
HEIGHT = 8

# --- SPI0 konfigurace ---
spi = SPI(0, baudrate=10_000_000,
          polarity=0,
          phase=0,
          sck=Pin(18),  # CLK
          mosi=Pin(19)) # DIN
cs = Pin(17, Pin.OUT)

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
CENTER   = 32768
MIN_VAL  = int(CENTER * (1 - DEADZONE))
MAX_VAL  = int(CENTER * (1 + DEADZONE))

# --- Velikost kroku ---
STEP = 1
STEPX = 1
STEPY = 1
stepdelay = 0.1

# --- zpomalení kroku ---
MOVE_INTERVAL = 800   # ms mezi posuny hada (větší = pomalejší)
last_move = time.ticks_ms()


def limit_position(x, y):
    """Vrátí souřadnice omezené na velikost displeje."""
    x = max(0, min(WIDTH - 1, x))
    y = max(0, min(HEIGHT - 1, y))
    return x, y


def draw_points(points):
    """
    points – list n-tic [(x1, y1), (x2, y2), ...]
    Vykreslí všechny body najednou.
    """
    display.fill(0)           # smažeme starý obraz
    for x, y in points:
        display.pixel(x, y, 1) # nakreslí každý bod
    display.show()

#had
def check_food_collision(snake, food):
    return snake[0] == food[0]
    
# --- Funkce pro náhodný spawn tečky ---
def spawn_food():
    x = urandom.getrandbits(3)  # 0–7 (3 bity stačí na 8 hodnot)
    y = urandom.getrandbits(3)
    points = [(x,y)]
    return points

food_spawned=False

snake = [(x_pos,y_pos)]   # tělo hada
end = False


while True:
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()
    btn   = not button.value()


    if end and btn:
        end = False
        # reset počáteční pozice hada
        x_pos = WIDTH // 2
        y_pos = HEIGHT // 2
        snake = [(x_pos, y_pos)]
        food_spawned = False  # nové jídlo se vygeneruje
        display.fill(0)
        display.show()
        continue




    # --- Určení směru podle joysticku ---
    if x_raw < MIN_VAL:
        STEPX, STEPY = STEP, 0
    elif x_raw > MAX_VAL:
        STEPX, STEPY = -STEP, 0
    elif y_raw < MIN_VAL:
        STEPX, STEPY = 0, STEP
    elif y_raw > MAX_VAL:
        STEPX, STEPY = 0, -STEP
    print(end)
    print(snake)
# --- posun hada jen když uběhl čas ---
    if time.ticks_diff(time.ticks_ms(), last_move) >= MOVE_INTERVAL and not end:
        last_move = time.ticks_ms()
        
        # --- předpověď budocnosti ---
        next_x = x_pos + STEPX
        next_y = y_pos + STEPY
        
        if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
            end = True
        # --- Posun hlavy ---
        x_pos += STEPX
        y_pos += STEPY
        x_pos, y_pos = limit_position(x_pos, y_pos)

        # --- Přidání nové hlavy do těla hada ---
        snake.insert(0, (x_pos, y_pos))  # přidá novou hlavu na začátek

        # --- kontrola kolize s jídlem ---
        if check_food_collision(snake, food):
            # necháme ocas – had poroste
            # spawn nového jídla
            MOVE_INTERVAL -=10
            food = spawn_food()
        else:
            snake.pop()
        # --- kolize hada s hadem
        for i in range(1, len(snake)):
            if snake[0] == snake[i]:
                end = True
                break
        # --- kolize se zdí ---
        
    # --- Spawn jídla ---
    if not food_spawned:
        food = spawn_food()
        food_spawned = True    
        
        
    # --- Vykreslení hada + jídla ---
    draw_points(snake + food)

    sleep(stepdelay)

