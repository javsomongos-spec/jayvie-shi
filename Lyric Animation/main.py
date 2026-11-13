
import pygame
import sys
import random
import ctypes

pygame.init()

# SCREEN SETTINGS
WIDTH = 400
HEIGHT = 300

# BORDERLESS WINDOW
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.NOFRAME
)

pygame.display.set_caption("Floating Lyrics")
clock = pygame.time.Clock()

# WINDOWS TRANSPARENCY
hwnd = pygame.display.get_wm_info()["window"]
user32 = ctypes.windll.user32

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
LWA_COLORKEY = 0x1

style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

user32.SetWindowLongW(
    hwnd,
    GWL_EXSTYLE,
    style | WS_EX_LAYERED
)

# MAGENTA BECOMES TRANSPARENT
TRANSPARENT = (255, 0, 255)
COLORKEY = 0x00FF00FF

user32.SetLayeredWindowAttributes(
    hwnd,
    COLORKEY,
    0,
    LWA_COLORKEY
)

# KEEP WINDOW ON TOP
HWND_TOPMOST = -1

user32.SetWindowPos(
    hwnd,
    HWND_TOPMOST,
    0, 0, 0, 0,
    0x0001 | 0x0002 | 0x0010
)

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FONT
font = pygame.font.SysFont("Arial", 15, bold=True)

# LYRICS
lyrics = [
    "Chasin' a heart is like chasin' a ghost",
    "You can't make somebody you love feel the same",
    "If they don't",
    "It doesn't matter the words that you say",
    "People change",
    "I'd drive through the night",
    "Walk a thousand miles",
    "To feel your head on my chest",
    "I'd give anything",
    "That's what's killing me",
    "The silence is getting too cold",
    "We stop fighting",
    "Deep down inside, we both know",
    "What do you want, baby?",
    "Do you only love me because you have to?",
    "All of your friends were all of mine first",
    "I can't see tomorrow without you today",
    "I'd rather let you go",
    "I'm so sorry, I wish I could be",
    "The one to love you more"
]

# ANIMATION SETTINGS
CARD_WIDTH = 175
PADDING = 12
LINE_HEIGHT = 18

DURATION = 4500
SPAWN_INTERVAL = 1400

active_cards = []
current_lyric = 0
last_spawn = 0


# WRAP TEXT
def wrap_text(text):

    words = text.split()
    lines = []
    current = ""

    for word in words:

        test = (current + " " + word).strip()

        if font.size(test)[0] <= CARD_WIDTH - PADDING * 2:
            current = test
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


# CREATE CARD
def create_card():

    global current_lyric

    text = lyrics[current_lyric]
    lines = wrap_text(text)

    card_height = len(lines) * LINE_HEIGHT + PADDING * 2

    x = random.randint(5, WIDTH - CARD_WIDTH - 5)

    active_cards.append({
        "lines": lines,
        "x": x,
        "height": card_height,
        "start": pygame.time.get_ticks()
    })

    current_lyric = (current_lyric + 1) % len(lyrics)


# DRAW CARD
def draw_card(card):

    elapsed = pygame.time.get_ticks() - card["start"]
    progress = elapsed / DURATION

    y = HEIGHT + 10 - (HEIGHT + card["height"] + 20) * progress

    alpha = 255

    if progress > 0.80:
        alpha = int(255 * (1 - (progress - 0.80) / 0.20))

    card_surface = pygame.Surface(
        (CARD_WIDTH, card["height"]),
        pygame.SRCALPHA
    )

    # BLACK CARD
    card_surface.fill((0, 0, 0, alpha))

    text_y = PADDING

    for line in card["lines"]:

        # WHITE TEXT
        rendered = font.render(line, True, WHITE)
        rendered.set_alpha(alpha)

        text_x = (CARD_WIDTH - rendered.get_width()) // 2

        card_surface.blit(rendered, (text_x, text_y))

        text_y += LINE_HEIGHT

    screen.blit(card_surface, (card["x"], int(y)))


# FIRST CARD
create_card()
last_spawn = pygame.time.get_ticks()

# MAIN LOOP
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                create_card()
                last_spawn = pygame.time.get_ticks()

    current_time = pygame.time.get_ticks()

    # SPAWN NEW CARDS
    if current_time - last_spawn >= SPAWN_INTERVAL:

        create_card()
        last_spawn = current_time

    # TRANSPARENT BACKGROUND
    screen.fill(TRANSPARENT)

    # DRAW ALL CARDS
    for card in active_cards[:]:

        elapsed = current_time - card["start"]

        if elapsed >= DURATION:
            active_cards.remove(card)
            continue

        draw_card(card)

    pygame.display.flip()

pygame.quit()
sys.exit()
