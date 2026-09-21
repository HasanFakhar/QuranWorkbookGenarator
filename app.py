import html
import requests
import streamlit as st
import streamlit.components.v1 as components

API_BASE = "https://api.alquran.cloud/v1"
EDITION = "quran-uthmani-quran-academy"

st.set_page_config(
    page_title="Quran Surah HTML Generator",
    page_icon="📖",
    layout="wide",
)

st.title("📖 Quran Surah HTML Generator")
st.caption(
    "Fetch any Surah from Al Quran Cloud and generate a print-friendly HTML page "
    "with four ruled writing lines between each Ayah."
)

@st.cache_data(ttl=3600)
def get_surah_list():
    response = requests.get(f"{API_BASE}/surah", timeout=20)
    response.raise_for_status()
    payload = response.json()
    return payload["data"]

@st.cache_data(ttl=3600)
def get_surah(surah_number):
    url = f"{API_BASE}/surah/{surah_number}/{EDITION}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if payload.get("code") != 200:
        raise RuntimeError(payload.get("status", "API request failed"))
    return payload["data"]

def build_html(surah, lines_between=4, font_size=34, line_spacing=1.9):
    surah_name = html.escape(surah["name"])
    english_name = html.escape(surah["englishName"])
    english_translation = html.escape(surah["englishNameTranslation"])
    revelation = html.escape(surah["revelationType"])
    number = surah["number"]
    ayahs = surah["ayahs"]

    ayah_blocks = []
    for index, ayah in enumerate(ayahs):
        text = html.escape(ayah["text"].strip())

        if number>3:

            bismillah ="بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ"

            text = text.replace(bismillah, "").strip()


        ayah_no = ayah["numberInSurah"]

        writing_lines = ""
        if index < len(ayahs):
            writing_lines = (
                '<div class="writing-lines">'
                + "".join('<div class="writing-line"></div>' for _ in range(lines_between))
                + "</div>"
            )

        ayah_blocks.append(
            f"""
            <section class="ayah-block">
                <div class="ayah-text">
                    {text}
                    <span class="ayah-marker">﴿{ayah_no}﴾</span>
                </div>
                {writing_lines}
            </section>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{english_name} — {surah_name}</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

    :root {{
        --page-width: 210mm;
        --page-min-height: 297mm;
        --ink: #3d2517;
        --rule: #7f776f;
        --gold: #b18a47;
    }}

    * {{
        box-sizing: border-box;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        background: #eee;
        color: var(--ink);
    }}

    body {{
        font-family: "Amiri", "Noto Naskh Arabic", "Traditional Arabic", serif;
    }}

    /* =========================
       A4 PAGE - SCREEN / PREVIEW
       ========================= */

    .page {{
        width: var(--page-width);
        min-height: var(--page-min-height);

        margin: 12mm auto;
        padding: 14mm 17mm 16mm;

        background: white;
        box-shadow: 0 0 8px rgba(0, 0, 0, .15);

        overflow: hidden;
    }}

    /* =========================
       SURAH HEADER
       ========================= */

    .header {{
        text-align: center;

        border-bottom: 1px solid var(--gold);

        padding-bottom: 8mm;
        margin-bottom: 10mm;
    }}

    .bismillah {{
        font-size: 22px;
        margin-bottom: 7mm;
    }}

    .surah-title {{
        font-size: 34px;
        font-weight: 700;
        margin: 0;
    }}

    .english-title {{
        direction: ltr;
        font-family: Georgia, serif;
        font-size: 16px;
        margin-top: 2mm;
    }}

    .meta {{
        direction: ltr;
        font-family: Arial, sans-serif;
        font-size: 10px;
        color: #777;
        margin-top: 2mm;
    }}

    /* =========================
       AYAH
       ========================= */

    .ayah-block {{
        break-inside: avoid;
        page-break-inside: avoid;

        margin: 0 0 5mm;
    }}

    .ayah-text {{
        text-align: center;

        font-size: {font_size}px;
        line-height: {line_spacing};
        font-weight: 400;

        padding: 2mm 0 4mm;
    }}

    .ayah-marker {{
        font-size: .72em;
        white-space: nowrap;
        margin-inline-start: .25em;
    }}

    /* =========================
       WRITING LINES
       ========================= */

    .writing-lines {{
        display: flex;
        flex-direction: column;

        gap: 15mm;

        padding: 2mm 0 7mm;
    }}

    .writing-line {{
        height: 0;

        border-top: 1px solid var(--rule);

        width: 100%;
    }}

    /* =========================
       PRINT / PDF
       ========================= */

    @media print {{

        @page {{
            size: A4 portrait;

            /*
             * Remove browser left/right
             * page margins.
             */
            margin: 15mm 0 15mm 0;
        }}

        html,
        body {{
            background: white;

            margin: 0;
            padding: 0;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;

            /*
             * No outer margin when printing.
             */
            margin: 0;

            /*
             * Keep padding here so the Quran
             * text does not touch the edge.
             */
            padding: 14mm 17mm 16mm;

            background: white;

            box-shadow: none;

            page-break-after: always;
            break-after: page;
        }}

        .page:last-child {{
            page-break-after: auto;
            break-after: auto;
        }}
    }}

    /* =========================
       MOBILE / SMALL SCREEN
       ========================= */

    @media screen and (max-width: 800px) {{

        .page {{
            width: 100%;
            min-height: auto;

            margin: 0;
            padding: 20px;
        }}

        .ayah-text {{
            font-size: max(26px, {font_size}px);
        }}
    }}
</style>
</head>
<body>
<div class="page">
    <header class="header">
        <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
        <h1 class="surah-title">{surah_name}</h1>
        <div class="english-title">{english_name} — {english_translation}</div>
        <div class="meta">Surah {number} · {revelation} · {surah["numberOfAyahs"]} Ayahs</div>
    </header>

    <main>
        {''.join(ayah_blocks)}
    </main>
</div>
</body>
</html>
"""

try:
    surahs = get_surah_list()
except Exception as exc:
    st.error(f"Could not load the Surah list: {exc}")
    st.stop()

surah_options = {
    f'{s["number"]}. {s["englishName"]} — {s["name"]}': s["number"]
    for s in surahs
}

with st.sidebar:
    st.header("Settings")
    selected_label = st.selectbox("Select Surah", list(surah_options.keys()), index=0)
    selected_number = surah_options[selected_label]

    lines_between = st.number_input(
        "Lines between Ayahs",
        min_value=1,
        max_value=8,
        value=4,
        step=1,
    )

    font_size = st.slider(
        "Arabic font size",
        min_value=24,
        max_value=52,
        value=34,
        step=1,
    )

    line_spacing = st.slider(
        "Arabic line spacing",
        min_value=1.2,
        max_value=2.5,
        value=1.9,
        step=0.1,
    )

    st.divider()
    st.markdown(
        "Source: [Al Quran Cloud API](https://alquran.cloud/api)"
    )

try:
    surah = get_surah(selected_number)
except Exception as exc:
    st.error(f"Could not fetch the selected Surah: {exc}")
    st.stop()

generated_html = build_html(
    surah,
    lines_between=int(lines_between),
    font_size=int(font_size),
    line_spacing=float(line_spacing),
)

st.subheader(f'{surah["englishName"]} — {surah["name"]}')
st.write(
    f'{surah["numberOfAyahs"]} Ayahs · {surah["revelationType"]} · '
    f'Edition: `{EDITION}`'
)

tab_preview, tab_source = st.tabs(["Preview", "HTML"])

with tab_preview:
    components.html(generated_html, height=900, scrolling=True)

with tab_source:
    st.code(generated_html, language="html")

filename = f'surah_{surah["number"]:03d}_{surah["englishName"].replace(" ", "_")}.html'
st.download_button(
    "⬇️ Download HTML",
    data=generated_html.encode("utf-8"),
    file_name=filename,
    mime="text/html",
    use_container_width=True,
)
