import os
from pathlib import Path

root = Path(r"c:\Users\agoda\Downloads\club-1\guide\taylor")
count_written = 0
for dirpath, dirs, files in os.walk(root):
    for f in files:
        if f.endswith('.cpp'):
            cpp = Path(dirpath) / f
            name = cpp.stem
            java = Path(dirpath) / (name + '.java')
            py = Path(dirpath) / (name + '.py')

            # read comment header from cpp (consecutive // or /* ... */ at top)
            header_lines = []
            try:
                with cpp.open('r', encoding='utf-8') as fh:
                    for line in fh:
                        s = line.rstrip('\n')
                        if s.strip().startswith('//'):
                            header_lines.append(s)
                        elif s.strip().startswith('/*'):
                            header_lines.append(s)
                            # read until */
                            for line2 in fh:
                                header_lines.append(line2.rstrip('\n'))
                                if '*/' in line2:
                                    break
                            break
                        elif s.strip() == '':
                            # skip blank
                            continue
                        else:
                            break
            except Exception:
                header_lines = []

            # prepare header text for other languages
            header_java = '\n'.join(header_lines) if header_lines else ''
            header_py = '\n'.join([l.lstrip('/').strip() if l.startswith('//') else l for l in header_lines]) if header_lines else ''
            if header_py:
                header_py = '# ' + '\n# '.join([ln.lstrip('/').strip() for ln in header_lines if ln.strip()])

            # Only write if target exists and is empty
            if java.exists() and java.stat().st_size == 0:
                content = ''
                if header_java:
                    content += header_java + '\n\n'
                content += f'public class {name} ' + '{\n'
                content += '    public static void main(String[] args) {\n'
                content += '        // Your code here\n'
                content += '    }\n'
                content += '}\n'
                with java.open('w', encoding='utf-8', newline='\n') as out:
                    out.write(content)
                count_written += 1

            if py.exists() and py.stat().st_size == 0:
                content = ''
                if header_py:
                    content += header_py + '\n\n'
                content += 'def main():\n'
                content += '    # Your code here\n'
                content += '    return\n\n'
                content += "if __name__ == '__main__':\n"
                content += '    main()\n'
                with py.open('w', encoding='utf-8', newline='\n') as out:
                    out.write(content)
                count_written += 1

print(f"Wrote/updated {count_written} files (only filled empty .java/.py siblings).")
