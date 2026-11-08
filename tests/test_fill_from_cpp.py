import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "fill_from_cpp.py"


class FillFromCppTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # The script resolves its root relative to its own location, so run a copy inside a temp tree.
        self.scripts = Path(self.tmp) / "scripts"
        self.scripts.mkdir()
        shutil.copy(SCRIPT, self.scripts / "fill_from_cpp.py")
        self.taylor = Path(self.tmp) / "guide" / "taylor"
        self.taylor.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_script(self):
        r = subprocess.run([sys.executable, "-I", str(self.scripts / "fill_from_cpp.py")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.strip()

    def make_problem(self, name, cpp_text, java="", py=""):
        d = self.taylor / name
        d.mkdir()
        (d / f"{name}.cpp").write_text(cpp_text, encoding="utf-8")
        (d / f"{name}.java").write_text(java, encoding="utf-8")
        (d / f"{name}.py").write_text(py, encoding="utf-8")
        return d

    def test_normal_fill(self):
        d = self.make_problem("AB", "// Sum two numbers\n#include <x>\nint main(){}\n")
        out = self.run_script()
        self.assertEqual(out, "Wrote/updated 2 files (only filled empty .java/.py siblings).")
        java = (d / "AB.java").read_text(encoding="utf-8")
        self.assertIn("// Sum two numbers", java)
        self.assertIn("public class AB {", java)
        py = (d / "AB.py").read_text(encoding="utf-8")
        self.assertTrue(py.startswith("# Sum two numbers"))
        self.assertIn("def main():", py)
        self.assertIn("if __name__ == '__main__':", py)

    def test_block_comment_header_is_copied(self):
        d = self.make_problem("BC", "/* Block\n header */\nint main(){}\n")
        self.run_script()
        self.assertIn("/* Block", (d / "BC.java").read_text(encoding="utf-8"))

    def test_missing_input_directory(self):
        shutil.rmtree(self.taylor)
        self.assertEqual(self.run_script(),
                         "Wrote/updated 0 files (only filled empty .java/.py siblings).")

    def test_no_match_leaves_nonempty_siblings(self):
        d = self.make_problem("NM", "int main(){}\n", java="class X {}\n", py="print(1)\n")
        out = self.run_script()
        self.assertTrue(out.startswith("Wrote/updated 0 files"))
        self.assertEqual((d / "NM.java").read_text(encoding="utf-8"), "class X {}\n")
        self.assertEqual((d / "NM.py").read_text(encoding="utf-8"), "print(1)\n")

    def test_missing_sibling_is_not_created(self):
        d = self.make_problem("MS", "int main(){}\n")
        (d / "MS.java").unlink()
        (d / "MS.py").unlink()
        self.assertTrue(self.run_script().startswith("Wrote/updated 0 files"))
        self.assertFalse((d / "MS.java").exists())
        self.assertFalse((d / "MS.py").exists())

    def test_idempotent_rerun(self):
        d = self.make_problem("ID", "// hi\nint main(){}\n")
        self.run_script()
        java1 = (d / "ID.java").read_text(encoding="utf-8")
        py1 = (d / "ID.py").read_text(encoding="utf-8")
        out = self.run_script()
        self.assertTrue(out.startswith("Wrote/updated 0 files"))
        self.assertEqual((d / "ID.java").read_text(encoding="utf-8"), java1)
        self.assertEqual((d / "ID.py").read_text(encoding="utf-8"), py1)


if __name__ == "__main__":
    unittest.main()
