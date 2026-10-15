from time import monotonic

from textual.app import App, ComposeResult
from textual.color import Color
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header, Static, Select
from tetrisplay import check_cell_state, check_for_game_over, drop_block, move_block, check_for_filled_row, _INTERVAL
from tetrisplay import _ROWS, _COLUMNS

saved_grid = None

class Cell(Static):
    filled = reactive(False)
    colour = reactive("")

    def watch_filled(self, filled: bool) -> None:
        self.set_class(filled, "filled")

    def watch_colour(self, colour: str) -> None:
        self.styles.background = colour or None

class TetrisApp(App):
    """A Textual app to manage tetris."""

    CSS_PATH = "tetris.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("left", "move(-1)", "Left"),
        ("right", "move(1)", "Right"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()

        self.cells = [[Cell() for x in range(_COLUMNS)] for y in range(_ROWS)]
        for row in self.cells:
            yield from row

        # yield Select((str(number), number) for number in range(20))

    def on_mount(self) -> None:
        self.screen.styles.grid_size_columns = _COLUMNS
        self.screen.styles.grid_size_rows = _ROWS
        self.refresh_board()
        self.timer = self.set_interval(_INTERVAL, self.game_loop)

    def game_loop(self) -> None:
        if check_for_game_over(saved_grid):
            self.timer.stop()
            self.notify("Game Over")
            return
        drop_block(saved_grid)
        check_for_filled_row(saved_grid)
        self.refresh_board()


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_move(self, direction:int) -> None:
        move_block(saved_grid, direction)
        self.refresh_board()

    def refresh_board(self) -> None:
        for x in range(10):
            for y in range(5):
                self.cells[x][y].colour = cell_state(y, x)

def start(grid):
    app = TetrisApp()
    global saved_grid
    saved_grid = grid
    app.run()


def cell_state(x, y):
    return check_cell_state(x, y, saved_grid)
