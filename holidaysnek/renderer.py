"""Safe curses drawing helpers shared by scenes."""
import curses
COLORS = {"black": curses.COLOR_BLACK, "red": curses.COLOR_RED, "green": curses.COLOR_GREEN, "yellow": curses.COLOR_YELLOW, "blue": curses.COLOR_BLUE, "magenta": curses.COLOR_MAGENTA, "cyan": curses.COLOR_CYAN, "white": curses.COLOR_WHITE}
class Canvas:
    def __init__(self, window): self.window = window; self.height, self.width = window.getmaxyx()
    def text(self, x, y, value, color="white", bold=False, dim=False):
        if y < 0 or y >= self.height or self.width < 2: return
        value = str(value); x = int(x); y = int(y)
        if x >= self.width or x + len(value) <= 0: return
        if x < 0: value = value[-x:]; x = 0
        value = value[:max(0, self.width - x - 1)]
        attr = curses.color_pair(COLORS.get(color, curses.COLOR_WHITE) + 1)
        if bold: attr |= curses.A_BOLD
        if dim: attr |= curses.A_DIM
        try: self.window.addnstr(y, x, value, max(0, self.width - x - 1), attr)
        except curses.error: pass
    def fill(self, x, y, width, height, char=" ", color="white"):
        for yy in range(max(0, y), min(self.height, y + height)): self.text(x, yy, char * max(0, width), color)
