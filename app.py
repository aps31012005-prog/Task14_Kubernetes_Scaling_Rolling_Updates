
import streamlit as st
import requests
from PIL import Image

# ==========================================
# Page Configuration & Styling
# ==========================================

st.set_page_config(
    page_title="CIFAR-10 Deep Learning App",
    page_icon="🧠",
    layout="wide"
)

# ==========================================
# UI Styling
# ==========================================

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
    }

    .class-badge {
        border: 1px solid #313745;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .class-badge:hover {
        border-color: #4CAF50;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }

    header {
        visibility: hidden !important;
    }

    .stApp > header {
        display: none !important;
    }

    button[title="View fullscreen"] {
        display: none !important;
    }

    [data-testid="stElementToolbar"] {
        display: none !important;
    }

    [data-testid="stStyledFullScreenButton"] {
        display: none !important;
    }

    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# Flask API Configuration
# ==========================================

# IMPORTANT:
# "flask-api" will be the Flask service name
# inside docker-compose.yml.
FLASK_API_URL = "http://flask-api-service:5000"

# ==========================================
# CIFAR-10 Class Names
# ==========================================

class_names = [
    "Airplane ✈️",
    "Automobile 🚗",
    "Bird 🐦",
    "Cat 🐱",
    "Deer 🦌",
    "Dog 🐶",
    "Frog 🐸",
    "Horse 🐴",
    "Ship 🚢",
    "Truck 🚚"
]

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("🧠 CIFAR-10 AI Platform")
st.sidebar.markdown("---")

st.sidebar.info(
    "**Deep Learning Showcase**\n\n"
    "This application uses a Streamlit frontend "
    "connected to a Flask REST API for CIFAR-10 image classification."
)

st.sidebar.markdown("---")
st.sidebar.caption("⚡ Streamlit + Flask + TensorFlow + Docker")

# ==========================================
# Hero Banner
# ==========================================

st.title("🧠 CIFAR-10 Image Classification Suite")

st.caption(
    "Interactive Neural Network Dashboard & Flask API Integration"
)

st.markdown(
    """
    > **Overview:** Experience real-time multi-class object recognition
    using a Convolutional Neural Network (CNN) served through a Flask
    REST API and displayed through a Streamlit frontend.
    """
)

st.markdown("---")

# ==========================================
# Key Dataset Metrics
# ==========================================

st.subheader("📊 Key Overview Metrics")

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.metric(
        "Training Set",
        "50,000",
        help="Number of images used during model training"
    )

with m2:
    st.metric(
        "Testing Set",
        "10,000",
        help="Independent images used for evaluation"
    )

with m3:
    st.metric(
        "Resolution",
        "32 × 32 px",
        help="RGB Color Input Dimensions"
    )

with m4:
    st.metric(
        "Target Classes",
        "10 Categories"
    )

with m5:
    st.metric(
        "Test Accuracy",
        "72.4%",
        delta="Epochs: 10"
    )

st.markdown("---")

# ==========================================
# Class Categories
# ==========================================

st.subheader("🏷️ Target Classification Categories")

cols = st.columns(5)

for idx, class_name in enumerate(class_names):

    with cols[idx % 5]:

        st.markdown(
            f"""
            <div class="class-badge">
                Class {idx}<br>
                <b>{class_name}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# ==========================================
# Neural Network Configuration
# ==========================================

st.subheader("🤖 Neural Network Configuration")

with st.expander(
    "🔍 Click to view detailed model architecture parameters",
    expanded=True
):

    col_a, col_b = st.columns(2)

    with col_a:

        st.markdown(
            """
            * **Architecture:** Sequential Convolutional Neural Network (CNN)
            * **Optimization Algorithm:** Adam
            * **Loss Calculation:** Sparse Categorical Crossentropy
            * **Classification Layer:** 10 Units with Softmax Activation
            """
        )

    with col_b:

        st.markdown(
            """
            * **Input Tensor Shape:** `(32, 32, 3)`
            * **Feature Extractors:** 2x Conv2D + MaxPooling Blocks
            * **Regularization:** Dropout (0.5 Rate)
            * **Hidden Layer Units:** 128 Dense Units (ReLU Activation)
            """
        )

st.markdown("---")

# ==========================================
# Flask API Connection Check
# ==========================================

st.subheader("🔌 Backend API Status")

if st.button("🔄 Check Flask API Connection"):

    try:

        response = requests.get(
            f"{FLASK_API_URL}/",
            timeout=5
        )

        if response.status_code == 200:

            st.success(
                "✅ Flask API is connected and running."
            )

            st.json(response.json())

        else:

            st.error(
                f"⚠️ Flask API returned status code "
                f"{response.status_code}"
            )

    except requests.exceptions.RequestException as e:

        st.error(
            "❌ Unable to connect to Flask API."
        )

        st.caption(
            f"Connection details: {e}"
        )

# ==========================================
# Image Prediction
# ==========================================

st.markdown("---")

st.subheader("🔮 Image Prediction")

st.write(
    "Upload an image and the Streamlit frontend will send it "
    "to the Flask REST API for prediction."
)

uploaded_file = st.file_uploader(
    "📤 Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Display uploaded image

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    with col2:

        st.info(
            "Image received successfully. "
            "Click the button below to send it to the Flask API."
        )

        predict_button = st.button(
            "🚀 Predict Image",
            type="primary"
        )

        if predict_button:

            try:

                # Reset file position

                uploaded_file.seek(0)

                # Prepare image for Flask API

                files = {
                    "image": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }

                # Send image to Flask API

                response = requests.post(
                    f"{FLASK_API_URL}/predict",
                    files=files,
                    timeout=60
                )

                # ==========================================
                # Successful Response
                # ==========================================

                if response.status_code == 200:

                    result = response.json()

                    predicted_class = result.get(
                        "predicted_class",
                        "Unknown"
                    )

                    confidence = result.get(
                        "confidence",
                        0
                    )

                    st.success(
                        "✅ Prediction completed successfully!"
                    )

                    st.metric(
                        "Predicted Class",
                        predicted_class
                    )

                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}%"
                    )

                    st.progress(
                        min(max(confidence / 100, 0.0), 1.0)
                    )

                    st.json(result)

                # ==========================================
                # Flask Error Response
                # ==========================================

                else:

                    try:
                        error_data = response.json()
                    except Exception:
                        error_data = {
                            "error": response.text
                        }

                    st.error(
                        f"❌ Flask API error "
                        f"(HTTP {response.status_code})"
                    )

                    st.json(error_data)

            except requests.exceptions.RequestException as e:

                st.error(
                    "❌ Could not connect to Flask API."
                )

                st.warning(
                    "Make sure the Flask container is running "
                    "and both containers are connected through "
                    "the Docker network."
                )

                st.caption(
                    f"Connection details: {e}"
                )

            except Exception as e:

                st.error(
                    "❌ An unexpected error occurred."
                )

                st.caption(
                    f"Error details: {e}"
                )

# ==========================================
# Footer / Status
# ==========================================

st.markdown("---")

st.caption(
    "🐳 Task 11 — Full Application Containerization | "
    "Streamlit Frontend → Flask REST API → CIFAR-10 CNN Model"
)
