"""Script to remove dark mode and enforce light theme only (Phase A4).

1. Removes all 'dark:...' Tailwind classes from frontend/src (html, ts).
2. Removes html.dark / [data-theme="dark"] / .dark token block from styles.css.
3. Ensures <meta name="color-scheme" content="light"> in index.html.
4. Ensures :root { color-scheme: light; } in styles.css.
"""

from __future__ import annotations

import re
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent.parent
    frontend_src = repo_root / "frontend" / "src"

    # Pattern for dark: classes
    # e.g. " dark:bg-slate-900" or "'dark:bg-slate-900'"
    pattern = re.compile(r'\b(?<!-)dark:[a-zA-Z0-9_\-\/\[\]\.\%]+(?:\:[a-zA-Z0-9_\-\/\[\]\.\%]+)*')

    files = list(frontend_src.rglob("*.ts")) + list(frontend_src.rglob("*.html"))
    total_replaced = 0
    modified_files = 0

    for f in files:
        content = f.read_text(encoding="utf-8")
        matches = pattern.findall(content)
        if matches:
            total_replaced += len(matches)
            modified_files += 1
            # Replace dark classes with empty string
            new_content = pattern.sub("", content)
            # Clean up double spaces in class attributes
            new_content = re.sub(r'class="([^"]*)"', lambda m: 'class="' + " ".join(m.group(1).split()) + '"', new_content)
            new_content = re.sub(r"class='([^']*)'", lambda m: "class='" + " ".join(m.group(1).split()) + "'", new_content)
            f.write_text(new_content, encoding="utf-8")

    print(f"Removed {total_replaced} dark: classes across {modified_files} files.")

    # Update index.html
    index_html = frontend_src / "index.html"
    if index_html.exists():
        txt = index_html.read_text(encoding="utf-8")
        if 'name="color-scheme"' not in txt:
            txt = txt.replace(
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n  <meta name="color-scheme" content="light">'
            )
            index_html.write_text(txt, encoding="utf-8")
            print('Added <meta name="color-scheme" content="light"> to index.html')

    # Update styles.css
    styles_css = frontend_src / "styles.css"
    if styles_css.exists():
        txt = styles_css.read_text(encoding="utf-8")
        # Remove dark block if present
        txt = re.sub(r'/\*.*?\bINK DARK THEME.*?\*/\s*html\.dark[^{]*\{[^}]*\}', '', txt, flags=re.DOTALL)
        txt = re.sub(r'html\.dark[^{]*\{[^}]*\}', '', txt, flags=re.DOTALL)
        txt = re.sub(r':root\[data-theme="dark"\][^{]*\{[^}]*\}', '', txt, flags=re.DOTALL)
        
        # Ensure :root has color-scheme: light;
        if "color-scheme: light;" not in txt:
            txt = txt.replace(":root {", ":root {\n  color-scheme: light;")
            
        styles_css.write_text(txt, encoding="utf-8")
        print("Updated styles.css with color-scheme: light and removed dark blocks.")


if __name__ == "__main__":
    main()
