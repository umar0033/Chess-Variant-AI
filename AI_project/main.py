import pygame
import chess
import random
import sys
import time

pygame.init()
pygame.mixer.init()

# Load music
try:
    pygame.mixer.music.load("win.mp3")
    music_loaded = True
except:
    music_loaded = False

WIDTH = HEIGHT = 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess with Magic Squares")
font = pygame.font.SysFont("Arial", 36)

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
TELEPORT_COLOR = (0, 191, 255)
REPLICATE_COLOR = (186, 85, 211)
HIGHLIGHT_COLOR = (0, 255, 0)
WHITE_TEXT = (255, 255, 255)
BLACK_TEXT = (0, 0, 0)

sound_on = False
sound_icon_rect = pygame.Rect(WIDTH - 50, 10, 30, 30)

mode = None
board = chess.Board()

center_squares = [chess.square(col, row) for row in range(2, 6) for col in range(8)]
teleport_squares = random.sample(center_squares, 2)
replicate_squares = random.sample([s for s in center_squares if s not in teleport_squares], 2)
teleport_map = {teleport_squares[0]: teleport_squares[1], teleport_squares[1]: teleport_squares[0]}

def load_images():
    pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    colors = ['white', 'black']
    images = {}
    for color in colors:
        for piece in pieces:
            filename = f"{color}_{piece}.png"
            try:
                img = pygame.image.load(filename)
                images[f"{color}_{piece}"] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            except Exception as e:
                print(f"Error loading image '{filename}': {e}")
    return images


piece_images = load_images()

def draw_sound_icon():
    color = (0, 255, 0) if sound_on else (255, 0, 0)
    pygame.draw.rect(screen, color, sound_icon_rect)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (WIDTH - 45, 15), (WIDTH - 45, 35), (WIDTH - 25, 25)
    ])

def draw_text_center(text, y):
    text_surf = font.render(text, True, WHITE_TEXT)
    rect = text_surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surf, rect)

def draw_welcome():
    screen.fill((0, 0, 0))
    draw_text_center("Chess with Magic Squares", HEIGHT // 6)
    draw_text_center("Press 1  -  2 Players", HEIGHT // 3)
    draw_text_center("Press 2  -  Play vs AI", HEIGHT // 3 + 40)
    rules = ["Rules:",
        "- Two magic squares are TELEPORTERS (blue).",
        "- Move onto one to teleport to the other.",
        "- Two squares REPLICATE pawns (purple).",
        "- Step on one to duplicate your pawn forward.",
        "- Minimax AI plays as Black in AI Mode.",
        "", "By: #22k4184  |  #22k4547  |  #22k4218"]
    small_font = pygame.font.SysFont("Arial", 20)
    for i, line in enumerate(rules):
        text_surf = small_font.render(line, True, WHITE_TEXT)
        rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + i * 25))
        screen.blit(text_surf, rect)
    draw_sound_icon()
    pygame.display.flip()

def draw_board(selected_square=None):
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if square == selected_square:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

            if square in teleport_squares:
                pygame.draw.rect(screen, TELEPORT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
            elif square in replicate_squares:
                pygame.draw.rect(screen, REPLICATE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

            piece = board.piece_at(square)
            if piece:
                color_str = "white" if piece.color == chess.WHITE else "black"
                name = piece.piece_type
                types = {
                    chess.PAWN: 'pawn', chess.KNIGHT: 'knight', chess.BISHOP: 'bishop',
                    chess.ROOK: 'rook', chess.QUEEN: 'queen', chess.KING: 'king'
                }
                key = f"{color_str}_{types[name]}"
                if key in piece_images:
                    screen.blit(piece_images[key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def evaluate_board():
    value = 0
    piece_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5,
        chess.QUEEN: 9, chess.KING: 0
    }
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values[piece.piece_type]
            value += val if piece.color == chess.WHITE else -val
    return value

def minimax(depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(), None
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def make_move(move):
    board.push(move)

    if board.move_stack and board.peek().to_square in teleport_squares:
        tele_target = teleport_map[board.peek().to_square]
        teleport_move = chess.Move(board.peek().to_square, tele_target)
        if teleport_move in board.legal_moves:
            board.push(teleport_move)
        else:
            piece = board.remove_piece_at(board.peek().to_square)
            if piece:
                board.set_piece_at(tele_target, piece)

    if board.move_stack and board.peek().to_square in replicate_squares:
        sq = board.peek().to_square
        direction = -8 if board.turn == chess.WHITE else 8
        forward = sq + direction
        if 0 <= forward < 64 and board.piece_at(forward) is None:
            piece = board.piece_at(sq)
            if piece and piece.piece_type == chess.PAWN:
                rank = chess.square_rank(forward)
                if (piece.color == chess.WHITE and rank == 7) or (piece.color == chess.BLACK and rank == 0):
                    return
                board.set_piece_at(forward, chess.Piece(piece.piece_type, piece.color))

def game_loop():
    global sound_on
    selected_square = None
    while not board.is_game_over():
        draw_board(selected_square)
        draw_sound_icon()
        pygame.display.flip()

        if mode == 'ai' and board.turn == chess.BLACK:
            time.sleep(1)
            _, best_move = minimax(2, float('-inf'), float('inf'), False)
            if best_move:
                make_move(best_move)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if sound_icon_rect.collidepoint(event.pos):
                        sound_on = not sound_on
                        if sound_on and music_loaded:
                            pygame.mixer.music.play()
                        else:
                            pygame.mixer.music.stop()
                    else:
                        col, row = event.pos[0] // SQUARE_SIZE, 7 - event.pos[1] // SQUARE_SIZE
                        square = chess.square(col, row)
                        if selected_square is None:
                            piece = board.piece_at(square)
                            if piece and piece.color == board.turn:
                                selected_square = square
                        else:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                make_move(move)
                            selected_square = None

# Main entry
while True:
    draw_welcome()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 'pvp'
                game_loop()
            elif event.key == pygame.K_2:
                mode = 'ai'
                game_loop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if sound_icon_rect.collidepoint(event.pos):
                sound_on = not sound_on
                if sound_on and music_loaded:
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.stop()
