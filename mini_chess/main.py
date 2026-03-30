import pygame

from core.game_state import GameState
from core.game_manager import GameManager
from core.board import find_king
from gui.renderer import Renderer
from gui.input_handler import InputHandler
from config import (
    MODE_HUMAN_VS_HUMAN,
    MODE_HUMAN_VS_ALPHABETA,
    MODE_HUMAN_VS_MCTS,
    MODE_AI_VS_AI,
    DEFAULT_MODE,
    AI_MOVE_DELAY_MS,
)

try:
    from ai.alphabeta import AlphaBetaAI
except Exception:
    AlphaBetaAI = None

try:
    from ai.mcts import MCTSAI
except Exception:
    MCTSAI = None


BOARD_SIZE = 8
CELL_SIZE = 60
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + 120


def mode_to_name(mode):
    if mode == MODE_HUMAN_VS_HUMAN:
        return "Human vs Human"
    if mode == MODE_HUMAN_VS_ALPHABETA:
        return "Human vs AlphaBeta"
    if mode == MODE_HUMAN_VS_MCTS:
        return "Human vs MCTS"
    if mode == MODE_AI_VS_AI:
        return "AI vs AI"
    return "Unknown"


def create_manager_for_mode(mode):
    state = GameState()

    white_ai = None
    black_ai = None

    if mode == MODE_HUMAN_VS_ALPHABETA:
        black_ai = AlphaBetaAI() if AlphaBetaAI else None

    elif mode == MODE_HUMAN_VS_MCTS:
        black_ai = MCTSAI() if MCTSAI else None

    elif mode == MODE_AI_VS_AI:
        white_ai = AlphaBetaAI() if AlphaBetaAI else None
        black_ai = MCTSAI() if MCTSAI else None

    return GameManager(state, mode=mode, white_ai=white_ai, black_ai=black_ai)


