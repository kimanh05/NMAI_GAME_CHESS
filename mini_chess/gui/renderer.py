import pygame
import os

BOARD_SIZE = 8
CELL_SIZE = 60
BOARD_PIXELS = BOARD_SIZE * CELL_SIZE
PANEL_HEIGHT = 140

BG_COLOR = (16, 20, 28)         # nền tổng
PANEL_COLOR = (24, 29, 38)      # panel dưới
PANEL_BORDER = (60, 70, 88)

LIGHT_COLOR = (240, 217, 181)   # ô sáng classic
DARK_COLOR = (181, 136, 99)     # ô tối classic

SELECT_COLOR = (82, 196, 110)   # ô chọn
MOVE_HINT_COLOR = (84, 160, 255) # chấm nước đi
CAPTURE_HINT_COLOR = (230, 92, 92)
CHECK_COLOR = (255, 99, 99)

BUTTON_COLOR = (58, 66, 82)
BUTTON_HOVER = (84, 96, 118)
BUTTON_TEXT = (245, 245, 245)
BUTTON_BORDER = (205, 210, 220)

TEXT_MAIN = (245, 247, 250)
TEXT_SUB = (176, 184, 196)
TEXT_ACCENT = (255, 211, 105)

OVERLAY_COLOR = (8, 10, 16, 170)
POPUP_COLOR = (30, 35, 46)
POPUP_BORDER = (220, 225, 232)


