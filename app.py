import random
import streamlit as st
from generator import generate_code
from config import LANGUAGES, LEVELS, EXAMPLES, MODELS, LANG_COLORS

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Code Generator", page_icon="⚡", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Pill-shaped example buttons */
  div[data-testid="stButton"] button {
    border-radius: 999px !important;
    font-size: 0.78rem !important;
    padding: 4px 14px !important;
  }
  /* Footer */
  .footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    text-align: center; padding: 7px;
    font-size: 0.72rem; color: #555;
    background: #0f0f0f;
    border-top: 1px solid #222;
    z-index: 999;
  }
</style>
<div class="footer">By YASH KUMAR MEHTA & AMIT MOURYA</div>
""", unsafe_allow_html=True)

# ── Styled header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 0.5rem 0 1.2rem; border-bottom: 1px solid #2a2a2a; margin-bottom: 1.4rem;">
  <h1 style="font-size: 2rem; font-weight: 700; margin: 0;">AI Code Generator</h1>
  <p style="color: #888; margin: 5px 0 0; font-size: 0.92rem;">
    Generate production-ready code in 18+ languages — powered by Google Gemini
  </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar — history ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🕘 Generation history")
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        if st.button("🗑 Clear history", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        st.markdown("---")
        for i, item in enumerate(reversed(st.session_state.history)):
            label = f"{item['language']} · {item['prompt'][:28]}…"
            if st.button(label, key=f"hist_{i}", use_container_width=True):
                st.session_state.output = item["code"]
                st.session_state.language = item["language"]
                st.session_state.usage = {}
                st.rerun()
    else:
        st.caption("No generations yet. Write a prompt and hit Generate!")

# ── Session state init ────────────────────────────────────────────────────────
for key in ["output", "language", "usage"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ── Loading messages ──────────────────────────────────────────────────────────
LOADING_MESSAGES = [
    "Summoning the code gods...",
    "Asking Gemini nicely...",
    "Converting coffee to code...",
    "Compiling your masterpiece...",
    "Teaching the AI to code for you...",
]

# ══════════════════════════════════════════════════════════════════════════════
# INPUT FORM
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.output is None:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Language + model + level
        language = st.selectbox("Programming language", LANGUAGES)
        model_label = st.selectbox("AI model", list(MODELS.keys()))
        level = st.selectbox("Complexity level", LEVELS, index=1)
        explain = st.checkbox("Include explanation after the code")

        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

        # Example prompt chips
        st.caption("Quick examples — click to fill:")
        ex_cols = st.columns(2)
        for i, ex in enumerate(EXAMPLES):
            if ex_cols[i % 2].button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state["prefill"] = ex
                st.rerun()

        prompt = st.text_area(
            "What do you want to build?",
            value=st.session_state.get("prefill", ""),
            height=150,
            placeholder="e.g. A REST API endpoint that validates email addresses",
        )

        if st.button("Generate Code", use_container_width=True, type="primary"):
            if not prompt.strip():
                st.warning("Please enter a prompt before generating.")
            else:
                st.session_state["prefill"] = ""
                chosen_model = MODELS[model_label]
                stream_box = st.empty()
                with st.spinner(random.choice(LOADING_MESSAGES)):
                    result, usage = generate_code(
                        language, prompt, level,
                        stream_placeholder=stream_box,
                        explain=explain,
                        model=chosen_model,
                    )

                if result.startswith("# Error"):
                    st.error(f"Something went wrong. Check your API key or try again.\n\n{result}")
                else:
                    st.session_state.output = result
                    st.session_state.language = language
                    st.session_state.usage = usage
                    st.session_state.history.append({
                        "language": language, "prompt": prompt, "code": result
                    })
                    st.rerun()

    with col2:
        st.markdown("""
        <div style="background:#1a1a1a; border:1px solid #2a2a2a; border-radius:12px; padding:20px; margin-top:8px;">
          <p style="font-weight:600; margin:0 0 12px; font-size:0.9rem;">How to use</p>
          <ol style="color:#aaa; font-size:0.82rem; line-height:1.9; padding-left:16px; margin:0;">
            <li>Pick a programming language</li>
            <li>Choose AI model & complexity</li>
            <li>Click an example or write your own prompt</li>
            <li>Hit <strong style="color:#e8e8e8;">Generate Code</strong></li>
            <li>Refine the result with follow-up prompts</li>
            <li>Download your code file</li>
          </ol>
          <hr style="border-color:#2a2a2a; margin:14px 0;">
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT VIEW
# ══════════════════════════════════════════════════════════════════════════════
else:
    lang = (st.session_state.language or "text").lower()
    code_output = st.session_state.output or ""
    color = LANG_COLORS.get(lang, "#7F77DD")

    # Language badge + success
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
      <span style="background:{color}22; color:{color}; padding:4px 14px;
        border-radius:999px; font-size:0.8rem; font-weight:700;
        border:1px solid {color}44;">
        {st.session_state.language}
      </span>
      <span style="color:#3B6D11; font-size:0.88rem;">✓ Code generated successfully</span>
    </div>
    """, unsafe_allow_html=True)

    # Token usage metrics
    usage = st.session_state.usage or {}
    if usage and usage.get("prompt_tokens") != "—":
        m1, m2, m3 = st.columns(3)
        m1.metric("Prompt tokens", usage.get("prompt_tokens", "—"))
        m2.metric("Output tokens", usage.get("output_tokens", "—"))

    # Code block
    st.code(code_output, language=lang)

    # Generate unit tests button
    st.markdown("---")
    tcol1, tcol2 = st.columns([3, 1])
    with tcol2:
        if st.button("🧪 Generate unit tests", use_container_width=True):
            test_stream = st.empty()
            with st.spinner("Writing tests..."):
                tests, _ = generate_code(
                    st.session_state.language,
                    f"Write unit tests for this code:\n\n{code_output}",
                    level="intermediate",
                    stream_placeholder=test_stream,
                )
            st.session_state.output = tests
            st.session_state.history.append({
                "language": st.session_state.language,
                "prompt": "Unit tests",
                "code": tests,
            })
            st.rerun()

    # Refine prompt
    with tcol1:
        refine = st.text_input(
            "Refine or modify",
            placeholder="e.g. make it async · add type hints · add error handling",
        )
    if st.button("Apply refinement ⚡", type="primary"):
        if refine.strip():
            stream_box = st.empty()
            with st.spinner(random.choice(LOADING_MESSAGES)):
                refined, new_usage = generate_code(
                    st.session_state.language,
                    f"Here is existing code:\n{code_output}\n\nNow: {refine}",
                    stream_placeholder=stream_box,
                )
            st.session_state.output = refined
            st.session_state.usage = new_usage
            st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Generate another", use_container_width=True):
            st.session_state.output = None
            st.session_state.language = None
            st.session_state.usage = None
            st.rerun()
    with col2:
        st.download_button(
            "⬇ Download code",
            data=code_output,
            file_name=f"generated.{lang}",
            mime="text/plain",
            use_container_width=True,
        )