def draw_menu_button(screen, rect, text, font, mouse_pos):
    base_color = (60, 60, 70)
    hover_color = (95, 95, 110)
    border_color = (220, 220, 220)

    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=12)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_menu(screen, title_font, button_font, mouse_pos):
    screen.fill((24, 26, 32))

    title = title_font.render("Mini Chess", True, (255, 255, 255))
    subtitle = button_font.render("Choose a game mode", True, (180, 180, 180))

    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 90)))
    screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_WIDTH // 2, 140)))

    buttons = {
        MODE_HUMAN_VS_HUMAN: pygame.Rect(170, 210, 300, 60),
        MODE_HUMAN_VS_ALPHABETA: pygame.Rect(170, 290, 300, 60),
        MODE_HUMAN_VS_MCTS: pygame.Rect(170, 370, 300, 60),
        MODE_AI_VS_AI: pygame.Rect(170, 450, 300, 60),
        "quit": pygame.Rect(170, 530, 300, 60),
    }

    draw_menu_button(screen, buttons[MODE_HUMAN_VS_HUMAN], "Human vs Human", button_font, mouse_pos)
    draw_menu_button(screen, buttons[MODE_HUMAN_VS_ALPHABETA], "Human vs AlphaBeta", button_font, mouse_pos)
    draw_menu_button(screen, buttons[MODE_HUMAN_VS_MCTS], "Human vs MCTS", button_font, mouse_pos)
    draw_menu_button(screen, buttons[MODE_AI_VS_AI], "AI vs AI", button_font, mouse_pos)
    draw_menu_button(screen, buttons["quit"], "Quit", button_font, mouse_pos)

    return buttons


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mini Chess")

    title_font = pygame.font.SysFont("arial", 42, bold=True)
    button_font = pygame.font.SysFont("arial", 28, bold=True)

    clock = pygame.time.Clock()
    renderer = Renderer()
    input_handler = InputHandler()

    in_menu = True
    selected_mode = DEFAULT_MODE
    manager = None
    start_ticks = 0
    last_ai_move_time = 0
    frozen_elapsed_seconds = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        if in_menu:
            buttons = draw_menu(screen, title_font, button_font, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[MODE_HUMAN_VS_HUMAN].collidepoint(event.pos):
                        selected_mode = MODE_HUMAN_VS_HUMAN
                        manager = create_manager_for_mode(selected_mode)
                        in_menu = False
                        start_ticks = pygame.time.get_ticks()
                        frozen_elapsed_seconds = 0
                        input_handler.clear_selection()

                    elif buttons[MODE_HUMAN_VS_ALPHABETA].collidepoint(event.pos):
                        selected_mode = MODE_HUMAN_VS_ALPHABETA
                        manager = create_manager_for_mode(selected_mode)
                        in_menu = False
                        start_ticks = pygame.time.get_ticks()
                        frozen_elapsed_seconds = 0
                        input_handler.clear_selection()

                    elif buttons[MODE_HUMAN_VS_MCTS].collidepoint(event.pos):
                        selected_mode = MODE_HUMAN_VS_MCTS
                        manager = create_manager_for_mode(selected_mode)
                        in_menu = False
                        start_ticks = pygame.time.get_ticks()
                        frozen_elapsed_seconds = 0
                        input_handler.clear_selection()

                    elif buttons[MODE_AI_VS_AI].collidepoint(event.pos):
                        selected_mode = MODE_AI_VS_AI
                        manager = create_manager_for_mode(selected_mode)
                        in_menu = False
                        start_ticks = pygame.time.get_ticks()
                        frozen_elapsed_seconds = 0
                        input_handler.clear_selection()

                    elif buttons["quit"].collidepoint(event.pos):
                        running = False

            pygame.display.flip()
            clock.tick(60)
            continue

        if manager is not None and manager.is_game_over():
            elapsed_seconds = frozen_elapsed_seconds
        else:
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # nút ở panel dưới
                state_for_buttons = manager.get_state()
                current_player_for_buttons = state_for_buttons.current_player
                in_check_for_buttons = manager.is_in_check(current_player_for_buttons)
                check_king_pos_for_buttons = find_king(state_for_buttons.board, current_player_for_buttons) if in_check_for_buttons else None

                bottom_buttons = renderer.draw(
                    screen,
                    state_for_buttons,
                    elapsed_seconds=elapsed_seconds,
                    mode_name=mode_to_name(selected_mode),
                    mouse_pos=mouse_pos,
                    selected_pos=input_handler.selected_pos,
                    highlight_moves=input_handler.highlight_moves,
                    in_check=in_check_for_buttons,
                    check_king_pos=check_king_pos_for_buttons,
                )

                if bottom_buttons["restart"].collidepoint(event.pos):
                    manager = create_manager_for_mode(selected_mode)
                    start_ticks = pygame.time.get_ticks()
                    frozen_elapsed_seconds = 0
                    input_handler.clear_selection()
                    continue

                if bottom_buttons["menu"].collidepoint(event.pos):
                    in_menu = True
                    input_handler.clear_selection()
                    continue

                if bottom_buttons["quit"].collidepoint(event.pos):
                    running = False
                    continue

                # click bàn cờ
                if not manager.is_game_over() and manager.is_human_turn():
                    move = input_handler.handle_click(event.pos, manager)
                    if move is not None:
                        success = manager.make_move(move)
                        if not success:
                            print("Invalid move")
                        else:
                            if manager.is_game_over():
                                frozen_elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                        input_handler.clear_selection()

        now = pygame.time.get_ticks()
        if manager.should_ai_move():
            current_ai = manager.get_current_ai()
            if current_ai is not None and now - last_ai_move_time >= AI_MOVE_DELAY_MS:
                ai_move = current_ai.choose_move(manager.get_state())
                manager.make_move(ai_move)
                if manager.is_game_over():
                    frozen_elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                input_handler.clear_selection()
                last_ai_move_time = now

        state = manager.get_state()
        current_player = state.current_player
        in_check = manager.is_in_check(current_player)
        check_king_pos = find_king(state.board, current_player) if in_check else None

        renderer.draw(
            screen,
            state,
            elapsed_seconds=elapsed_seconds,
            mode_name=mode_to_name(selected_mode),
            mouse_pos=mouse_pos,
            selected_pos=input_handler.selected_pos,
            highlight_moves=input_handler.highlight_moves,
            in_check=in_check,
            check_king_pos=check_king_pos,
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()