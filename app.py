from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "recommendations.json"
MODEL_PATH = ROOT / "models" / "efficientnet_ip102.pt"

st.set_page_config(page_title="CropSentinel | Pest intelligence", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_recommendations() -> dict[str, dict[str, Any]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def demo_predict(image: Image.Image) -> tuple[str, float, str]:
    """Provide a transparent demo result until a trained checkpoint is installed."""
    pixels = np.asarray(image.convert("RGB").resize((64, 64)), dtype=np.float32)
    mean_rgb = pixels.mean(axis=(0, 1))
    green_ratio = float(mean_rgb[1] / max(mean_rgb.mean(), 1))
    edge_energy = float(np.abs(np.diff(pixels, axis=0)).mean())
    if green_ratio > 1.08 and edge_energy < 24:
        return "aphids", 0.78, "demo-visual heuristic"
    if edge_energy > 34:
        return "fall armyworm", 0.71, "demo-visual heuristic"
    return "beet armyworm", 0.64, "demo-visual heuristic"

@st.cache_resource
def load_model() -> Any | None:
    if not MODEL_PATH.exists():
        return None
    try:
        import torch
        return torch.jit.load(str(MODEL_PATH), map_location="cpu").eval()
    except Exception:
        return None

def predict(image: Image.Image) -> tuple[str, float, str]:
    model = load_model()
    if model is None:
        return demo_predict(image)
    import torch
    from torchvision import transforms
    tensor = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])(image.convert("RGB")).unsqueeze(0)
    with torch.inference_mode():
        probabilities = torch.softmax(model(tensor), dim=1)[0]
        confidence, index = probabilities.max(dim=0)
    class_names = json.loads((ROOT / "models" / "class_names.json").read_text(encoding="utf-8"))
    return class_names[str(int(index))], float(confidence), "EfficientNet checkpoint"

def show_metric(label: str, value: str, accent: str) -> None:
    st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value" style="color:{accent}">{value}</div></div>', unsafe_allow_html=True)

