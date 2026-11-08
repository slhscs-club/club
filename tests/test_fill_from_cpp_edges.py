import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "fill_from_cpp.py"


class FillFromCppEdgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.scripts = Path(self.tmp) / "scripts"
        self.scripts.mkdir()
        shutil.copy(SCRIPT, self.scripts / "fill_from_cpp.py")
        self.taylor = Path(self.tmp) / "guide" / "taylor"
        self.taylor.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_script(self):
        r = subprocess.run([sys.executable, "-I", str(self.scripts / "fill_from_cpp.py")],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.strip()

    def make_problem(self, name, cpp_bytes, java="", py="", parent=None):
        d = (parent or self.taylor) / name
        d.mkdir(parents=True)
        (d / f"{name}.cpp").write_bytes(cpp_bytes)
        (d / f"{name}.java").write_text(java, encoding="utf-8")
        (d / f"{name}.py").write_text(py, encoding="utf-8")
        return d

    def test_non_ascii_header_is_preserved(self):
        d = self.make_problem("NA", "// Café – données ✓\nint main(){}\n".encode("utf-8"))
        self.assertTrue(self.run_script().startswith("Wrote/updated 2 files"))
        self.assertIn("// Café – données ✓", (d / "NA.java").read_text(encoding="utf-8"))
        self.assertTrue((d / "NA.py").read_text(encoding="utf-8").startswith("# Café – données ✓\n"))

    def test_one_line_block_comment_does_not_swallow_code(self):
        d = self.make_problem("OL", b"/* One line */\nint main(){}\n")
        self.run_script()
        java = (d / "OL.java").read_text(encoding="utf-8")
        self.assertIn("/* One line */", java)
        self.assertNotIn("int main", java)

    def test_multi_line_block_comment_is_kept_whole(self):
        d = self.make_problem("ML", b"/* One\n two */\nint main(){}\n")
        self.run_script()
        java = (d / "ML.java").read_text(encoding="utf-8")
        self.assertIn(" two */", java)
        self.assertNotIn("int main", java)

    def test_crlf_cpp_produces_lf_output(self):
        d = self.make_problem("CR", b"// Sum two\r\n#include <x>\r\nint main(){}\r\n")
        self.run_script()
        java = (d / "CR.java").read_bytes()
        py = (d / "CR.py").read_bytes()
        self.assertNotIn(b"\r", java)
        self.assertNotIn(b"\r", py)
        self.assertTrue(java.startswith(b"// Sum two\n"))
        self.assertTrue(py.startswith(b"# Sum two\n"))

    def test_empty_cpp_fills_stub_without_header(self):
        d = self.make_problem("EC", b"")
        self.assertTrue(self.run_script().startswith("Wrote/updated 2 files"))
        self.assertTrue((d / "EC.java").read_text(encoding="utf-8").startswith("public class EC {"))
        self.assertTrue((d / "EC.py").read_text(encoding="utf-8").startswith("def main():"))

    def test_only_one_sibling_present_is_filled(self):
        d = self.make_problem("OS", b"// one\nint main(){}\n")
        (d / "OS.java").unlink()
        self.assertTrue(self.run_script().startswith("Wrote/updated 1 files"))
        self.assertFalse((d / "OS.java").exists())
        self.assertIn("def main():", (d / "OS.py").read_text(encoding="utf-8"))

    def test_nested_subdirectories_are_processed(self):
        group = self.taylor / "group"
        d = self.make_problem("NS", b"// deep\nint main(){}\n", parent=group)
        self.assertTrue(self.run_script().startswith("Wrote/updated 2 files"))
        self.assertIn("public class NS {", (d / "NS.java").read_text(encoding="utf-8"))

    def test_non_cpp_files_are_ignored(self):
        d = self.taylor / "NC"
        d.mkdir()
        (d / "NC.h").write_text("// header\n", encoding="utf-8")
        (d / "NC.java").write_text("", encoding="utf-8")
        (d / "NC.py").write_text("", encoding="utf-8")
        self.assertTrue(self.run_script().startswith("Wrote/updated 0 files"))
        self.assertEqual((d / "NC.java").read_text(encoding="utf-8"), "")
        self.assertEqual((d / "NC.py").read_text(encoding="utf-8"), "")


if __name__ == "__main__":
    unittest.main()
