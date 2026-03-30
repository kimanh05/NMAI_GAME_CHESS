import pygame
import os

BOARD_SIZE = 8
CELL_SIZE = 60
BOARD_PIXELS = BOARD_SIZE * CELL_SIZE

LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
SELECT_COLOR = (100, 200, 100)
MOVE_HINT_COLOR = (80, 170, 255)
CHECK_COLOR = (220, 60, 60)


class Renderer:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18, bold=True)
        self.overlay_font = pygame.font.SysFont("arial", 34, bold=True)
        self.overlay_sub_font = pygame.font.SysFont("arial", 20, bold=True)
        self.button_font = pygame.font.SysFont("arial", 18, bold=True)

        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "assets")

        self.images = {
            "K": pygame.image.load(os.path.join(assets_path, "wK.png")).convert_alpha(),
            "R": pygame.image.load(os.path.join(assets_path, "wR.png")).convert_alpha(),
            "P": pygame.image.load(os.path.join(assets_path, "wP.png")).convert_alpha(),
            "k": pygame.image.load(os.path.join(assets_path, "bK.png")).convert_alpha(),
            "r": pygame.image.load(os.path.join(assets_path, "bR.png")).convert_alpha(),
            "p": pygame.image.load(os.path.join(assets_path, "bP.png")).convert_alpha(),
        }

    def draw_board(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)

    def draw_selected(self, screen, selected_pos):
        if selected_pos is None:
            return

        row, col = selected_pos
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SELECT_COLOR, rect, 4)

    def draw_move_hints(self, screen, highlight_moves):
        for move in highlight_moves:
            row, col = move.er, move.ec
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, MOVE_HINT_COLOR, (center_x, center_y), 7)

    def draw_check_highlight(self, screen, check_king_pos):
        if check_king_pos is None:
            return

        row, col = check_king_pos
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, CHECK_COLOR, rect, 4)

    def draw_pieces(self, screen, board):
        piece_size = int(CELL_SIZE * 0.82)

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece == ".":
                    continue

                img = self.images.get(piece)
                if img:
                    scaled = pygame.transform.smoothscale(img, (piece_size, piece_size))
                    x = col * CELL_SIZE + (CELL_SIZE - piece_size) // 2
                    y = row * CELL_SIZE + (CELL_SIZE - piece_size) // 2
                    screen.blit(scaled, (x, y))

    def format_time(self, elapsed_seconds):
        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def draw_button(self, screen, rect, text, mouse_pos):
        base_color = (60, 60, 70)
        hover_color = (95, 95, 110)
        border_color = (220, 220, 220)

        color = hover_color if rect.collidepoint(mouse_pos) else base_color
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=10)

        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw_bottom_buttons(self, screen, mouse_pos):
        button_width = 90
        button_height = 30
        gap = 10

        total_width = button_width * 3 + gap * 2
        start_x = (BOARD_PIXELS - total_width) // 2
        y = BOARD_PIXELS + 82

        restart_btn = pygame.Rect(start_x, y, button_width, button_height)
        menu_btn = pygame.Rect(start_x + button_width + gap, y, button_width, button_height)
        quit_btn = pygame.Rect(start_x + (button_width + gap) * 2, y, button_width, button_height)

        self.draw_button(screen, restart_btn, "Restart", mouse_pos)
        self.draw_button(screen, menu_btn, "Menu", mouse_pos)
        self.draw_button(screen, quit_btn, "Quit", mouse_pos)

        return {
            "restart": restart_btn,
            "menu": menu_btn,
            "quit": quit_btn,
        }

    def draw_status(
        self,
        screen,
        current_player,
        elapsed_seconds,
        mode_name,
        mouse_pos,
        game_over=False,
        result=None,
        winner=None,
        in_check=False,
    ):
        panel_y = BOARD_PIXELS
        panel_rect = pygame.Rect(0, panel_y, BOARD_PIXELS, 120)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)

        if game_over:
            if result == "checkmate":
                line1 = f"Game Over - {winner} wins"
            elif result == "stalemate":
                line1 = "Game Over - Stalemate"
            elif result == "draw":
                line1 = "Game Over - Draw"
            else:
                line1 = "Game Over"
        else:
            line1 = f"Current player: {current_player}"

        line2 = f"Time: {self.format_time(elapsed_seconds)}"
        line3 = f"Mode: {mode_name}"
        line4 = "CHECK!" if (not game_over and in_check) else "Click buttons below"

        text1 = self.small_font.render(line1, True, (255, 255, 255))
        text2 = self.small_font.render(line2, True, (255, 255, 255))
        text3 = self.small_font.render(line3, True, (255, 255, 255))
        text4 = self.small_font.render(line4, True, (255, 100, 100) if line4 == "CHECK!" else (220, 220, 220))

        screen.blit(text1, (10, BOARD_PIXELS + 8))
        screen.blit(text2, (10, BOARD_PIXELS + 30))
        screen.blit(text3, (10, BOARD_PIXELS + 52))
        screen.blit(text4, (10, BOARD_PIXELS + 74))

        return self.draw_bottom_buttons(screen, mouse_pos)

    def get_game_over_message(self, result, winner):
        if result == "draw":
            return "DRAW", "Only kings left"
        if result == "stalemate":
            return "STALEMATE", "No legal moves"
        if result == "checkmate":
            if winner is None:
                return "CHECKMATE", ""
            return "CHECKMATE", f"{winner.upper()} wins"
        return "GAME OVER", ""

    def draw_game_over_overlay(self, screen, result, winner):
        overlay = pygame.Surface((BOARD_PIXELS, BOARD_PIXELS), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        box_width = 320
        box_height = 140
        box_x = (BOARD_PIXELS - box_width) // 2
        box_y = (BOARD_PIXELS - box_height) // 2

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (35, 35, 40), box_rect, border_radius=16)
        pygame.draw.rect(screen, (230, 230, 230), box_rect, width=2, border_radius=16)

        title, subtitle = self.get_game_over_message(result, winner)

        title_surface = self.overlay_font.render(title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(BOARD_PIXELS // 2, box_y + 42))
        screen.blit(title_surface, title_rect)

        subtitle_surface = self.overlay_sub_font.render(subtitle, True, (220, 220, 220))
        subtitle_rect = subtitle_surface.get_rect(center=(BOARD_PIXELS // 2, box_y + 80))
        screen.blit(subtitle_surface, subtitle_rect)

        hint_surface = self.small_font.render("Use buttons below", True, (255, 220, 120))
        hint_rect = hint_surface.get_rect(center=(BOARD_PIXELS // 2, box_y + 112))
        screen.blit(hint_surface, hint_rect)

    def draw(
        self,
        screen,
        state,
        elapsed_seconds,
        mode_name,
        mouse_pos,
        selected_pos=None,
        highlight_moves=None,
        in_check=False,
        check_king_pos=None,
    ):
        if highlight_moves is None:
            highlight_moves = []

        self.draw_board(screen)
        self.draw_selected(screen, selected_pos)
        self.draw_move_hints(screen, highlight_moves)
        self.draw_check_highlight(screen, check_king_pos)
        self.draw_pieces(screen, state.board)

        if state.game_over:
            self.draw_game_over_overlay(screen, state.result, state.winner)

        bottom_buttons = self.draw_status(
            screen,
            current_player=state.current_player,
            elapsed_seconds=elapsed_seconds,
            mode_name=mode_name,
            mouse_pos=mouse_pos,
            game_over=state.game_over,
            result=state.result,
            winner=state.winner,
            in_check=in_check,
        )

        return bottom_buttons