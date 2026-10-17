import tkinter as tk
import random, threading, queue, json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ===================== CONFIG =====================
CELL = 20
SPEED = 140
MODEL_PATH = r"D:\vs code\Automation\sample Projects\Tools for voice\vosk-model-small-en-us-0.15"
HIGHSCORE_FILE = "highscore.txt"

# Colors
BG_TOP = "#020617"
BG_BOTTOM = "#050a1f"
GRID_COLOR = "#1f2937"
SNAKE_CORE = "#0ef70e"
SNAKE_GLOW = "#010202"
FOOD_CORE = "#fd0909"
FOOD_GLOW = "#f61448"

ACCENT = "#38bdf8"
TEXT = "#e5e7eb"
DIM = "#000000"

# ===================== LOAD HIGHSCORE =====================
try:
    with open(HIGHSCORE_FILE, "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# ===================== WINDOW =====================
root = tk.Tk()
root.title("NEON VOICE SNAKE")
root.state("zoomed")
root.configure(bg="black")

# ===================== GRADIENT =====================
def draw_gradient(canvas, w, h, c1, c2, steps=160):
    r1,g1,b1 = canvas.winfo_rgb(c1)
    r2,g2,b2 = canvas.winfo_rgb(c2)
    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps) >> 8
        g = int(g1 + (g2 - g1) * i / steps) >> 8
        b = int(b1 + (b2 - b1) * i / steps) >> 8
        y1 = int(h * i / steps)
        y2 = int(h * (i + 1) / steps)
        canvas.create_rectangle(
            0, y1, w, y2,
            fill=f"#{r:02x}{g:02x}{b:02x}", outline=""
        )

# ===================== HUD =====================
hud = tk.Canvas(root, height=100, highlightthickness=0)
hud.pack(fill="x")

def draw_hud():
    hud.delete("all")
    w = root.winfo_width()
    draw_gradient(hud, w, 100, "#020617", "#020b2d")
    hud.create_text(w//2, 38, text="VOICE CONTROLLED SNAKE",
                    fill=ACCENT, font=("Segoe UI", 26, "bold"))
    hud.create_text(w//2, 70, text="Say  UP   DOWN   LEFT   RIGHT",
                    fill="#94a3b8", font=("Segoe UI", 12))

# ===================== GAME CANVAS =====================
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# ===================== GAME STATE =====================
snake = []
direction = "Right"
food = (0, 0)
game_over = False
score = 0

def grid_size():
    w, h = canvas.winfo_width(), canvas.winfo_height()
    return w - w % CELL, h - h % CELL

# ===================== DRAW GAME =====================
def draw_game():
    canvas.delete("all")
    w, h = grid_size()

    draw_gradient(canvas, w, h, BG_TOP, BG_BOTTOM)

    for x in range(0, w, CELL):
        canvas.create_line(x, 0, x, h, fill=GRID_COLOR)
    for y in range(0, h, CELL):
        canvas.create_line(0, y, w, y, fill=GRID_COLOR)

    for x, y in snake:
        canvas.create_rectangle(x-3, y-3, x+CELL+3, y+CELL+3,
                                fill=SNAKE_GLOW, outline="")
        canvas.create_rectangle(x, y, x+CELL, y+CELL,
                                fill=SNAKE_CORE, outline="")

    fx, fy = food
    canvas.create_rectangle(fx, fy, fx+CELL, fy+CELL,
                       fill=FOOD_CORE, outline="")

    # 🔥 SCORE DISPLAY
    canvas.create_text(20, 20, anchor="nw",
                       text=f"Score: {score}",
                       fill=TEXT, font=("Segoe UI", 14, "bold"))
    canvas.create_text(w-20, 20, anchor="ne",
                       text=f"High Score: {high_score}",
                       fill=TEXT, font=("Segoe UI", 14, "bold"))

# ===================== GAME OVER =====================
def show_game_over():
    global high_score
    w, h = grid_size()

    if score > high_score:
        high_score = score
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(high_score))

    canvas.create_rectangle(0, 0, w, h,
                            fill=DIM, stipple="gray50", outline="")

    canvas.create_text(w//2, h//2 - 60,
                       text="YOU GREW FAST.\nNOT SMART.",
                       fill=TEXT, font=("Segoe UI", 40, "bold"),
                       justify="center")

    btn = tk.Button(root, text="RESTART",
                    font=("Segoe UI", 16, "bold"),
                    bg=ACCENT, fg="black",
                    padx=40, pady=14,
                    relief="flat",
                    command=start_game)
    canvas.create_window(w//2, h//2 + 40, window=btn)

# ===================== MOVE =====================
def move():
    global game_over, food, score

    if game_over:
        return

    x, y = snake[0]
    if direction == "Up": y -= CELL
    if direction == "Down": y += CELL
    if direction == "Left": x -= CELL
    if direction == "Right": x += CELL

    w, h = grid_size()
    head = (x, y)

    if x < 0 or y < 0 or x >= w or y >= h or head in snake:
        game_over = True
        show_game_over()
        return

    snake.insert(0, head)

    hx, hy = head
    fx, fy = food

    if abs(hx - fx) < CELL and abs(hy - fy) < CELL:
        score += 1
        food = spawn_food()
    else:
        snake.pop()

    draw_game()
    root.after(SPEED, move)

# ===================== VOICE CONTROL =====================
def listen_voice():
    global direction
    q = queue.Queue()
    last = None

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    recognizer = KaldiRecognizer(
        Model(MODEL_PATH), 16000,
        '["up","down","left","right"]'
    )

    with sd.RawInputStream(
    samplerate=16000,
    blocksize=4000,
    dtype="int16",
    channels=1,
    callback=callback
):
        while True:
            data = q.get()
            text = json.loads(recognizer.PartialResult()).get("partial", "")
            if text:
                cmd = text.split()[-1]
                if cmd != last:
                    last = cmd
                    if "up" in cmd and direction != "Down":
                        direction = "Up"
                    elif "down" in cmd and direction != "Up":
                        direction = "Down"
                    elif "left" in cmd and direction != "Right":
                        direction = "Left"
                    elif "right" in cmd and direction != "Left":
                        direction = "Right"
            recognizer.AcceptWaveform(data)

def spawn_food():
    w, h = grid_size()
    while True:
        pos = (
            random.randrange(0, w, CELL),
            random.randrange(0, h, CELL)
        )
        if pos not in snake:
            return pos

# ===================== START / RESTART =====================
def start_game():
    global snake, food, direction, game_over, score
    game_over = False
    direction = "Right"
    score = 0
    w, h = grid_size()
    snake = [(w//2, h//2), (w//2 - CELL, h//2)]
    food = spawn_food()
    draw_game()
    move()

# ===================== INIT =====================
threading.Thread(target=listen_voice, daemon=True).start()
root.after(300, lambda: (draw_hud(), start_game()))
root.mainloop()
