"""Haunted graveyard scene with drifting bats and occasional spirits."""
import math
import random

from holidaysnek.effects import BaseScene


class Scene(BaseScene):
    def __init__(self):
        super().__init__()
        self._ghosts = []
        self._ghost_timer = self.rng.uniform(8.0, 15.0)
        self._last_size = (0, 0)

    def update(self, dt, width, height, intensity):
        super().update(dt, width, height, intensity)
        self._last_size = (width, height)
        self._ghost_timer -= dt
        if self._ghost_timer <= 0 and width > 24 and height > 10:
            # A rare visitor crosses the scene instead of popping in every loop.
            from_left = self.rng.choice([True, False])
            sprite = self.rng.choice(["ghost", "ghoul"])
            y = self.rng.randint(max(3, height // 3), max(3, height * 2 // 3))
            speed = self.rng.uniform(3.0, 6.5) * max(0.65, intensity)
            x = -7 if from_left else width + 2
            self._ghosts.append({
                "x": float(x), "y": y, "speed": speed,
                "direction": 1 if from_left else -1,
                "sprite": sprite,
                "phase": self.rng.uniform(0, math.tau),
            })
            self._ghost_timer = self.rng.uniform(18.0, 34.0) / max(0.7, intensity)
        survivors = []
        for ghost in self._ghosts:
            ghost["x"] += ghost["speed"] * ghost["direction"] * dt
            if -12 < ghost["x"] < width + 10:
                survivors.append(ghost)
        self._ghosts = survivors

    def render(self, c, w, h, intensity):
        if w < 24 or h < 10:
            c.text(0, 0, "Enlarge terminal to enter the graveyard...", "magenta", True)
            return

        # Deep night sky, distant stars, and a moon peeking through clouds.
        for y in range(1, max(2, h // 2), 2):
            for x in range((y * 11 + int(self.t * 2)) % 13, w, 13):
                c.text(x, y, "." if (x + y) % 3 else "*", "blue", dim=True)
        moon_x, moon_y = max(2, w - 13), max(2, h // 7)
        c.text(moon_x, moon_y, " .-.", "white", True)
        c.text(moon_x, moon_y + 1, "(   )", "white", True)
        c.text(moon_x, moon_y + 2, " '-'", "white", True)
        # A moving veil of cloud occasionally crosses the moon.
        cloud_x = int((self.t * 2.2) % (w + 18)) - 18
        if moon_y + 3 < h:
            c.text(cloud_x, moon_y + 3, "~~~  ~~~", "blue", dim=True)

        c.text(max(0, (w - 14) // 2), 2, "HALLOWEEN NIGHT", "magenta", True)
        c.text(max(0, (w - 25) // 2), 4, "The graveyard is stirring...", "white", dim=True)

        # Bare, twisted trees frame the scene. The branch angles shift subtly in the wind.
        sway = int(math.sin(self.t * 0.7) * 1.5)
        self._draw_tree(c, 3, h - 5, max(7, h // 2), sway, flip=False)
        self._draw_tree(c, w - 5, h - 5, max(6, h // 2 - 1), -sway, flip=True)
        if w > 70:
            self._draw_tree(c, w // 4, h - 5, max(5, h // 3), -sway, flip=False, dim=True)
            self._draw_tree(c, w * 3 // 4, h - 5, max(5, h // 3), sway, flip=True, dim=True)

        # Windblown ground mist.
        ground_y = h - 5
        for band in range(2):
            y = ground_y - 1 - band * 2
            if y > 5:
                offset = int(self.t * (2.0 + band) * (1 if band == 0 else -1))
                for x in range((offset % 11) - 11, w, 11):
                    c.text(x, y, "~~~~", "cyan", dim=True)

        # Bats flap across the sky on independent paths.
        bat_count = max(3, int(w * 0.075 * intensity))
        for i in range(bat_count):
            x = int((i * 19 + self.t * (3.0 + i % 3 * 1.7)) % max(1, w))
            y = max(1, int(h * 0.16 + math.sin(self.t * 2.1 + i * 1.7) * (1.5 + i % 3)))
            wings = "/v\\" if int(self.t * 8 + i) % 2 else "\\v/"
            c.text(x, y, wings, "white" if i % 4 == 0 else "magenta", True)

        # Gravestones in several sizes create a layered, uneven silhouette.
        grave_count = max(4, int(w / 11))
        for i in range(grave_count):
            x = 2 + int(i * (w - 8) / max(1, grave_count - 1))
            stone_h = 2 + (i * 7 % 3)
            y = ground_y - stone_h
            if i % 3 == 0:
                shape = [" .--. ", "|    |", "| +  |", "|____|"]
            elif i % 3 == 1:
                shape = [" .--.", "|    |", "| xx |", "|____|"]
            else:
                shape = [" .--. ", "| RIP |", "|____|"]
            for row, line in enumerate(shape[:stone_h + 1]):
                c.text(x - len(line) // 2, y + row, line, "white" if i % 2 else "cyan", dim=True)
            c.text(x - 3, ground_y + 1, "._._.", "blue", dim=True)

        # A jack-o-lantern flickers near the path.
        pumpkin_x = max(1, min(w - 12, w // 2 - 5))
        pumpkin_y = max(6, ground_y - 4)
        glow = int(self.t * 5) % 4 != 0
        c.text(pumpkin_x, pumpkin_y, " .------. ", "yellow", True)
        c.text(pumpkin_x, pumpkin_y + 1, " /      \\", "yellow", True)
        c.text(pumpkin_x, pumpkin_y + 2, "|  %s  |" % ("^  ^" if glow else ".  ."), "yellow", True)
        c.text(pumpkin_x, pumpkin_y + 3, "|   \\/   |", "yellow", True)
        c.text(pumpkin_x, pumpkin_y + 4, " '------' ", "red", True)

        # Spirits are rare events: they drift through and vanish off-screen.
        for ghost in self._ghosts:
            gx, gy = int(ghost["x"]), ghost["y"]
            if ghost["sprite"] == "ghost":
                sprite = [".-.", "(o o)", "/|_|\\"]
                color = "white"
            else:
                sprite = [" .-.", "{x x}", " /V\\"]
                color = "cyan"
            for row, line in enumerate(sprite):
                c.text(gx, gy + row, line, color, True)

    def _draw_tree(self, c, x, base_y, height, sway, flip=False, dim=False):
        """Draw a crooked, leafless tree using terminal-safe ASCII branches."""
        trunk_color = "blue" if dim else "white"
        branch_color = "blue" if dim else "magenta"
        top = max(5, base_y - height)
        trunk_x = x + sway
        for y in range(top, base_y):
            offset = int(math.sin(y * 0.9 + self.t * 0.5) * 1.2)
            tx = trunk_x + offset
            c.text(tx, y, "Y" if y == top else "|" if y < base_y - 2 else "}", trunk_color, True, dim=dim)
            level = y - top
            if level in (1, 3, height // 2, height // 2 + 2):
                direction = -1 if (level % 2 == 1) else 1
                if flip:
                    direction *= -1
                branch = "\\---" if direction < 0 else "---/"
                c.text(tx - 4 if direction < 0 else tx + 1, y, branch, branch_color, dim=dim)
                if level in (3, height // 2 + 2):
                    c.text(tx - 6 if direction < 0 else tx + 4, y - 1, "/\\", branch_color, dim=dim)
