import os
import re
import unittest

JS = os.path.join(os.path.dirname(__file__), "..", "scripts", "logo-particles.js")


class LogoParticlesColorTest(unittest.TestCase):
    def test_color_index_stays_within_colors_array(self):
        with open(JS, encoding="utf-8") as f:
            src = f.read()
        # colors has 2 entries; picking from a hardcoded 6 yields undefined colors
        m = re.search(r"this\.color\s*=\s*colors\[(.+?)\];", src)
        self.assertIsNotNone(m, "color assignment not found")
        self.assertIn("colors.length", m.group(1))


if __name__ == "__main__":
    unittest.main()
