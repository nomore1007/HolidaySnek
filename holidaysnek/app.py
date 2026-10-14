"""Terminal application, keyboard controls, menu and animation loop."""
from __future__ import annotations
import curses, time
from .renderer import Canvas, COLORS
from .scene_loader import discover_scenes
from .settings import load_settings, save_settings, clamp
def init_colors():
    curses.start_color()
    try: curses.use_default_colors()
    except curses.error: pass
    for color, value in COLORS.items():
        try: curses.init_pair(value + 1, value, -1)
        except curses.error: curses.init_pair(value + 1, value, curses.COLOR_BLACK)
def draw_menu(canvas, scenes, selected, settings):
    w, h = canvas.width, canvas.height
    box_w = min(max(42, w - 4), 72); box_h = min(len(scenes) + 12, max(8, h - 2))
    left, top = max(0, (w - box_w) // 2), max(0, (h - box_h) // 2)
    canvas.fill(left, top, box_w, box_h, " ", "black")
    canvas.text(left + 2, top, "+" + "-" * max(0, box_w - 4) + "+", "cyan", True)
    canvas.text(left + 2, top + 1, "HOLIDAYSNEK / SCENE SELECT", "yellow", True)
    for i, plugin in enumerate(scenes):
        y = top + 3 + i
        if y >= top + box_h - 7: break
        canvas.text(left + 2, y, (">" if i == selected else " ") + " " + plugin.name, "green" if i == selected else "white", i == selected)
    base = top + box_h - 6
    canvas.text(left + 2, base, f"Animation speed: {settings['speed']:.2f}x (- / +)", "cyan")
    canvas.text(left + 2, base + 1, f"Scene intensity: {settings['intensity']:.0%} ([ / ])", "yellow")
    canvas.text(left + 2, base + 3, "Up/Down select  Enter apply  M/Esc close  Q quit", "white")
    canvas.text(left + 2, top + box_h - 1, "+" + "-" * max(0, box_w - 4) + "+", "cyan")
def run(stdscr):
    curses.curs_set(0); stdscr.nodelay(True); stdscr.keypad(True); init_colors()
    plugins = discover_scenes()
    if not plugins:
        stdscr.addstr(0, 0, "No scenes found. Check the scenes directory."); stdscr.getch(); return
    settings = load_settings(); by_id = {p.id: p for p in plugins}
    if settings["scene"] not in by_id: settings["scene"] = plugins[0].id
    current = by_id[settings["scene"]]; scene = current.create(); menu = False
    selected = next((i for i, p in enumerate(plugins) if p.id == current.id), 0); last = time.monotonic()
    try:
        while True:
            now = time.monotonic(); dt = min(now - last, .1) * settings["speed"]; last = now
            key = stdscr.getch()
            while key != -1:
                if key in (ord("q"), ord("Q")): return
                if key in (ord("m"), ord("M"), 27): menu = not menu
                elif menu and key in (curses.KEY_UP, ord("k")): selected = (selected - 1) % len(plugins)
                elif menu and key in (curses.KEY_DOWN, ord("j")): selected = (selected + 1) % len(plugins)
                elif menu and key in (10, 13, curses.KEY_ENTER):
                    current = plugins[selected]; scene = current.create(); settings["scene"] = current.id; save_settings(settings); menu = False
                elif key in (ord("+"), ord("=")): settings["speed"] = clamp(settings["speed"] + .1, .25, 3); save_settings(settings)
                elif key == ord("-"): settings["speed"] = clamp(settings["speed"] - .1, .25, 3); save_settings(settings)
                elif key == ord("]"): settings["intensity"] = clamp(settings["intensity"] + .1, .1, 1); save_settings(settings)
                elif key == ord("["): settings["intensity"] = clamp(settings["intensity"] - .1, .1, 1); save_settings(settings)
                key = stdscr.getch()
            stdscr.erase(); canvas = Canvas(stdscr)
            try: scene.update(dt, canvas.width, canvas.height, settings["intensity"]); scene.render(canvas, canvas.width, canvas.height, settings["intensity"])
            except Exception as exc:
                canvas.text(1, 1, f"Scene error: {exc}", "red", True); canvas.text(1, 2, "Press m to choose another scene, q to quit.")
            if menu: draw_menu(canvas, plugins, selected, settings)
            else: canvas.text(1, max(0, canvas.height - 1), f" {current.name} | m menu q quit | speed {settings['speed']:.1f}x ", "white", dim=True)
            stdscr.refresh(); time.sleep(max(.01, .045 / settings["speed"]))
    finally: save_settings(settings)
def main():
    try: curses.wrapper(run)
    except KeyboardInterrupt: pass
if __name__ == "__main__": main()