class Renderer:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("arial", 19, bold=True)
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

    def draw_background(self, screen):
        screen.fill(BG_COLOR)

    def draw_board(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)

    def draw_board_frame(self, screen):
        rect = pygame.Rect(0, 0, BOARD_PIXELS, BOARD_PIXELS)
        pygame.draw.rect(screen, (90, 70, 50), rect, width=4, border_radius=6)

    def draw_selected(self, screen, selected_pos):
        if selected_pos is None:
            return
        row, col = selected_pos
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SELECT_COLOR, rect, 4, border_radius=8)

    # def draw_move_hints(self, screen, highlight_moves):
    #     for item in highlight_moves:
    #         move, is_capture = item
    #         row, col = move.er, move.ec
    #         center_x = col * CELL_SIZE + CELL_SIZE // 2
    #         center_y = row * CELL_SIZE + CELL_SIZE // 2
            
    #         if is_capture:
    #             rect = pygame.Rect(col * CELL_SIZE + 6, row * CELL_SIZE + 6, CELL_SIZE - 12, CELL_SIZE - 12)
    #             pygame.draw.rect(screen, (220, 70, 70), rect, 4, border_radius=10)
    #         else:
    #             pygame.draw.circle(screen, MOVE_HINT_COLOR, (center_x, center_y), 7)

    def draw_move_hints(self, screen, highlight_moves):
        for move, is_capture in highlight_moves:
            row, col = move.er, move.ec
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2

            if is_capture:
                rect = pygame.Rect(col * CELL_SIZE + 6, row * CELL_SIZE + 6, CELL_SIZE - 12, CELL_SIZE - 12)
                pygame.draw.rect(screen, CAPTURE_HINT_COLOR, rect, 4, border_radius=10)
            else:
                pygame.draw.circle(screen, MOVE_HINT_COLOR, (center_x, center_y), 7)

    def draw_check_highlight(self, screen, check_king_pos):
        if check_king_pos is None:
            return
        row, col = check_king_pos
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, CHECK_COLOR, rect, 4, border_radius=8)

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
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=14)
        pygame.draw.rect(screen, BUTTON_BORDER, rect, width=2, border_radius=14)

        text_surface = self.button_font.render(text, True, BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        
    def draw_bottom_buttons(self, screen, mouse_pos):
        button_width = 104
        button_height = 36
        gap = 14

        total_width = button_width * 3 + gap * 2
        start_x = (BOARD_PIXELS - total_width) // 2
        y = BOARD_PIXELS + 94

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

    def draw_status(self, screen, current_player, elapsed_seconds, mode_name, mouse_pos, game_over=False, result=None, winner=None, in_check=False, ai_thinking=False,):
        panel_y = BOARD_PIXELS
        panel_rect = pygame.Rect(0, panel_y, BOARD_PIXELS, 140)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect)
        pygame.draw.line(screen, PANEL_BORDER, (0, panel_y), (BOARD_PIXELS, panel_y), 2)

        line1 = f"Turn: {current_player.capitalize()}"
        if mode_name == "AI vs AI":
            line2 = f"Time: {self.format_time(elapsed_seconds)}    White: AlphaBeta   Black: MCTS"
        else:
            line2 = f"Time: {self.format_time(elapsed_seconds)}    Mode: {mode_name}"


        if game_over:
            if result == "draw":
                line3 = "Result: Draw"
            elif result == "threefold_repetition":
                line3 = "Result: Draw by repetition"
            elif result == "stalemate":
                line3 = "Result: Stalemate"
            elif result == "checkmate":
                line3 = f"Result: {winner.capitalize()} wins"
            else:
                line3 = "Result: Game Over"
        else:
            if in_check:
                line3 = "Status: CHECK!"
            elif ai_thinking:
                line3 = "Status: AI is thinking..."
            else:
                line3 = "Status: Ready"

        text1 = self.small_font.render(line1, True, TEXT_MAIN)
        text2 = self.small_font.render(line2, True, TEXT_SUB)
        text3 = self.small_font.render(line3, True, TEXT_ACCENT if ("CHECK" in line3 or "thinking" in line3.lower()) else TEXT_MAIN)

        screen.blit(text1, (14, BOARD_PIXELS + 10))
        screen.blit(text2, (14, BOARD_PIXELS + 36))
        screen.blit(text3, (14, BOARD_PIXELS + 62))

        return self.draw_bottom_buttons(screen, mouse_pos)

    def get_game_over_message(self, result, winner):
        if result == "draw":
            return "DRAW", "Only kings left"
        if result == "threefold_repetition":
            return "DRAW", "Threefold repetition"
        if result == "stalemate":
            return "STALEMATE", "No legal moves"
        if result == "checkmate":
            if winner is None:
                return "CHECKMATE", ""
            return "CHECKMATE", f"{winner.upper()} wins"
        return "GAME OVER", ""

    def draw_game_over_overlay(self, screen, result, winner):
        overlay = pygame.Surface((BOARD_PIXELS, BOARD_PIXELS), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))

        box_width = 340
        box_height = 150
        box_x = (BOARD_PIXELS - box_width) // 2
        box_y = (BOARD_PIXELS - box_height) // 2

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, POPUP_COLOR, box_rect, border_radius=18)
        pygame.draw.rect(screen, POPUP_BORDER, box_rect, width=2, border_radius=18)

        title, subtitle = self.get_game_over_message(result, winner)

        title_surface = self.overlay_font.render(title, True, TEXT_MAIN)
        subtitle_surface = self.overlay_sub_font.render(subtitle, True, TEXT_SUB)
        hint_surface = self.small_font.render("Use buttons below", True, TEXT_ACCENT)

        screen.blit(title_surface, title_surface.get_rect(center=(BOARD_PIXELS // 2, box_y + 42)))
        screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(BOARD_PIXELS // 2, box_y + 82)))
        screen.blit(hint_surface, hint_surface.get_rect(center=(BOARD_PIXELS // 2, box_y + 118)))

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
        ai_thinking=False,
    ):
        if highlight_moves is None:
            highlight_moves = []

        self.draw_background(screen)
        self.draw_board(screen)
        self.draw_selected(screen, selected_pos)
        self.draw_move_hints(screen, highlight_moves)
        self.draw_check_highlight(screen, check_king_pos)
        self.draw_pieces(screen, state.board)
        self.draw_board_frame(screen)

        if state.game_over:
            self.draw_game_over_overlay(screen, state.result, state.winner)

        return self.draw_status(
            screen,
            current_player=state.current_player,
            elapsed_seconds=elapsed_seconds,
            mode_name=mode_name,
            mouse_pos=mouse_pos,
            game_over=state.game_over,
            result=state.result,
            winner=state.winner,
            in_check=in_check,
            ai_thinking=ai_thinking,
        )