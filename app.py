import streamlit as st
import parselmouth
from parselmouth.praat import call
import numpy as np
import pandas as pd
import tempfile

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="PhoneticLab",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================
# CUSTOM DESIGN
# ====================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f9f6fb;
}

/* Global padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Main title */
.main-title {
    font-size: 52px;
    font-weight: 800;
    color: #c2185b;
    margin-bottom: 0;
}

/* Subtitle */
.subtitle {
    color: #7b1fa2;
    font-size: 20px;
    margin-top: 0;
    margin-bottom: 25px;
}

/* Section cards */
.custom-card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(194, 24, 91, 0.08);
    border: 1px solid #f3d9e5;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8d7e8;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #4a154b;
}

/* Buttons */
.stButton button {
    border-radius: 12px;
    background-color: #d81b60;
    color: white;
    font-weight: 700;
    border: none;
    padding: 10px 18px;
}

.stDownloadButton button {
    border-radius: 12px;
    background-color: #e91e63;
    color: white;
    font-weight: 700;
    border: none;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ====================================
# HEADER
# ====================================

st.markdown(
    '<p class="main-title">🎀 PhoneticLab</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Modular Corpus-Oriented Speech Analysis Platform</p>',
    unsafe_allow_html=True
)

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("⚙️ Analysis Workspace")

# ====================================
# PROJECT SECTION
# ====================================

st.sidebar.markdown("---")

project_name = st.sidebar.text_input(
    "📁 Project Name"
)

# ====================================
# ANALYSIS SELECTION
# ====================================

st.sidebar.markdown("---")

st.sidebar.subheader("🔬 Select Analyses")

run_acoustic = st.sidebar.checkbox(
    "Acoustic Analysis"
)

run_prosody = st.sidebar.checkbox(
    "Prosodic Analysis"
)

run_voice = st.sidebar.checkbox(
    "Voice Quality Analysis"
)

# ====================================
# ADVANCED SETTINGS
# ====================================

st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Advanced Settings")

pitch_floor = st.sidebar.slider(
    "Pitch Floor (Hz)",
    50,
    150,
    75
)

pitch_ceiling = st.sidebar.slider(
    "Pitch Ceiling (Hz)",
    200,
    600,
    500
)

time_step = st.sidebar.slider(
    "Time Step",
    0.001,
    0.05,
    0.01
)

# ====================================
# PARAMETER SELECTION
# ====================================

selected_acoustic = []
selected_prosody = []
selected_voice = []

# ---------- Acoustic ----------

if run_acoustic:

    st.sidebar.markdown("---")

    st.sidebar.subheader("📊 Acoustic Parameters")

    selected_acoustic = st.sidebar.multiselect(

        "Choose acoustic parameters",

        [
            "Mean Pitch",
            "Pitch Range",
            "Pitch Variability",
            "Mean Intensity"
        ]
    )

# ---------- Prosodic ----------

if run_prosody:

    st.sidebar.markdown("---")

    st.sidebar.subheader("🎵 Prosodic Parameters")

    selected_prosody = st.sidebar.multiselect(

        "Choose prosodic parameters",

        [
            "Duration",
            "Pitch Variability",
            "Intensity Variability"
        ]
    )

# ---------- Voice Quality ----------

if run_voice:

    st.sidebar.markdown("---")

    st.sidebar.subheader("🎙️ Voice Quality Parameters")

    selected_voice = st.sidebar.multiselect(

        "Choose voice quality parameters",

        [
            "Jitter",
            "Shimmer",
            "HNR"
        ]
    )

# ====================================
# RUN BUTTON
# ====================================

st.sidebar.markdown("---")

run_analysis = st.sidebar.button("▶ Run Analysis")

# ====================================
# PROJECT DISPLAY
# ====================================

st.markdown(
    f"## 📁 Current Project: {project_name}"
)

# ====================================
# DASHBOARD
# ====================================

with st.container():

    st.markdown(
        '<div class="custom-card">',
        unsafe_allow_html=True
    )

    st.markdown("## 📊 Corpus Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Platform", "Active")

    with c2:
        st.metric("Workflow", "Modular")

    with c3:
        st.metric("Analysis", "Custom")

    with c4:
        st.metric("Status", "Ready")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# ====================================
# FILE UPLOAD
# ====================================

with st.container():

    st.markdown(
        '<div class="custom-card">',
        unsafe_allow_html=True
    )

    st.markdown("## 📂 Upload Corpus")

    uploaded_files = st.file_uploader(
        "Upload WAV files",
        type=["wav"],
        accept_multiple_files=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# ====================================
# MAIN ANALYSIS
# ====================================

if uploaded_files and run_analysis:

    st.success("Analysis started!")

    progress_bar = st.progress(0)

    corpus_results = []
    acoustic_results = []
    prosody_results = []
    voice_results = []

    for i, uploaded_file in enumerate(uploaded_files):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())

            temp_path = tmp_file.name

        sound = parselmouth.Sound(temp_path)

        # ====================================
        # PITCH EXTRACTION
        # ====================================

        pitch = sound.to_pitch(

            time_step=time_step,

            pitch_floor=pitch_floor,

            pitch_ceiling=pitch_ceiling
        )

        pitch_values = pitch.selected_array['frequency']

        pitch_values = pitch_values[pitch_values != 0]

        intensity = sound.to_intensity()

        intensity_values = intensity.values[0]

        duration = sound.get_total_duration()

        # ====================================
        # CORPUS TABLE
        # ====================================

        corpus_results.append({

            "File": uploaded_file.name,
            "Status": "Processed"
        })

        # ====================================
        # ACOUSTIC ANALYSIS
        # ====================================

        if run_acoustic:

            acoustic_row = {
                "File": uploaded_file.name
            }

            if "Mean Pitch" in selected_acoustic:

                acoustic_row["Mean Pitch"] = round(
                    np.mean(pitch_values),
                    2
                )

            if "Pitch Range" in selected_acoustic:

                acoustic_row["Pitch Range"] = round(
                    np.max(pitch_values) - np.min(pitch_values),
                    2
                )

            if "Pitch Variability" in selected_acoustic:

                acoustic_row["Pitch Variability"] = round(
                    np.std(pitch_values),
                    2
                )

            if "Mean Intensity" in selected_acoustic:

                acoustic_row["Mean Intensity"] = round(
                    np.mean(intensity_values),
                    2
                )

            acoustic_results.append(acoustic_row)

        # ====================================
        # PROSODIC ANALYSIS
        # ====================================

        if run_prosody:

            prosody_row = {
                "File": uploaded_file.name
            }

            if "Duration" in selected_prosody:

                prosody_row["Duration"] = round(
                    duration,
                    2
                )

            if "Pitch Variability" in selected_prosody:

                prosody_row["Pitch Variability"] = round(
                    np.std(pitch_values),
                    2
                )

            if "Intensity Variability" in selected_prosody:

                prosody_row["Intensity Variability"] = round(
                    np.std(intensity_values),
                    2
                )

            prosody_results.append(prosody_row)

        # ====================================
        # VOICE QUALITY
        # ====================================

        if run_voice:

            point_process = call(
                sound,
                "To PointProcess (periodic, cc)",
                pitch_floor,
                pitch_ceiling
            )

            voice_row = {
                "File": uploaded_file.name
            }

            if "Jitter" in selected_voice:

                jitter = call(
                    point_process,
                    "Get jitter (local)",
                    0,
                    0,
                    0.0001,
                    0.02,
                    1.3
                )

                voice_row["Jitter"] = round(
                    jitter,
                    5
                )

            if "Shimmer" in selected_voice:

                shimmer = call(
                    [sound, point_process],
                    "Get shimmer (local)",
                    0,
                    0,
                    0.0001,
                    0.02,
                    1.3,
                    1.6
                )

                voice_row["Shimmer"] = round(
                    shimmer,
                    5
                )

            if "HNR" in selected_voice:

                harmonicity = sound.to_harmonicity()

                hnr = call(
                    harmonicity,
                    "Get mean",
                    0,
                    0
                )

                voice_row["HNR"] = round(
                    hnr,
                    2
                )

            voice_results.append(voice_row)

        progress_bar.progress(
            (i + 1) / len(uploaded_files)
        )

    # ====================================
    # RESULTS TABLE
    # ====================================

    corpus_df = pd.DataFrame(corpus_results)

    st.markdown("## 📁 Corpus Management")

    st.dataframe(
        corpus_df,
        use_container_width=True
    )

    # ====================================
    # TABS
    # ====================================

    tab_names = []

    if run_acoustic:
        tab_names.append("📊 Acoustic")

    if run_prosody:
        tab_names.append("🎵 Prosodic")

    if run_voice:
        tab_names.append("🎙️ Voice Quality")

    tabs = st.tabs(tab_names)

    tab_index = 0

    # ====================================
    # ACOUSTIC TAB
    # ====================================

    if run_acoustic:

        acoustic_df = pd.DataFrame(acoustic_results)

        with tabs[tab_index]:

            st.subheader("Acoustic Results")

            st.dataframe(
                acoustic_df,
                use_container_width=True
            )

        tab_index += 1

    # ====================================
    # PROSODIC TAB
    # ====================================

    if run_prosody:

        prosody_df = pd.DataFrame(prosody_results)

        with tabs[tab_index]:

            st.subheader("Prosodic Results")

            st.dataframe(
                prosody_df,
                use_container_width=True
            )

        tab_index += 1

    # ====================================
    # VOICE TAB
    # ====================================

    if run_voice:

        voice_df = pd.DataFrame(voice_results)

        with tabs[tab_index]:

            st.subheader("Voice Quality Results")

            st.dataframe(
                voice_df,
                use_container_width=True
            )

    # ====================================
    # EXPORTS
    # ====================================

    st.markdown("## ⬇️ Export Results")

    export_cols = st.columns(3)

    col_index = 0

    if run_acoustic:

        acoustic_csv = acoustic_df.to_csv(
            index=False
        ).encode("utf-8")

        with export_cols[col_index]:

            st.download_button(
                "Download Acoustic CSV",
                acoustic_csv,
                f"{project_name}_acoustic_results.csv",
                "text/csv"
            )

        col_index += 1

    if run_prosody:

        prosody_csv = prosody_df.to_csv(
            index=False
        ).encode("utf-8")

        with export_cols[col_index]:

            st.download_button(
                "Download Prosodic CSV",
                prosody_csv,
                f"{project_name}_prosodic_results.csv",
                "text/csv"
            )

        col_index += 1

    if run_voice:

        voice_csv = voice_df.to_csv(
            index=False
        ).encode("utf-8")

        with export_cols[col_index]:

            st.download_button(
                "Download Voice CSV",
                voice_csv,
                f"{project_name}_voice_results.csv",
                "text/csv"
            )

# ====================================
# FOOTER
# ====================================

st.markdown("---")

st.caption("🎀 PhoneticLab • Modular Speech Analysis Platform")