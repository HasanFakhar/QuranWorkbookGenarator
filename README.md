# Quran Surah HTML Generator

A Streamlit application that fetches Quranic Arabic text from the Al Quran Cloud API and generates a print-friendly HTML page for any Surah.

## Features

- Select any of the 114 Surahs.
- Uses the `quran-uthmani-quran-academy` edition from Al Quran Cloud.
- Four ruled writing lines between Ayahs by default.
- Adjustable number of lines, Arabic font size, and line spacing.
- RTL Arabic layout.
- A4 print styling.
- Preview the generated page inside Streamlit.
- Download the generated HTML file.

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```powershell
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## API

The app uses:

`https://api.alquran.cloud/v1/surah/{surah_number}/quran-uthmani-quran-academy`

The API is public and does not require an API key.

## Notes

The generated HTML uses the Amiri font from Google Fonts when internet access is available. It also includes Arabic font fallbacks so the page remains readable if the web font cannot be loaded.

The HTML is designed for A4 portrait printing. Use the browser's Print dialog and select A4 if needed.
