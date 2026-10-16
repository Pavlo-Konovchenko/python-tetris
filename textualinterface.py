from time import monotonic

import tetrisplay
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header, Static, Select
from tetrisplay import check_cell_state, check_for_game_over, drop_block, move_block, check_for_filled_row, _INTERVAL

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

    grid = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="controls"):
            yield Select(((str(n), n) for n in range(4, 31)), prompt="Rows", id="rows")
            yield Select(((str(n), n) for n in range(4, 21)), prompt="Columns", id="cols")
            yield Button("Start", id="start", variant="success")
        yield Digits("00:00", id="clock")
        yield Grid(id="board")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        rows = self.query_one("#rows", Select)
        cols = self.query_one("#cols", Select)
        if rows.is_blank() or cols.is_blank():
            self.notify("Pick both a row and a column count", severity="error")
            return

        tetrisplay._ROWS = rows.value
        tetrisplay._COLUMNS = cols.value
        self.grid = tetrisplay.build_clean_grid()

        self.cells = [[Cell() for _ in range(cols.value)] for _ in range(rows.value)]
        board = self.query_one("#board")
        board.styles.grid_size_columns = cols.value
        board.styles.grid_size_rows = rows.value
        board.mount_all(cell for row in self.cells for cell in row)

        self.query_one("#controls").display = False
        self.refresh_board()
        self.start_time = monotonic()
        self.clock_timer = self.set_interval(0.1, self.update_clock)
        self.timer = self.set_interval(_INTERVAL, self.game_loop)

    def game_loop(self) -> None:
        if check_for_game_over(self.grid):
            self.timer.stop()
            self.notify("Game Over")
            return
        drop_block(self.grid)
        check_for_filled_row(self.grid)
        self.refresh_board()

    def update_clock(self) -> None:
        elapsed = monotonic() - self.start_time
        minutes, seconds = divmod(int(elapsed), 60)
        self.query_one("#clock", Digits).update(f"{minutes:02}:{seconds:02}")


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_move(self, direction:int) -> None:
        if self.grid is None:
            return
        move_block(self.grid, direction)
        self.refresh_board()

    def refresh_board(self) -> None:
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
                self.cells[row][col].colour = check_cell_state(col, row, self.grid)

def start():
    TetrisApp().run()
