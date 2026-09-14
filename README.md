# CollectUtilities v3 (Nuke Plugin)  

A small toolkit of Nuke (VFX compositing software) utility scripts for managing **Read** node footage: checking for missing frames, collecting/copying files used in a script, renaming sequences, and moving files into organized folders — all from a menu inside Nuke.

- **Original Author:** Miguel Torija ([migueltorija.com](http://migueltorija.com))
- **Python fixes / menu integration / updates:** Nitin Kashyap
- **Release date:** Jan 21, 2026
- **Host application:** Autodesk / Foundry **Nuke** (tested with PySide2, with PySide6 fallback)

<img src="https://github.com/Nitinkashyap96/CollectUtilities_v3/blob/main/icon_mtCollectUtilities_v03.png?raw=true" alt="Collect Utilities Icon" width="54" />

---

## ✨ Features

This adds a **Collect Utilities** menu under Nuke's `Nodes` menu with 5 tools:

| Tool | Script | What it does |
|---|---|---|
| **Check Frames** | `mtCheckFrames.py` | Scans a selected Read node's file sequence and reports missing frames within the project or a custom frame range. |
| **Files To Folder** | `mtFilesToFolder_v03.py` | Copies files referenced by selected Read / DeepRead / ReadGeo2 nodes into a target folder. |
| **File Renamer** | `mtFileRenamer_v03_1.py` | Batch-renames a selected Read node's image sequence on disk and repoints the node to the new name. |
| **Collect Files** | `mtCollectFiles_v03.py` | Collects all footage/dependencies used by the current script into one destination (with a confirmation/advisory dialog). |
| **Get Frames** | `mtGetFrames.py` | Reads frame-range/format/colorspace info from a selected Read node. |

Each UI-based tool (`Files To Folder`, `File Renamer`, `Collect Files`) is built from a `.ui` file (Qt Designer) loaded at runtime via `PySide2`/`PySide6`.

---

## 🧰 Requirements

- **Nuke** 12+ (uses `nuke`, `nukescripts` Python modules)
- **Python** 3.10/3.11 (compiled `.pyc` cache included for both — matches modern Nuke's embedded Python 3)
- **PySide2** (primary) or **PySide6** (fallback, used automatically in `mtCollectFiles_v03.py` if PySide2 isn't available)
- **psutil** Python package (used by `mtCollectFiles_v03.py` and `mtFileRenamer_v03_1.py`)

Install `psutil` into Nuke's Python environment if it isn't already available:

```bash
"C:\Program Files\Nuke15.x\python.exe" -m pip install psutil
```

(Adjust the path to match your installed Nuke version.)

---

## 📁 Package Contents

```
CollectUtilities_v3/
├── init.py                              # Adds plugin paths to Nuke
├── menu.py                              # Builds the "Collect Utilities" Nodes menu
├── icon_mtCollectUtilities_v03.png      # Menu icon
├── CollectUtilities.png                 # Tool banner/preview image
└── CollectUtilities_v03_scripts/
    ├── mtCheckFrames.py
    ├── mtCollectFiles_v03.py
    ├── mtFilesToFolder_v03.py
    ├── mtFileRenamer_v03_1.py
    ├── mtGetFrames.py
    └── ui/
        ├── mtCollectFiles_v002.ui
        ├── mtCollectFiles_advise_v001.ui
        ├── mtFileRenamer_v001.ui
        └── mtFilesToFolder_v001.ui
```

---

## 🚀 Installation — Step by Step

1. **Locate your Nuke user directory.**
   This is the `.nuke` folder in your home directory:
   - Windows: `C:\Users\<YourUser>\.nuke`
   - macOS: `~/.nuke`
   - Linux: `~/.nuke`

2. **Copy the tool folder in.**
   Copy the entire `CollectUtilities_v3` folder (as extracted from the zip) directly into your `.nuke` folder, so the path looks like:
   ```
   ~/.nuke/CollectUtilities_v3/
   ```

3. **Register the plugin path.**
   Open (or create) `~/.nuke/menu.py` and add):
   ```python
   nuke.pluginAddPath("./CollectUtilities_v3")
   ```
   > If `menu.py` already exists with other tools, just make sure Nuke's plugin path search includes the `CollectUtilities_v3` folder (step 3 handles this) — Nuke will automatically execute any `menu.py` found on the plugin path at startup.

5. **Install the Python dependency.**
   Make sure `psutil` is installed in Nuke's Python (see [Requirements](#-requirements) above).

6. **Restart Nuke.**
   On launch you should see a console message similar to:
   ```
   CollectUtilities v1.0.0, build 20 Jan 2026.
   Copyright (C) 2025 by Nitin Kashyap, All rights reserved.
   ```

7. **Access the tools.**
   Go to the Node Graph → right-click (or top menu) → **Nodes → Collect Utilities**, where you'll find all five commands listed.

---

## 🖱️ Usage

- **Check Frames:** Select a `Read` node → `Nodes → Collect Utilities → Check Frames` → choose a frame range source (Read / Project / Custom) → run to see a report of missing frames.
- **Get Frames:** Select a single `Read` node → `Nodes → Collect Utilities → Get Frames` → specify `All` or a custom comma-separated frame list → optionally enable auto-ordering.
- **Files To Folder:** Select one or more `Read` / `DeepRead` / `ReadGeo2` nodes → `Nodes → Collect Utilities → Files To Folder` → the dialog auto-fills the selected node names → choose a destination and run.
- **File Renamer:** Select a single `Read` node → `Nodes → Collect Utilities → File Renamer` → enter the new name in the dialog → confirm to rename the file(s) and update the node.
- **Collect Files:** With no selection needed → `Nodes → Collect Utilities → Collect Files` → the dialog pre-fills a destination folder and script name based on your current project → run to gather every referenced media file plus a saved copy of the script into one packaged folder.

---

## ⚠️ Notes

- Paths in the scripts are read relative to the current Nuke project root (`nuke.root()['name']`), so save your script before running these tools for the best results.
- `mtFilesToFolder_v03.py` and `mtFileRenamer_v03_1.py` import `PySide2` directly; if your Nuke build only ships PySide6, you may need to adjust those imports the same way `mtCollectFiles_v03.py` does (try/except fallback).
- A `__pycache__` folder is included from development/testing and can be safely deleted — Nuke will regenerate it.

---

## 📝 License

```
Copyright (C) 2025 by Nitin Kashyap. All rights reserved.
```
Original tool created by **Miguel Torija** (Digital Compositor), with Python fixes, debugging, and menu integration by **Nitin Kashyap**.

---

## 🙏 Credits

- **Miguel Torija** — original author, [migueltorija.com](https://migueltorija.com)
- **Nitin Kashyap** — Python fixes/debugging, menu.py integration, tool updates
