import unittest
from holidaysnek.scene_loader import discover_scenes

class FakeCanvas:
    def __init__(self): self.calls = 0
    def text(self, *args, **kwargs): self.calls += 1
    def fill(self, *args, **kwargs): self.calls += 1

class SceneTests(unittest.TestCase):
    def test_all_seven_builtin_scenes_discover(self):
        scenes = discover_scenes()
        self.assertEqual(len(scenes), 7)
        self.assertEqual(len({scene.id for scene in scenes}), 7)

    def test_every_scene_can_render_at_typical_terminal_size(self):
        for plugin in discover_scenes():
            with self.subTest(scene=plugin.id):
                scene = plugin.create()
                canvas = FakeCanvas()
                scene.update(0.04, 100, 30, 0.7)
                scene.render(canvas, 100, 30, 0.7)
                self.assertGreater(canvas.calls, 0)

if __name__ == "__main__":
    unittest.main()
