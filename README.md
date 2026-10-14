# HolidaySnek 🎃

Animated seasonal scenes for modern Linux terminals. HolidaySnek is a tiny, dependency-free Python terminal screensaver with flickering fires, falling snow, spooky skies, autumn leaves, and cozy rooms.

## Features

- Seven built-in scenes: Halloween, Thanksgiving, Christmas Village, Winter Cabin, Christmas Living Room, Winter Fireplace, and Christmas Fireplace.
- Two immersive terminal-filling fireplaces with animated flames, logs, sparks, and snowfall. The Christmas version adds garland, colored lights, stockings, and ornaments.
- Press **m** to open the scene menu. Use **Up/Down** (or **j/k**) and **Enter** to switch scenes.
- **+/-** adjusts animation speed. **[/]** adjusts scene intensity. **Esc** or **m** closes the menu. **q** quits.
- Remembers your last scene, speed, and intensity.
- Plugins are discovered from folders. No editing the core app to add scenes.
- Python 3.11+ and no third-party runtime dependencies.

## Run it

```bash
python3 -m holidaysnek
```

Install as a user command:

```bash
python3 -m pip install --user .
holidaysnek
```

Use a modern terminal with 256-color support for the best results. The app also works in ordinary color terminals. Resize the terminal at any time.

## Add a scene

Create a folder containing `scene.toml` and `scene.py` under `scenes/`:

```text
scenes/
  my-scene/
    scene.toml
    scene.py
```

Example `scene.toml`:

```toml
id = "my-scene"
name = "My Scene"
description = "A short description shown to users."
```

Example `scene.py`:

```python
class Scene:
    def update(self, dt, width, height, intensity):
        pass

    def render(self, canvas, width, height, intensity):
        canvas.text(2, 2, "Hello from my scene!", "green", bold=True)
```

The loader imports each plugin independently and skips invalid scenes rather than preventing the application from starting. Scene IDs must be unique. Third-party plugins are Python code and should only be installed from sources you trust.

For external scene collections, set `HOLIDAYSNEK_SCENES` to one or more directories separated by your platform's path separator (`:` on Linux). Built-in scenes load first; duplicate IDs are ignored.

## Settings

Settings are saved to `$XDG_CONFIG_HOME/holidaysnek/config.json`, or `~/.config/holidaysnek/config.json` when `XDG_CONFIG_HOME` is unset.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Licensed under the MIT License. See [LICENSE](LICENSE).
