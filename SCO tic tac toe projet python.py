# =========================================================
# 1.  Le jeu SCOPIONS - TIC TAC TOE
# =========================================================

import pygame
import sys
import math
import random

# =========================
# CONFIGURATION GRAPHIQUE GÉNÉRALE
# =========================
WIDTH, HEIGHT = 900, 600
FPS = 32

BACKGROUND_COLOR = (76, 8, 20)
GOLD = (212, 175, 55)
ORANGE = (225, 193, 2)
BLUE = (200, 140, 87)
WHITE = (230, 230, 230)
RED = (220, 60, 60)

GRID_SIZE = 4
CELL_SIZE = 61

PLAYER_NUMBERS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
IA_NUMBERS = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
OPERATORS = ["+", "-", "×", "÷"]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# --- LOGO SCORPION ---
logo = pygame.image.load(r"C:\Users\Utilisateur\Downloads\scopions.tic.tac.png").convert_alpha()
logo = pygame.transform.scale(logo, (900, 600))
logo.set_alpha(38)

pygame.display.set_caption(" ♦ Scopions TIC TAC TOE ♦")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 48)
small_font = pygame.font.SysFont("consolas", 18)

# =========================
# AJOUT DU MENU (NOUVEAU)
# =========================
MENU_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 75, 350, 150, 50)

# === FOND DU MENU ===
menu_bg = pygame.image.load(r"C:\Users\Utilisateur\Downloads\IMG_4419.jpeg").convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

# =========================
# OUTILS
# =========================
def rotate_point(x, y, cx, cy, angle_rad):
    dx, dy = x - cx, y - cy
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    rx = cx + dx * cos_a - dy * sin_a
    ry = cy + dx * sin_a + dy * cos_a
    return rx, ry


def compute_cells():
    center_x, center_y = WIDTH // 2, HEIGHT // 2 - 50
    angle = math.radians(45)

    grid_pixel_size = GRID_SIZE * CELL_SIZE
    top_left_x = center_x - grid_pixel_size // 2
    top_left_y = center_y - grid_pixel_size // 2

    cells = []

    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            x = top_left_x + c * CELL_SIZE
            y = top_left_y + r * CELL_SIZE

            p1 = rotate_point(x, y, center_x, center_y, angle)
            p2 = rotate_point(x + CELL_SIZE, y, center_x, center_y, angle)
            p3 = rotate_point(x + CELL_SIZE, y + CELL_SIZE, center_x, center_y, angle)
            p4 = rotate_point(x, y + CELL_SIZE, center_x, center_y, angle)

            row.append([p1, p2, p3, p4])
        cells.append(row)

    return cells


# =========================
# PARTICULES
# =========================
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(20, 40)
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = max(50, int(255 * (self.life / 40)))
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
            surface.blit(s, (self.x - self.size, self.y - self.size))


def spawn_particles_for_cell(cells, r, c, color, particles):
    poly = cells[r][c]
    cx = sum([p[0] for p in poly]) / 4
    cy = sum([p[1] for p in poly]) / 4
    for _ in range(15):
        particles.append(Particle(cx, cy, color))


# =========================
# DESSIN DE LA GRILLE
# =========================
def draw_grid(cells, board, selected):
    mouse_pos = pygame.mouse.get_pos()
    mx, my = mouse_pos

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            poly = cells[r][c]

            if board[r][c] is None:
                pygame.draw.polygon(screen, GOLD, poly, 2)
            else:
                owner = board[r][c]["owner"]
                color = ORANGE if owner == "player" else BLUE
                pygame.draw.polygon(screen, color, poly, 3)

            if selected == (r, c):
                pygame.draw.polygon(screen, ORANGE, poly, 4)

            if point_in_poly(mx, my, poly):
                pygame.draw.polygon(screen, (255, 237, 35), poly, 3)

            if board[r][c] is not None:
                val = board[r][c]["value"]
                txt = font.render(str(val), True, WHITE)
                cx = sum([p[0] for p in poly]) / 4
                cy = sum([p[1] for p in poly]) / 4
                screen.blit(txt, (cx - txt.get_width() / 2, cy - txt.get_height() / 2))