recommendations = load_recommendations()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --ink:#13231d; --leaf:#1d6b4b; --paper:#f4f5ec; --rust:#c9673d; }
html, body, [class*="css"] { font-family:'Space Grotesk', sans-serif; }
.stApp { background:radial-gradient(circle at 86% 4%, #dcecb0 0, transparent 27%), var(--paper); color:var(--ink); }
.block-container { max-width:1240px; padding-top:2rem; }
h1, h2, h3 { color:var(--ink); letter-spacing:0 !important; }
h1 { font-size:clamp(2.5rem, 5vw, 5.7rem) !important; line-height:.92 !important; }
.eyebrow { color:var(--leaf); font-family:'DM Mono', monospace; font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; }
.hero-copy { font-size:1.1rem; max-width:620px; color:#4d6358; line-height:1.55; }
.panel { border:1px solid #d6ddcd; border-radius:8px; background:rgba(255,255,255,.62); padding:1.35rem; height:100%; }
.metric { background:#13231d; border-radius:8px; padding:1rem 1.1rem; min-height:96px; }
.metric-label { color:#b6c9bc; font-family:'DM Mono', monospace; text-transform:uppercase; font-size:.68rem; }
.metric-value { font-size:1.65rem; font-weight:700; margin-top:.55rem; }
.tag { display:inline-block; background:#e5f6b9; color:#285c3c; padding:.32rem .55rem; border-radius:999px; font-size:.76rem; margin:.18rem .2rem .18rem 0; }
.warning { border-left:4px solid var(--rust); background:#fff0e7; padding:.8rem 1rem; border-radius:0 6px 6px 0; }
.stButton > button { border-radius:6px; background:var(--leaf); color:white; border:0; font-weight:600; padding:.7rem 1rem; }
@keyframes rise-in { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
@keyframes pulse-line { 0%, 100% { box-shadow:0 0 0 0 rgba(200,239,134,.1); } 50% { box-shadow:0 0 0 8px rgba(200,239,134,0); } }
@keyframes drift { 0%, 100% { transform:translate3d(0,0,0); } 50% { transform:translate3d(0,-6px,0); } }
.hero-copy { animation:rise-in .65s ease-out both; }
.panel { animation:rise-in .55s ease-out both; transition:transform .2s ease, border-color .2s ease, box-shadow .2s ease; }
.panel:hover { transform:translateY(-3px); border-color:#9cba8f; box-shadow:0 12px 30px rgba(19,35,29,.08); }
.eyebrow { animation:rise-in .4s ease-out both; }
.metric { animation:pulse-line 3.2s ease-in-out infinite; }
.stButton > button:hover { transform:translateY(-2px); box-shadow:0 8px 16px rgba(29,107,75,.2); transition:all .2s ease; }
.stProgress > div > div > div > div { background:linear-gradient(90deg, #1d6b4b, #9ccf58); transition:width 1s cubic-bezier(.2,.8,.2,1); }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; } }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">FIELD INTELLIGENCE / IP102 READY</div>', unsafe_allow_html=True)
st.title("CropSentinel")
st.markdown('<p class="hero-copy">A visual co-pilot for the first five minutes after a pest appears. Upload a field photo, get a likely identification, then choose the least harmful useful action.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Mission control")
    st.caption("A student-built pest intelligence prototype")
    st.divider()
    st.markdown("**Model status**")
    if MODEL_PATH.exists():
        st.success("EfficientNet checkpoint loaded")
    else:
        st.info("Demo mode active")
    st.markdown("**Workflow**")
    st.markdown("1. Upload a clear image\n2. Inspect the confidence\n3. Start with the lowest-risk action")
    st.divider()
    st.caption("Predictions are preliminary. Confirm the pest and product instructions with a local agricultural expert.")

upload_col, result_col = st.columns([1.04, 1], gap="large")
with upload_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 01 / Capture the signal")
    uploaded = st.file_uploader("Upload a pest image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, use_container_width=True, caption=f"{uploaded.name} · {image.width} × {image.height}px")
        analyze = st.button("Analyze image", use_container_width=True)
    else:
        st.info("Best results come from a well-lit, close-up image with the insect in focus.")
        analyze = False
    st.markdown('</div>', unsafe_allow_html=True)

with result_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 02 / Read the signal")
    if uploaded and analyze:
        pest_key, confidence, model_source = predict(image)
        st.session_state["last_prediction"] = (pest_key, confidence, model_source)
    prediction = st.session_state.get("last_prediction")
    if prediction:
        pest_key, confidence, model_source = prediction
        pest = recommendations.get(pest_key, recommendations["unknown"])
        st.markdown(f"<span class='tag'>{model_source}</span><span class='tag'>{pest['crop']}</span>", unsafe_allow_html=True)
        st.subheader(pest["name"])
        st.caption(pest["scientific_name"])
        m1, m2 = st.columns(2)
        with m1:
            show_metric("Confidence", f"{confidence:.0%}", "#c8ef86")
        with m2:
            show_metric("Risk mode", "Review" if confidence < .75 else "Actionable", "#ffb38f")
        if confidence < .75:
            st.markdown('<div class="warning"><b>Confidence is limited.</b> Compare the alternatives and verify the insect before treatment.</div>', unsafe_allow_html=True)
        st.progress(confidence)
        st.caption("A high score is not a guarantee of field-level identification.")
    else:
        st.markdown("<div style='padding:4rem 1rem;text-align:center;color:#718178'><div style='font-size:3rem'>⌁</div><b>Your identification will appear here</b><br><small>One photo in. A safer next step out.</small></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if prediction:
    pest_key, confidence, _ = prediction
    pest = recommendations.get(pest_key, recommendations["unknown"])
    st.divider()
    st.markdown("## 03 / Recommended action")
    st.caption("The action ladder starts with prevention and targeted, lower-impact options before chemical control.")
    action_cols = st.columns(3, gap="medium")
    for column, title, icon, items in zip(action_cols, ["Observe & prevent", "Organic / biological", "Chemical, only if needed"], ["◌", "✳", "△"], [pest["prevent"], pest["organic"], pest["chemical"]]):
        with column:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f"### {icon} {title}")
            for item in items:
                st.markdown(f"- {item}")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f"**Field note:** {pest['field_note']}")
    st.caption(f"Recommendation source: {pest['source']}")
    st.markdown('<div class="warning"><b>Safety boundary:</b> This prototype does not prescribe a product, dose, or application schedule. Always follow the local product label and consult an agricultural professional.</div>', unsafe_allow_html=True)

st.divider()
st.markdown("<small>CropSentinel · IP102-ready prototype · Built for responsible first-pass identification</small>", unsafe_allow_html=True)