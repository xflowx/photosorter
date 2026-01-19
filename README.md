please note: This project was fully made with AI, as a prove of concept


# 📸 Photo Sorter

A fast, fullscreen, keyboard‑driven tool for efficiently sorting large numbers of photographs into multiple directories while viewing them in a slideshow.

`photo_sorter` is designed for photographers and power users who want to triage, curate, and organize photos **without breaking flow**—using only the keyboard.

> **Scope of this README**: This describes the version with **config file support** and **Send‑to‑Trash**. It does **not** include experimental letter‑key targets/actions.

---

## ✨ Features

- 🖥️ **Fullscreen slideshow** with smooth, high‑quality scaling (LANCZOS)
- ⌨️ **Keyboard navigation** (forward/back)
- 📁 **Move or copy** photos into configurable target directories
- 🔢 Up to **36 target folders**, mapped to number keys (`1–9`) and letters
- 🗑️ **Send photos to Trash / Recycle Bin** (safe, reversible)
- ↩️ **Undo** for move/copy (and guidance for trash undo)
- 💾 **Persistent config file** (YAML or JSON)
- 🔁 Optional recursive folder scanning and shuffle mode
- 🧭 Auto‑advance after actions (configurable)
- 🖼️ Automatic **EXIF orientation correction**
- 📷 Supports common formats (`JPG`, `JPEG`, `PNG`, `GIF`, `BMP`, `TIFF`, `WEBP`) and optional **HEIC/HEIF**

---

## 📷 Typical Workflow

1. Start the app and point it to your **Unsorted** folder (via config).
2. View each image **fullscreen**.
3. Press a **number key (1–9)** or **letter key (a-z)** to **move/copy** the image to a mapped folder.
4. Press **`0`** to **send to Trash** (if enabled in config).
5. The app **auto‑advances** to the next image.
6. Made a mistake? Press **`U`** to undo the last action.

---

## 🧩 Installation

### Requirements

- Python **3.8+**
- **Pillow** (image decoding)
- **send2trash** (safe, reversible trash)
- *(Optional)* **pillow‑heif** (HEIC/HEIF support)

```bash
pip install pillow send2trash
# optional for HEIC/HEIF
pip install pillow-heif
```

> On some Linux distros, you may also need system packages for Tk (e.g., `sudo apt install python3-tk`).

---

## ▶️ Running

Save the script as `photo_sorter.py`, then:

```bash
python photo_sorter.py
```

On first run, the app creates an example config file (YAML if `pyyaml` is installed, otherwise JSON) at the default location.

### Use a custom config path

```bash
python photo_sorter.py --config /path/to/config.yaml
```

---

## ⚙️ Configuration

The tool reads a YAML or JSON config file.

### Default locations

- **Linux / macOS**: `~/.config/photo_sorter/config.yaml`
- **Windows**: `%APPDATA%/photo_sorter/config.yaml`

> If the file does not exist, an example config is created automatically.

### Example `config.yaml`

```yaml
source: "/home/user/Pictures/Inbox"
recursive: true
shuffle: true
mode: move        # move | copy

# Optional UI tweaks
background: "#000000"

# File extensions to include (lowercase, without dots)
extensions:
  - jpg
  - jpeg
  - png
  - gif
  - bmp
  - tif
  - tiff
  - webp
  - heic  # requires pillow-heif

# Map number keys 1..9 to target directories
# Each value is a string path. (No per-target mode here; uses global mode.)
# Example uses Linux paths; adapt for macOS/Windows.
targets:
  "1": "/home/user/Pictures/Keepers"
  "2": "/home/user/Pictures/Family"
  "3": "/home/user/Pictures/To_Edit"

# Send-to-Trash configuration
trash:
  enabled: true
  key: "0"         # press 0 to send to Trash
```

### CLI vs Config precedence

- **CLI flags** (if/when provided) override **config** values.
- If `--config` is provided, that path is used; otherwise the default path is used.

---

## ⌨️ Keyboard Shortcuts

### Navigation & display

- **Right / Down / Space / N** → Next photo
- **Left / Up / P** → Previous photo
- **F** → Toggle fullscreen
- **I** → Toggle info overlay (index, mode, filename)
- **H** → Toggle help overlay (key bindings & mapped targets)

### Sorting actions

- **1–9** **a-z** → Move/Copy current photo to the mapped target directory
- **0** → Send to **Trash** (if enabled in config)
- **U** → **Undo** last action

### App

- **Esc / Q** → Quit

---

## 🔄 Undo Behavior

- **Move** → The file is moved back to its original folder.
- **Copy** → The copied file is deleted.
- **Trash** → Due to system Trash APIs, restoration must be done **manually** from your OS Trash/Recycle Bin. The app records the last action, but cannot auto‑restore from Trash.

---

## 📁 Behavior Details

- **Collision‑safe names**: If a destination already has the filename, the app appends `-1`, `-2`, … to avoid overwrites.
- **Ordering**: If `shuffle` is **true**, files are randomized at startup; otherwise they are listed by name.
- **Recursive scan**: When `recursive` is **true**, all matching files in subdirectories are included.
- **EXIF orientation**: Images are auto‑rotated according to EXIF.
- **Formats**: By default handles `jpg, jpeg, png, gif, bmp, tif, tiff, webp`; HEIC/HEIF supported when `pillow‑heif` is installed.

---

## 🛠️ Packaging (Optional)

Create a single-file executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller -F -w photo_sorter.py
```

- `-F` creates one executable
- `-w` hides the console window (Windows/macOS)

---

## 🧪 Troubleshooting

- **Tkinter missing**: Install your OS package (e.g., Ubuntu/Debian: `sudo apt install python3-tk`).
- **HEIC files won’t open**: Install `pillow-heif` (`pip install pillow-heif`).
- **No images found**: Check `extensions`, `source`, and whether `recursive` is required.
- **Undo from Trash**: Use your OS Trash/Recycle Bin to restore; the app cannot programmatically restore trashed files.

---

## 🤝 Contributing

Issues and PRs are welcome! Please describe your environment (OS, Python version), steps to reproduce, and include logs if available.

---

## 📝 License

MIT License — do what you want, but please leave the attribution and license in place.

---

## 🙏 Acknowledgments

- Built with **Pillow** for image handling
- Uses **send2trash** for safe Trash/Recycle Bin support
- Thanks to the open‑source community for inspiration and testing