# =========================
# PAVÉ NUMÉRIQUE
# =========================
def build_keypad():
    buttons = []
    x0, y0 = 120, HEIGHT - 200
    w, h = 60, 40
    spacing = 10

    num = 1
    for row in range(5):
        for col in range(4):
            rect = pygame.Rect(
                x0 + col * (w + spacing),
                y0 + row * (h + spacing),
                w,
                h
            )
            buttons.append((rect, num))
            num += 1

    return buttons


def draw_keypad(buttons, selected_number):
    mouse_pos = pygame.mouse.get_pos()

    for rect, value in buttons:
        if rect.collidepoint(mouse_pos):
            bg_color = (60, 15, 20)
        else:
            bg_color = (15, 20, 40)

        border_color = ORANGE if value == selected_number else GOLD

        pygame.draw.rect(screen, bg_color, rect, border_radius=6)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=6)

        txt = small_font.render(str(value), True, WHITE)
        screen.blit(
            txt,
            (rect.x + rect.width // 2 - txt.get_width() // 2,
             rect.y + rect.height // 2 - txt.get_height() // 2)
        )
        
         # --- Losange pour les chiffres impairs ---
        if value % 2 == 1:  # impair
            size = 4  # taille du losange

            # Position du losange (ajustée pour TON pavé numérique)
            cx = rect.x + rect.width - 20   # légèrement à droite du texte
            cy = rect.y + rect.height - 15 # centré verticalement

            diamond = [
                (cx, cy - size),      # haut
                (cx + size, cy),      # droite
                (cx, cy + size),      # bas
                (cx - size, cy)       # gauche
            ]

            pygame.draw.polygon(screen, (100,78,25), diamond)


def detect_keypad_click(buttons, mouse_pos):
    for rect, value in buttons:
        if rect.collidepoint(mouse_pos):
            return value
    return None


# =========================
# OPÉRATEURS + ANNULER
# =========================
def build_operator_buttons():
    ops = ["+", "-", "×", "÷"]
    buttons = []

    x0, y0 = WIDTH - 240, HEIGHT - 200
    w, h = 60, 40
    spacing = 10

    for i, op in enumerate(ops):
        rect = pygame.Rect(x0, y0 + i * (h + spacing), w, h)
        buttons.append((rect, op))

    cancel_rect = pygame.Rect(x0 + 80, y0, 100, 40)
    buttons.append((cancel_rect, "ANNULER"))

    return buttons


def draw_operator_buttons(buttons, selected_op):
    mouse_pos = pygame.mouse.get_pos()

    for rect, op in buttons:
        if rect.collidepoint(mouse_pos):
            bg_color = (60, 30, 20)
        else:
            bg_color = (15, 20, 40)

        if op == "ANNULER":
            pygame.draw.rect(screen, bg_color, rect, border_radius=6)
            pygame.draw.rect(screen, RED, rect, 2, border_radius=6)

            txt = small_font.render(op, True, WHITE)
            screen.blit(
                txt,
                (rect.x + rect.width // 2 - txt.get_width() // 2,
                 rect.y + rect.height // 2 - txt.get_height() // 2)
            )
            continue

        border_color = ORANGE if op == selected_op else GOLD

        pygame.draw.rect(screen, bg_color, rect, border_radius=6)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=6)

        txt = small_font.render(op, True, WHITE)
        screen.blit(
            txt,
            (rect.x + rect.width // 2 - txt.get_width() // 2,
             rect.y + rect.height // 2 - txt.get_height() // 2)
        )


def detect_operator_click(buttons, mouse_pos):
    for rect, op in buttons:
        if rect.collidepoint(mouse_pos):
            return op
    return None


# =========================
# GHOST CALC
# =========================
def draw_ghost_calc(selected_number, selected_op, preview_result):
    ghost_rect = pygame.Rect(WIDTH - 260, 80, 220, 160)
    pygame.draw.rect(screen, (20, 30, 60), ghost_rect, border_radius=10)
    pygame.draw.rect(screen, GOLD, ghost_rect, 2, border_radius=10)

    title = font.render("CALCULE FANTOME", True, ORANGE)
    screen.blit(title, (ghost_rect.x + 20, ghost_rect.y + 15))

    if preview_result:
        txt = font.render(preview_result, True, ORANGE)
        screen.blit(txt, (ghost_rect.x + 20, ghost_rect.y + 70))
        return

    if selected_number and not selected_op:
        txt = font.render(str(selected_number), True, ORANGE)
        screen.blit(txt, (ghost_rect.x + 20, ghost_rect.y + 70))

    if selected_number and selected_op:
        txt = font.render(f"{selected_number} {selected_op}", True, ORANGE)
        screen.blit(txt, (ghost_rect.x + 20, ghost_rect.y + 70))


# =========================
# CALCUL
# =========================
def compute(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "×":
        return a * b
    if op == "÷":
        if b == 0:
            return None
        return a // b
    return None


# =========================
# DÉTECTION DE CLIC SUR UNE CASE
# =========================
def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    px1, py1 = poly[0]

    for i in range(n + 1):
        px2, py2 = poly[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                    if px1 == px2 or x <= xinters:
                        inside = not inside
        px1, py1 = px2, py2

    return inside


def detect_cell_click(cells, mouse_pos):
    mx, my = mouse_pos
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if point_in_poly(mx, my, cells[r][c]):
                return (r, c)
    return None


# =========================
# IA
# =========================
def ai_possible_moves(board):
    moves = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] is None:
                moves.append((r, c))
    return moves


def ai_find_possible_win(board, owner, target_score):
    moves = ai_possible_moves(board)

    for r, c in moves:
        temp = [row[:] for row in board]

        if owner == "ia":
            num = random.choice(IA_NUMBERS)
        else:
            num = random.choice(PLAYER_NUMBERS)

        temp[r][c] = {"value": num, "owner": owner}

        if check_victory(temp, target_score, owner):
            return (r, c)

    return None


def ai_play(board, cells, particles, target_score):
    moves = ai_possible_moves(board)
    if not moves:
        return

    win_move = ai_find_possible_win(board, "ia", target_score)
    if win_move:
        r, c = win_move
        num = random.choice(IA_NUMBERS)
        board[r][c] = {"value": num, "owner": "ia"}
        spawn_particles_for_cell(cells, r, c, BLUE, particles)
        return

    block_move = ai_find_possible_win(board, "player", target_score)
    if block_move:
        r, c = block_move
        num = random.choice(IA_NUMBERS)
        board[r][c] = {"value": num, "owner": "ia"}
        spawn_particles_for_cell(cells, r, c, BLUE, particles)
        return

    r, c = random.choice(moves)
    num = random.choice(IA_NUMBERS)
    board[r][c] = {"value": num, "owner": "ia"}
    spawn_particles_for_cell(cells, r, c, BLUE, particles)


# =========================
# SCORE & VICTOIRE
# =========================
def compute_player_points(board, owner):
    total = 0
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = board[r][c]
            if cell and cell["owner"] == owner:
                total += cell["value"]
    return total


def get_lines():
    lines = []

    for r in range(GRID_SIZE):
        lines.append([(r, c) for c in range(GRID_SIZE)])

    for c in range(GRID_SIZE):
        lines.append([(r, c) for r in range(GRID_SIZE)])

    lines.append([(i, i) for i in range(GRID_SIZE)])
    lines.append([(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)])

    return lines


def check_victory(board, target_score, owner):
    lines = get_lines()

    for line in lines:
        triplets = [
            (line[0], line[1], line[2]),
            (line[1], line[2], line[3])
        ]
        for a, b, c in triplets:
            values = []
            ok = True
            for (r, col) in (a, b, c):
                cell = board[r][col]
                if not cell or cell["owner"] != owner:
                    ok = False
                    break
                values.append(cell["value"])
            if ok and sum(values) == target_score:
                return True
    return False


def board_full(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] is None:
                return False
    return True


# =========================
# RENDU DU JEU
# =========================
def render_game(
    cells,
    board,
    selected_cell,
    keypad,
    selected_number,
    op_buttons,
    selected_op,
    preview_result,
    particles,
    player_points,
    target_score,
    remaining_time,
    game_state,
    message
):
    screen.fill(BACKGROUND_COLOR)

    # Logo en fond
    screen.blit(logo, (0, 0))

    # Titre
    title = font.render(" ♦ Scopions Tic Tac Toe ♦ ", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # Grille
    draw_grid(cells, board, selected_cell)

    # Pavé numérique
    draw_keypad(keypad, selected_number)

    # Opérateurs
    draw_operator_buttons(op_buttons, selected_op)

    # Ghost calc
    draw_ghost_calc(selected_number, selected_op, preview_result)

    # Particules
    for p in particles:
        p.draw(screen)

    # Score
    score_text = font.render(f"Points : {player_points} / {target_score}", True, GOLD)
    screen.blit(score_text, (20, 20))

    # Temps
    time_color = GOLD if remaining_time > 20 else RED
    time_text = font.render(f"Temps : {int(remaining_time)} s", True, time_color)
    screen.blit(time_text, (WIDTH - time_text.get_width() - 20, 20))

    # Écrans de fin
    if game_state in ("victory", "defeat", "nul"):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        if game_state == "victory":
            msg_color = ORANGE
        elif game_state == "defeat":
            msg_color = RED
        else:
            msg_color = WHITE

        msg_txt = big_font.render(message, True, msg_color)
        screen.blit(
            msg_txt,
            (WIDTH // 2 - msg_txt.get_width() // 2,
             HEIGHT // 2 - msg_txt.get_height() // 2 - 20)
        )

        info_txt = font.render("Appuie sur ESPACE pour continuer a jouer", True, GOLD)
        screen.blit(
            info_txt,
            (WIDTH // 2 - info_txt.get_width() // 2,
             HEIGHT // 2 - info_txt.get_height() // 2 + 40)
        )

    pygame.display.flip()


# =========================
# BOUCLE PRINCIPALE (AVEC MENU)
# =========================
def main():
    target_score = 30
    round_time = 120.0

    # --- ÉTAT INITIAL : MENU ---
    game_state = "menu"

    # Bouton du menu (petit bouton jaune)
    button_rect = pygame.Rect(WIDTH // 2 - 378, 350, 150, 50)

    cells = compute_cells()
    keypad = build_keypad()
    op_buttons = build_operator_buttons()

    selected_cell = None
    selected_number = None
    selected_op = None

    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    particles = []

    message = ""
    remaining_time = round_time

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # =========================
        # ÉCRAN D'ACCUEIL
        # =========================
        if game_state == "menu":
            # Fond d'écran du menu
            screen.blit(menu_bg, (0, 0))

            title = big_font.render("♦ SCOPIONS TIC TAC TOE ♦", True, GOLD)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

            # Bouton jaune
            pygame.draw.rect(screen, ORANGE, button_rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, button_rect, 3, border_radius=10)

            txt = font.render("JOUER", True, WHITE)
            screen.blit(
                txt,
                (button_rect.x + button_rect.width // 2 - txt.get_width() // 2,
                 button_rect.y + button_rect.height // 2 - txt.get_height() // 2)
            )

            pygame.display.flip()

            # Gestion des événements du menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mx, my):
                        game_state = "playing"

            continue  # On reste dans le menu tant qu'on n'a pas cliqué

        # =========================
        # LOGIQUE DU JEU 
        # =========================
        if game_state == "playing":
            remaining_time -= dt
            if remaining_time <= 0:
                remaining_time = 0
                game_state = "defeat"
                message = "|DÉFAITE (Temps écoulé)| "

        preview_result = None

        if game_state == "playing":
            if selected_number and selected_op and selected_cell:
                cell_val = board[selected_cell[0]][selected_cell[1]]
                if cell_val:
                    b = cell_val["value"]
                    res = compute(selected_number, selected_op, b)
                    if res is not None:
                        preview_result = f"{selected_number} {selected_op} {b} = {res}"

        # =========================
        # GESTION DES ÉVÉNEMENTS DU JEU
        # =========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Écrans de fin
            if game_state in ("victory", "defeat", "nul"):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    particles = []
                    selected_cell = None
                    selected_number = None
                    selected_op = None

                    if game_state == "victory":
                        target_score += 30

                    remaining_time = round_time
                    game_state = "playing"
                    message = ""
                continue

            # Clics en jeu
            if game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                clicked_cell = detect_cell_click(cells, pos)
                if clicked_cell:
                    selected_cell = clicked_cell

                    # Pose simple
                    if selected_number and not selected_op:
                        if board[selected_cell[0]][selected_cell[1]] is None:
                            board[selected_cell[0]][selected_cell[1]] = {
                                "value": selected_number,
                                "owner": "player"
                            }
                            spawn_particles_for_cell(
                                cells,
                                selected_cell[0],
                                selected_cell[1],
                                ORANGE,
                                particles
                            )
                            selected_number = None
                            selected_cell = None

                            if check_victory(board, target_score, "player"):
                                game_state = "victory"
                                message = "| ☺ TU AS GAGNEZ GG ☺ | "
                            else:
                                ai_play(board, cells, particles, target_score)
                                if check_victory(board, target_score, "ia"):
                                    game_state = "defeat"
                                    message = "DÉFAITE... dommage, appuie sur espace pour rejouer"

                    # Assimilation
                    elif selected_number and selected_op:
                        target = board[selected_cell[0]][selected_cell[1]]
                        if target:
                            b = target["value"]
                            res = compute(selected_number, selected_op, b)
                            if res is not None:
                                board[selected_cell[0]][selected_cell[1]] = {
                                    "value": res,
                                    "owner": "player"
                                }
                                spawn_particles_for_cell(
                                    cells,
                                    selected_cell[0],
                                    selected_cell[1],
                                    ORANGE,
                                    particles
                                )
                                selected_number = None
                                selected_op = None
                                selected_cell = None

                                if check_victory(board, target_score, "player"):
                                    game_state = "victory"
                                    message = " |☺ BIEN JOUÉ TU AS GAGNÉ ☺| "
                                else:
                                    ai_play(board, cells, particles, target_score)
                                    if check_victory(board, target_score, "ia"):
                                        game_state = "defeat"
                                        message = "|TU AS PERDU| "

                clicked_number = detect_keypad_click(keypad, pos)
                if clicked_number in PLAYER_NUMBERS:
                    selected_number = clicked_number

                clicked_op = detect_operator_click(op_buttons, pos)
                if clicked_op:
                    if clicked_op == "ANNULER":
                        selected_number = None
                        selected_op = None
                        selected_cell = None
                    else:
                        selected_op = clicked_op

        # Match nul
        if game_state == "playing" and board_full(board):
            if not check_victory(board, target_score, "player") and not check_victory(board, target_score, "ia"):
                game_state = "nul"
                message = "|MATCH NUL|"

        # Particules
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)

        # =========================
        # RENDU 
        # =========================
        render_game(
            cells,
            board,
            selected_cell,
            keypad,
            selected_number,
            op_buttons,
            selected_op,
            preview_result,
            particles,
            compute_player_points(board, "player"),
            target_score,
            remaining_time,
            game_state,
            message
        )

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

   