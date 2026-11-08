import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
JS = os.path.join(ROOT, "scripts", "logo-particles.js")
GEN = os.path.join(ROOT, "guide", "taylor", "init_folders.py")


class LogoImgDeclaredTest(unittest.TestCase):
    def test_img_is_declared_locally(self):
        with open(JS, encoding="utf-8") as f:
            src = f.read()
        # any bare assignment to img (not preceded by let/const/var) leaks a global
        self.assertIsNone(re.search(r"(?<!const )(?<!let )(?<!var )(?<![\w.])img\s*=(?!=)", src),
                          "img assigned without a local declaration")


class InitFoldersNoOverwriteTest(unittest.TestCase):
    def test_existing_student_files_are_not_overwritten(self):
        tmp = tempfile.mkdtemp()
        try:
            gen = os.path.join(tmp, "init_folders.py")
            shutil.copy(GEN, gen)
            target = os.path.join(tmp, "VPC", "VPC.py")
            os.makedirs(os.path.dirname(target))
            with open(target, "w", encoding="utf-8") as f:
                f.write("print('student work')\n")
            subprocess.run([sys.executable, "-I", gen], check=True, cwd=tmp,
                           capture_output=True)
            with open(target, encoding="utf-8") as f:
                self.assertEqual(f.read(), "print('student work')\n")
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
