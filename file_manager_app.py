import streamlit as st
from pathlib import Path
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileVault – File Manager",
    page_icon="🗂️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset / Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0f1117;
    color: #e2e8f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 60%);
    border: 1px solid #2a3145;
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 8px;
}
.hero-title {
    font-size: 32px;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 8px;
    line-height: 1.15;
}
.hero-title span { color: #818cf8; }
.hero-sub {
    font-size: 14px;
    color: #64748b;
    margin: 0;
}

/* ── Operation cards (tab buttons) ── */
.op-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 24px;
}
.op-card {
    background: #1a1f2e;
    border: 1px solid #2a3145;
    border-radius: 12px;
    padding: 16px 12px;
    text-align: center;
    cursor: pointer;
    transition: border-color .2s, background .2s;
}
.op-card:hover { border-color: #6366f1; background: #1e2438; }
.op-card.active { border-color: #6366f1; background: #1e2438; }
.op-icon { font-size: 22px; margin-bottom: 6px; }
.op-label { font-size: 12px; font-weight: 600; color: #94a3b8; }

/* ── Panel ── */
.panel {
    background: #1a1f2e;
    border: 1px solid #2a3145;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 16px;
}
.panel-title {
    font-size: 16px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 4px;
}
.panel-desc {
    font-size: 13px;
    color: #475569;
    margin-bottom: 20px;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0f1117 !important;
    border: 1px solid #2a3145 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #6366f1 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: background .2s, transform .1s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #4f46e5 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Radio (operation selector) ── */
.stRadio > div { flex-direction: row !important; gap: 8px; }
.stRadio label { color: #e2e8f0 !important; font-size: 13px !important; }

/* ── Alerts ── */
.stSuccess > div, .stError > div, .stInfo > div, .stWarning > div {
    border-radius: 10px !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── File content box ── */
.file-content {
    background: #0f1117;
    border: 1px solid #2a3145;
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #a5b4fc;
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.7;
    max-height: 300px;
    overflow-y: auto;
}

/* ── Divider ── */
hr { border-color: #2a3145 !important; margin: 8px 0 20px !important; }

/* ── Select box ── */
.stSelectbox > div > div {
    background: #0f1117 !important;
    border: 1px solid #2a3145 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #131720 !important; border-right: 1px solid #2a3145; }

</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🗂️ Python File Manager</div>
    <div class="hero-title">File<span>Vault</span></div>
    <p class="hero-sub">Create · Read · Update · Delete — right from your browser</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: workspace info ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📁 Workspace")
    workspace = st.text_input("Working directory", value=str(Path.cwd()), help="All files are relative to this path")
    st.markdown("---")

    work_dir = Path(workspace) if workspace else Path.cwd()
    if work_dir.exists():
        files = [f.name for f in work_dir.iterdir() if f.is_file()]
        if files:
            st.markdown(f"**{len(files)} file(s) found**")
            for f in sorted(files)[:20]:
                st.markdown(f"<span style='font-family:monospace;font-size:12px;color:#818cf8'>📄 {f}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#475569;font-size:13px'>No files in this directory</span>", unsafe_allow_html=True)
    else:
        st.error("Directory not found")

    st.markdown("---")
    st.markdown("<span style='font-size:11px;color:#334155'>Built with Python + Streamlit</span>", unsafe_allow_html=True)

# ── Operation selector ────────────────────────────────────────────────────────
OPERATIONS = {
    "➕ Create": "create",
    "📖 Read": "read",
    "✏️ Update": "update",
    "🗑️ Delete": "delete",
}

col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]

if "op" not in st.session_state:
    st.session_state.op = "create"

for i, (label, key) in enumerate(OPERATIONS.items()):
    with cols[i]:
        active = "active" if st.session_state.op == key else ""
        st.markdown(f"""<div class="op-card {active}" onclick="">
            <div class="op-icon">{label.split()[0]}</div>
            <div class="op-label">{label.split()[1]}</div>
        </div>""", unsafe_allow_html=True)

op = st.radio("", list(OPERATIONS.keys()), horizontal=True, label_visibility="collapsed")
st.session_state.op = OPERATIONS[op]
selected = st.session_state.op

st.markdown("<hr>", unsafe_allow_html=True)


# ── Helper ────────────────────────────────────────────────────────────────────
def resolve(name: str) -> Path:
    p = Path(name)
    if not p.is_absolute():
        p = work_dir / p
    return p


# ── CREATE ────────────────────────────────────────────────────────────────────
if selected == "create":
    st.markdown("""<div class="panel">
        <div class="panel-title">Create a new file</div>
        <div class="panel-desc">Enter a filename and write your content. The file will be saved in the working directory.</div>
    </div>""", unsafe_allow_html=True)

    fname = st.text_input("File name", placeholder="e.g. notes.txt", key="c_name")
    content = st.text_area("Content", placeholder="Start typing your file content here…", height=180, key="c_content")

    if st.button("Create File", key="create_btn"):
        if not fname.strip():
            st.error("Please enter a file name.")
        else:
            path = resolve(fname.strip())
            if path.exists():
                st.error(f"⚠️ **{path.name}** already exists. Choose a different name or use Update.")
            else:
                try:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                    st.success(f"✅ **{path.name}** created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ── READ ──────────────────────────────────────────────────────────────────────
elif selected == "read":
    st.markdown("""<div class="panel">
        <div class="panel-title">Read a file</div>
        <div class="panel-desc">Enter a filename to display its contents below.</div>
    </div>""", unsafe_allow_html=True)

    fname = st.text_input("File name", placeholder="e.g. notes.txt", key="r_name")

    if st.button("Read File", key="read_btn"):
        if not fname.strip():
            st.error("Please enter a file name.")
        else:
            path = resolve(fname.strip())
            if not path.exists():
                st.error(f"⚠️ **{fname}** does not exist.")
            else:
                try:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    size = path.stat().st_size
                    st.info(f"📄 **{path.name}** — {size} bytes")
                    if text.strip():
                        st.markdown(f'<div class="file-content">{text}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("This file is empty.")
                except Exception as e:
                    st.error(f"Error reading file: {e}")


# ── UPDATE ────────────────────────────────────────────────────────────────────
elif selected == "update":
    st.markdown("""<div class="panel">
        <div class="panel-title">Update a file</div>
        <div class="panel-desc">Rename, append new content, or completely overwrite an existing file.</div>
    </div>""", unsafe_allow_html=True)

    fname = st.text_input("File name", placeholder="e.g. notes.txt", key="u_name")
    action = st.selectbox("Operation", ["Rename", "Append content", "Overwrite content"], key="u_action")

    if action == "Rename":
        new_name = st.text_input("New file name", placeholder="e.g. renamed_notes.txt", key="u_new")
        if st.button("Rename File", key="rename_btn"):
            if not fname.strip() or not new_name.strip():
                st.error("Both current and new names are required.")
            else:
                path = resolve(fname.strip())
                new_path = resolve(new_name.strip())
                if not path.exists():
                    st.error(f"⚠️ **{fname}** does not exist.")
                elif new_path.exists():
                    st.error(f"⚠️ **{new_name}** already exists.")
                else:
                    try:
                        path.rename(new_path)
                        st.success(f"✅ Renamed **{path.name}** → **{new_path.name}**")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    elif action == "Append content":
        data = st.text_area("Content to append", height=140, key="u_append")
        if st.button("Append to File", key="append_btn"):
            if not fname.strip():
                st.error("Please enter a file name.")
            else:
                path = resolve(fname.strip())
                if not path.exists():
                    st.error(f"⚠️ **{fname}** does not exist.")
                else:
                    try:
                        with open(path, "a", encoding="utf-8") as f:
                            f.write("\n" + data)
                        st.success(f"✅ Content appended to **{path.name}**")
                    except Exception as e:
                        st.error(f"Error: {e}")

    else:  # Overwrite
        data = st.text_area("New content (replaces everything)", height=140, key="u_overwrite")
        if st.button("Overwrite File", key="overwrite_btn"):
            if not fname.strip():
                st.error("Please enter a file name.")
            else:
                path = resolve(fname.strip())
                if not path.exists():
                    st.error(f"⚠️ **{fname}** does not exist.")
                else:
                    try:
                        path.write_text(data, encoding="utf-8")
                        st.success(f"✅ **{path.name}** overwritten successfully.")
                    except Exception as e:
                        st.error(f"Error: {e}")


# ── DELETE ────────────────────────────────────────────────────────────────────
elif selected == "delete":
    st.markdown("""<div class="panel">
        <div class="panel-title">Delete a file</div>
        <div class="panel-desc">Permanently removes the file from disk. This action cannot be undone.</div>
    </div>""", unsafe_allow_html=True)

    fname = st.text_input("File name", placeholder="e.g. notes.txt", key="d_name")

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if st.button("Delete File", key="delete_btn"):
        if not fname.strip():
            st.error("Please enter a file name.")
        else:
            path = resolve(fname.strip())
            if not path.exists():
                st.error(f"⚠️ **{fname}** does not exist.")
            else:
                st.session_state.confirm_delete = True
                st.session_state.delete_target = str(path)

    if st.session_state.get("confirm_delete"):
        target = Path(st.session_state.delete_target)
        st.warning(f"⚠️ Are you sure you want to permanently delete **{target.name}**?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, delete it", key="confirm_yes"):
                try:
                    target.unlink()
                    st.success(f"🗑️ **{target.name}** deleted.")
                    st.session_state.confirm_delete = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        with c2:
            if st.button("Cancel", key="confirm_no"):
                st.session_state.confirm_delete = False
                st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;font-size:11px;color:#334155;letter-spacing:0.05em'>"
    "FileVault · Built with Python &amp; Streamlit"
    "</div>",
    unsafe_allow_html=True
)
