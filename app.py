import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Breast Cancer Prediction",
    page_icon="🩺",
    layout="wide"
)

# =========================
# LANGUAGE
# =========================

language = st.sidebar.selectbox(
    "🌐 Language",
    [
        "English",
        "Bahasa Indonesia"
    ]
)

if language == "English":
    from en import TEXT
else:
    from id import TEXT

# =========================
# API CONFIG
# =========================

API_URL = "https://sleek-phony-patience.ngrok-free.dev/predict"

# =========================
# SIDEBAR
# =========================

st.sidebar.title(TEXT["sidebar_title"])

st.sidebar.info(
    f"""
**{TEXT["algorithm"]}**
- Support Vector Machine (SVM)

**{TEXT["dataset"]}**
- Breast Cancer Wisconsin Diagnostic

**{TEXT["input_features"]}**
- 30 Diagnostic Features

**{TEXT["output"]}**
- Benign
- Malignant
"""
)

# =========================
# HEADER
# =========================

st.title(TEXT["title"])

st.markdown(TEXT["description"])

# =========================
# FEATURE LIST
# =========================

features = [
    "Mean Radius",
    "Mean Texture",
    "Mean Perimeter",
    "Mean Area",
    "Mean Smoothness",
    "Mean Compactness",
    "Mean Concavity",
    "Mean Concave Points",
    "Mean Symmetry",
    "Mean Fractal Dimension",

    "Radius Error",
    "Texture Error",
    "Perimeter Error",
    "Area Error",
    "Smoothness Error",
    "Compactness Error",
    "Concavity Error",
    "Concave Points Error",
    "Symmetry Error",
    "Fractal Dimension Error",

    "Worst Radius",
    "Worst Texture",
    "Worst Perimeter",
    "Worst Area",
    "Worst Smoothness",
    "Worst Compactness",
    "Worst Concavity",
    "Worst Concave Points",
    "Worst Symmetry",
    "Worst Fractal Dimension"
]

# =========================
# INPUT
# =========================

col1, col2, col3 = st.columns(3)

inputs = []

for i in range(10):
    with col1:
        value = st.number_input(
            features[i],
            value=0.0,
            format="%.5f"
        )
        inputs.append(value)

for i in range(10, 20):
    with col2:
        value = st.number_input(
            features[i],
            value=0.0,
            format="%.5f"
        )
        inputs.append(value)

for i in range(20, 30):
    with col3:
        value = st.number_input(
            features[i],
            value=0.0,
            format="%.5f"
        )
        inputs.append(value)

st.divider()

# =========================
# PREDICT
# =========================

if st.button(TEXT["predict_button"], use_container_width=True):

    with st.spinner(TEXT["predicting"]):

        try:

            response = requests.post(
                API_URL,
                json={"features": inputs},
                timeout=30
            )

            response.raise_for_status()

            result = response.json()

            prediction = result["prediction"]

            probability = result["probability"]
                        st.subheader(TEXT["prediction_result"])

            if prediction == 1:

                st.success(
                    f"""
{TEXT["benign"]}

{TEXT["confidence"]}: {probability:.2%}
"""
                )

            else:

                st.error(
                    f"""
{TEXT["malignant"]}

{TEXT["confidence"]}: {probability:.2%}
"""
                )

            st.progress(float(probability))

            st.metric(
                label=TEXT["model_confidence"],
                value=f"{probability:.2%}"
            )

        except requests.exceptions.Timeout:

            st.error(TEXT["timeout"])

        except requests.exceptions.ConnectionError:

            st.error(TEXT["connection_error"])

        except requests.exceptions.HTTPError:

            st.error(TEXT["server_error"])

        except Exception as e:

            st.error(f'{TEXT["unknown_error"]}\n\n{e}')

st.divider()

st.caption(TEXT["footer"])
