
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo Sorter with:
- Fullscreen slideshow
- Keyboard-based move/copy
- Persistent config file (YAML / JSON)
- Send to Trash (Recycle Bin / macOS Trash / Linux Trash)
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk, ImageOps
from send2trash import send2trash

# Optional HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

# ---------------- CONFIG HANDLING ----------------

def default_config_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home() / ".config"
    return base / "photo_sorter" / "config.yaml"


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    if path.suffix.lower() in (".yaml", ".yml"):
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_example_config(path: Path):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    example = {
        "source": "/path/to/photos",
        "recursive": True,
        "shuffle": False,
        "mode": "move",
        "targets": {
            "1": "/path/to/keep",
            "2": "/path/to/family",
        },
        "trash": {
            "enabled": True,
            "key": "0"
        }
    }
    try:
        import yaml
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(example, f)
    except ImportError:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(example, f, indent=2)

# ---------------- FILE OPS ----------------

def safe_move(src: Path, dst_dir: Path) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    i = 1
    while dst.exists():
        dst = dst_dir / f"{src.stem}-{i}{src.suffix}"
        i += 1
    shutil.move(src, dst)
    return dst


def safe_copy(src: Path, dst_dir: Path) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    i = 1
    while dst.exists():
        dst = dst_dir / f"{src.stem}-{i}{src.suffix}"
        i += 1
    shutil.copy2(src, dst)
    return dst

# ---------------- MAIN APP ----------------

class App:
    def __init__(self, root, files, targets, tr_enabled, tr_key, move_mode):
        self.root = root
        self.files = files
        self.index = 0
        self.targets = targets
        self.move_mode = move_mode
        self.tr_enabled = tr_enabled
        self.tr_key = tr_key

        self.undo_stack = []

        root.attributes("-fullscreen", True)
        root.configure(bg="black")

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        root.bind("<Right>", lambda e: self.next())
        root.bind("<Left>", lambda e: self.prev())
        root.bind("<Escape>", lambda e: root.quit())

        for k in targets:
            root.bind(str(k), lambda e, n=k: self.use_target(n))

        if tr_enabled:
            root.bind(tr_key, lambda e: self.trash())

        root.bind("u", lambda e: self.undo())

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if not self.files:
            return
        img = Image.open(self.files[self.index])
        img = ImageOps.exif_transpose(img)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        img.thumbnail((sw, sh), Image.Resampling.LANCZOS)

        self.tkimg = ImageTk.PhotoImage(img)
        self.canvas.create_image(
            sw // 4, sh // 2, image=self.tkimg, anchor="center"
        )

    def next(self):
        self.index = (self.index + 1) % len(self.files)
        self.draw()

    def prev(self):
        self.index = (self.index - 1) % len(self.files)
        self.draw()

    def use_target(self, k):
        src = self.files[self.index]
        dst_dir = Path(self.targets[k])
        if self.move_mode:
            dst = safe_move(src, dst_dir)
            self.files[self.index] = dst
            self.undo_stack.append(("move", dst, src))
        else:
            dst = safe_copy(src, dst_dir)
            self.undo_stack.append(("copy", dst))
        self.next()

    def trash(self):
        src = self.files[self.index]
        send2trash(str(src))
        self.undo_stack.append(("trash", src))
        self.next()

    def undo(self):
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        if action[0] == "trash":
            messagebox.showinfo("Undo", "Restore from Trash manually.")
        elif action[0] == "move":
            shutil.move(action[1], action[2])
            self.files[self.index] = action[2]
        elif action[0] == "copy":
            Path(action[1]).unlink(missing_ok=True)
        self.draw()

# ---------------- ENTRY POINT ----------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()

    cfg_path = args.config or default_config_path()
    ensure_example_config(cfg_path)
    cfg = load_config(cfg_path)

    source = Path(cfg.get("source", "."))
    files = list(source.glob("*.jpg")) + list(source.glob("*.png"))
    
    shuffle_cfg = cfg.get("shuffle")
    if not shuffle_cfg: 
        files.sort()
    
    targets = {k: v for k, v in cfg.get("targets", {}).items()}
    trash_cfg = cfg.get("trash", {})
    tr_enabled = trash_cfg.get("enabled", False)
    tr_key = trash_cfg.get("key", "0")
    move_mode = cfg.get("mode", "move") == "move"

    root = tk.Tk()
    App(root, files, targets, tr_enabled, tr_key, move_mode)
    root.mainloop()

if __name__ == "__main__":
    main()

