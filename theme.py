"""GovernAI look and feel: dark "space" theme, plus HTML pieces Streamlit can't draw natively.

Everything here is plain CSS/HTML/SVG. No web fonts or CDNs are loaded, so the app
still looks right with Wi-Fi off.
"""
import html
import math

import streamlit as st

from scoring import LABELS, PASS_LINE

CSS = """
:root {
  --bg: #07060f; --line: rgba(255,255,255,.09); --text: #eeeaff;
  --muted: #9c98bb; --muted2: #6f6b90; --cyan: #8ff3e6;
  --good: #3ee89a; --caution: #f5b74e; --bad: #ff5f7e;
  --serif: "Instrument Serif", "Iowan Old Style", Georgia, "Times New Roman", serif;
  --sans: "Space Grotesk", Inter, system-ui, -apple-system, "Segoe UI", sans-serif;
}
html, body, .stApp {
  background: var(--bg) !important; color: var(--text); font-family: var(--sans);
}
.stApp {
  background:
    radial-gradient(1100px 700px at 88% -12%, rgba(110,70,220,.34), transparent 60%),
    radial-gradient(900px 600px at -8% 112%, rgba(30,120,140,.2), transparent 60%),
    var(--bg) !important;
}
/* faint starfield */
.stApp::before {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image:
    radial-gradient(1px 1px at 12% 18%, #fff9 50%, transparent 51%),
    radial-gradient(1px 1px at 64% 42%, #fff6 50%, transparent 51%),
    radial-gradient(1.5px 1.5px at 33% 77%, #fff7 50%, transparent 51%),
    radial-gradient(1px 1px at 85% 63%, #fff5 50%, transparent 51%),
    radial-gradient(1px 1px at 47% 9%, #fff6 50%, transparent 51%),
    radial-gradient(1px 1px at 92% 90%, #fff5 50%, transparent 51%),
    radial-gradient(1px 1px at 24% 52%, #fff5 50%, transparent 51%);
  background-size: 460px 460px;
}
header[data-testid="stHeader"] { background: transparent !important; pointer-events: none; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stAppDeployButton"], .stDeployButton {
  visibility: hidden; height: 0;
}
.block-container { max-width: 1180px; padding-top: 1.2rem; padding-bottom: 3rem; position: relative; z-index: 1; }

/* cards: every st.container(border=True) becomes a glass panel */
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(17,15,32,.8) !important; border: 1px solid var(--line) !important;
  border-radius: 24px !important; padding: 1.4rem 1.5rem !important;
  backdrop-filter: blur(14px); box-shadow: 0 30px 80px -40px rgba(0,0,0,.9);
}

/* top bar */
.gai-brand { display: flex; align-items: center; gap: .7rem; font-weight: 600; font-size: 1.15rem; height: 44px; }
.gai-orb {
  width: 34px; height: 34px; border-radius: 50%; position: relative; flex: none;
  background: radial-gradient(circle at 35% 35%, #fff 0 8%, #c9b8ff 22%, #7d5cf0 58%, #2b1d66 100%);
  box-shadow: 0 0 22px rgba(164,139,255,.6);
}
.gai-orb::after { content: ""; position: absolute; inset: -6px; border-radius: 50%; border: 1px solid rgba(255,255,255,.16); }
.gai-status {
  display: flex; justify-content: flex-end; align-items: center; gap: .5rem; height: 44px;
  color: var(--muted); font-size: .85rem; white-space: nowrap;
}
.gai-pill {
  display: inline-flex; align-items: center; gap: .5rem; padding: .45rem .9rem;
  border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,.03);
}
.gai-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; background: var(--caution); box-shadow: 0 0 10px currentColor; flex: none; }
.gai-dot.ok { background: var(--good); color: var(--good); }

/* segmented controls (nav, chips, mode) as pills */
div[data-testid="stSegmentedControl"] button,
div[data-testid="stButtonGroup"] button {
  border-radius: 999px !important; border: 1px solid transparent !important;
  background: transparent !important; color: var(--muted) !important; font-family: var(--sans) !important;
}
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stButtonGroup"] button[aria-checked="true"] {
  background: rgba(255,255,255,.1) !important; color: var(--text) !important; border-color: var(--line) !important;
}
div[data-testid="stSegmentedControl"] > div,
div[data-testid="stButtonGroup"] > div { gap: .35rem; }

/* buttons */
.stButton button {
  border-radius: 999px !important; border: 1px solid var(--line) !important;
  background: rgba(255,255,255,.04) !important; color: var(--text) !important;
  font-family: var(--sans) !important; padding: .55rem 1.1rem !important;
}
.stButton button:hover { border-color: rgba(143,243,230,.5) !important; }
button[data-testid="stBaseButton-primary"], button[kind="primary"] {
  background: linear-gradient(90deg, #ece7ff, #b9f3ea) !important; color: #120f26 !important;
  border: none !important; font-weight: 600 !important; box-shadow: 0 0 28px rgba(143,243,230,.22) !important;
}

/* inputs */
div[data-baseweb="textarea"], div[data-baseweb="input"], div[data-baseweb="select"] > div {
  background: rgba(8,7,18,.75) !important; border: 1px solid var(--line) !important; border-radius: 14px !important;
}
textarea, input { color: var(--text) !important; font-family: var(--sans) !important; }
[data-testid="stWidgetLabel"] p, label { color: var(--muted) !important; }
div[data-testid="stCaptionContainer"], .stCaption { color: var(--muted2) !important; }
div[data-testid="stExpander"] details { border: 1px solid var(--line) !important; border-radius: 14px !important; background: rgba(8,7,18,.5); }

/* hero */
h1.gai-hero {
  font-family: var(--serif) !important; font-weight: 400 !important; font-size: clamp(2.8rem, 4.3vw, 4.5rem) !important;
  line-height: .98 !important; letter-spacing: -.01em; margin: .6rem 0 1.2rem !important; color: #f2f0ff !important;
}
.gai-hero em {
  font-style: italic; background: linear-gradient(90deg, #d7ecff, #b9f3ea 45%, #c9b9ff);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.gai-lead { color: var(--muted); font-size: 1.05rem; line-height: 1.6; max-width: 36rem; margin: 0 0 1.4rem; }
.gai-privacy { color: var(--muted2); font-size: .88rem; display: flex; gap: .55rem; align-items: center; margin-top: .9rem; }
.gai-dial svg { width: 100%; max-width: 540px; height: auto; display: block; margin: 0 auto; }

/* section headings and steps */
.gai-title { font-family: var(--serif); font-size: 2.1rem; line-height: 1.1; margin: 0; color: #f2f0ff; }
.gai-sub { color: var(--muted); margin: .3rem 0 .4rem; }
.gai-step { display: flex; align-items: center; gap: .6rem; font-weight: 500; margin: 1.1rem 0 .45rem; color: var(--text); }
.gai-step span {
  width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; flex: none;
  font-size: .72rem; color: var(--cyan); background: rgba(143,243,230,.1); border: 1px solid rgba(143,243,230,.35);
}

/* verdict + scorecard */
.gai-head { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; margin-bottom: .6rem; }
.gai-model { font-size: 1.4rem; font-weight: 600; margin: .15rem 0; }
.gai-model small, .muted2 { color: var(--muted2); font-weight: 400; }
.gai-verdict { border-radius: 16px; padding: .7rem 1rem; text-align: right; min-width: 150px; border: 1px solid; flex: none; }
.gai-verdict.caution { color: var(--caution); border-color: rgba(245,183,78,.45); background: rgba(245,183,78,.07); }
.gai-verdict.safe { color: var(--good); border-color: rgba(62,232,154,.45); background: rgba(62,232,154,.07); }
.gai-verdict.unsafe { color: var(--bad); border-color: rgba(255,95,126,.45); background: rgba(255,95,126,.07); }
.gai-vlabel { font-size: .8rem; }
.gai-vpct { font-size: 2.2rem; font-weight: 600; line-height: 1.1; }
.gai-row { margin: .95rem 0 .25rem; }
.gai-row-top { display: flex; justify-content: space-between; font-size: .95rem; }
.gai-pct { font-weight: 600; white-space: nowrap; }
.gai-track { position: relative; height: 6px; border-radius: 6px; background: rgba(255,255,255,.07); margin: .5rem 0; }
.gai-fill { height: 100%; border-radius: 6px; }
.gai-knob {
  position: absolute; top: 50%; width: 14px; height: 14px; border-radius: 50%; background: #fff;
  transform: translate(-50%, -50%); box-shadow: 0 0 12px rgba(255,255,255,.7);
}
.good { color: var(--good); }
.caution { color: var(--caution); }
.bad { color: var(--bad); }
.gai-fill.good { background: linear-gradient(90deg, #2fbf85, #3ee89a); }
.gai-fill.caution { background: linear-gradient(90deg, #d98e2b, #f5b74e); }
.gai-fill.bad { background: linear-gradient(90deg, #e03a62, #ff7d9a); }
.gai-note { font-size: .85rem; }
.gai-worst {
  margin-top: 1.1rem; border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1rem;
  background: rgba(0,0,0,.25); color: var(--muted); line-height: 1.5;
}
.gai-worst b { color: var(--text); font-weight: 600; }

/* single verdict (This response) */
.gai-chip { display: inline-block; padding: .22rem .7rem; border-radius: 999px; font-size: .85rem; font-weight: 600; }
.gai-chip.pass { color: var(--good); background: rgba(62,232,154,.12); border: 1px solid rgba(62,232,154,.35); }
.gai-chip.fail { color: var(--bad); background: rgba(255,95,126,.12); border: 1px solid rgba(255,95,126,.4); }
.gai-sev { color: var(--caution); font-size: .85rem; margin-left: .4rem; }
.gai-result { border: 1px solid var(--line); border-radius: 16px; padding: 1rem 1.1rem; margin-top: .8rem; }
.gai-result.fail { border-color: rgba(255,95,126,.4); background: rgba(255,95,126,.05); }
.gai-result.pass { border-color: rgba(62,232,154,.3); background: rgba(62,232,154,.04); }
.gai-cat { font-weight: 600; margin-left: .5rem; }
.gai-reason { margin: .6rem 0 .3rem; line-height: 1.55; }
.gai-empty { color: var(--muted); text-align: center; padding: 1.8rem 0 .6rem; }
.gai-star { display: flex; justify-content: center; margin: .4rem 0 .8rem; }
.gai-star .gai-orb { width: 42px; height: 42px; }

/* sample banner, compare VS, footer */
.gai-banner {
  border: 1px solid rgba(245,183,78,.35); background: rgba(245,183,78,.06); border-radius: 16px;
  padding: .9rem 1.1rem; margin-bottom: 1.2rem; color: var(--muted); line-height: 1.5;
}
.gai-banner b { color: var(--caution); font-weight: 600; }
.gai-vs { display: flex; flex-direction: column; align-items: center; gap: .6rem; padding-top: 3.5rem; text-align: center; }
.gai-vs-orb {
  width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
  border: 1px solid var(--line); font-family: var(--serif); font-style: italic; font-size: 1.5rem;
  background: radial-gradient(circle, #2c2352, #0b0a18); box-shadow: 0 0 30px rgba(164,139,255,.35);
}
.gai-foot { text-align: center; color: var(--muted2); font-size: .85rem; margin-top: 2rem; }
.muted { color: var(--muted); }
.small { font-size: .85rem; }

@media (max-width: 760px) {
  .gai-hero { font-size: 2.6rem; }
  .gai-status { justify-content: flex-start; height: auto; }
  .gai-verdict { min-width: 0; }
}
"""

VERDICT_CLASS = {"SAFE TO USE": "safe", "USE WITH CAUTION": "caution", "NOT SAFE": "unsafe"}
VERDICT_LABEL = {"SAFE TO USE": "Safe to use", "USE WITH CAUTION": "Use with caution", "NOT SAFE": "Not safe"}


def esc(text) -> str:
    return html.escape(str(text))


def inject_css() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def brand_html() -> str:
    return '<div class="gai-brand"><span class="gai-orb"></span><span>GovernAI</span></div>'


def status_html(state: str, text: str) -> str:
    dot = "ok" if state == "ready" else ""
    return f'<div class="gai-status"><span class="gai-pill"><span class="gai-dot {dot}"></span>{esc(text)}</span></div>'


def tone(pct: int) -> str:
    if pct >= PASS_LINE:
        return "good"
    if pct >= 60:
        return "caution"
    return "bad"


def hero_title_html() -> str:
    return '<h1 class="gai-hero">Is this AI model<br><em>safe for you?</em></h1>'


def section_html(title: str, sub: str = "") -> str:
    sub_html = f'<div class="gai-sub">{esc(sub)}</div>' if sub else ""
    return f'<div class="gai-title">{esc(title)}</div>{sub_html}'


def step_html(n: int, text: str) -> str:
    return f'<div class="gai-step"><span>{n:02d}</span>{esc(text)}</div>'


def scorecard_html(card: dict, model: str, profile: str) -> str:
    """Model scorecard: verdict box, one bar per category, and the worst failure."""
    v = card["verdict"]
    rows = []
    for label, d in sorted(card["details"].items(), key=lambda kv: (kv[1]["pct"], kv[0])):
        p = d["pct"]
        t = tone(p)
        mark = "✓" if p >= PASS_LINE else "✕"
        note = "" if p >= PASS_LINE else f'<div class="gai-note {t}">{esc(d["note"])}</div>'
        rows.append(
            '<div class="gai-row">'
            f'<div class="gai-row-top"><span>{esc(label)}</span><span class="gai-pct {t}">{p}% {mark}</span></div>'
            f'<div class="gai-track"><div class="gai-fill {t}" style="width:{p}%"></div>'
            f'<div class="gai-knob" style="left:{p}%"></div></div>{note}</div>'
        )

    worst_html = ""
    if card.get("worst"):
        w = card["worst"]
        short = w["prompt"].replace("\n", " ")
        short = short[:90] + ("…" if len(short) > 90 else "")
        worst_html = (f'<div class="gai-worst">Worst failure: <b>{esc(LABELS.get(w["category"], w["category"]))}</b>'
                      f' — “{esc(short)}”</div>')

    return (
        '<div class="gai-head"><div>'
        '<div class="muted small">Model scorecard</div>'
        f'<div class="gai-model">{esc(model)} <small>· {esc(profile)}</small></div>'
        f'<div class="muted small">Based on {card["count"]} evaluated responses</div></div>'
        f'<div class="gai-verdict {VERDICT_CLASS[v]}"><div class="gai-vlabel">{VERDICT_LABEL[v]}</div>'
        f'<div class="gai-vpct">{card["overall"]}%</div></div></div>'
        + "".join(rows) + worst_html
    )


def judgment_html(j: dict) -> str:
    """'This response' verdict for one judged reply."""
    ok = bool(j["pass"])
    cat = LABELS.get(j["category"], j["category"])
    sev = "" if ok else f'<span class="gai-sev">· {esc(j["severity"])} severity</span>'
    return (
        f'<div class="gai-result {"pass" if ok else "fail"}">'
        f'<span class="gai-chip {"pass" if ok else "fail"}">{"✓ Pass" if ok else "✕ Fail"}</span>'
        f'<span class="gai-cat">{esc(cat)}</span>{sev}'
        f'<div class="muted small" style="margin-top:.45rem">Expected {esc(j["expected"])} · the model {esc(j["actual"].lower())}</div>'
        f'<div class="gai-reason">{esc(j["reason"])}</div></div>'
    )


def dial_svg() -> str:
    """Decorative dial for the hero: a sweep pointing at one rule."""
    cx = cy = 260
    R = 250
    ticks = []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        major = i % 5 == 0
        r1 = R - (22 if major else 12)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        x2, y2 = cx + (R - 4) * math.cos(a), cy + (R - 4) * math.sin(a)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{"#cfc6ff" if major else "#6f6b90"}" stroke-width="{1.6 if major else 1}" opacity="{.8 if major else .45}"/>')
    dots = []
    for deg, r in ((-90, 218), (-62, 224), (-150, 214), (-200, 220), (10, 218), (120, 222), (168, 220)):
        a = math.radians(deg)
        dots.append(f'<circle cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" r="4" fill="#f3f0ff" opacity=".85"/>')
    a0, a1, rr = math.radians(-64), math.radians(-36), R - 34
    p0 = (cx + rr * math.cos(a0), cy + rr * math.sin(a0))
    p1 = (cx + rr * math.cos(a1), cy + rr * math.sin(a1))
    wedge = (f'M{cx},{cy} L{p0[0]:.1f},{p0[1]:.1f} A{rr},{rr} 0 0 1 {p1[0]:.1f},{p1[1]:.1f} Z')
    return (
        '<div class="gai-dial"><svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<radialGradient id="dialBg" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#4a3a8f" stop-opacity=".75"/>'
        '<stop offset="60%" stop-color="#1b1640" stop-opacity=".85"/>'
        '<stop offset="100%" stop-color="#0a0918" stop-opacity=".95"/></radialGradient>'
        '<linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>'
        '<stop offset="100%" stop-color="#e9fffb" stop-opacity=".9"/></linearGradient>'
        '<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#8ff3e6" stop-opacity=".7"/>'
        '<stop offset="50%" stop-color="#a48bff" stop-opacity=".25"/>'
        '<stop offset="100%" stop-color="#8ff3e6" stop-opacity=".5"/></linearGradient>'
        '</defs>'
        f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#dialBg)" stroke="url(#rim)" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{R - 60}" fill="none" stroke="#ffffff" stroke-opacity=".06"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{R - 110}" fill="none" stroke="#ffffff" stroke-opacity=".05"/>'
        + "".join(ticks) + "".join(dots) +
        f'<path d="{wedge}" fill="url(#sweep)" opacity=".85"/>'
        '<text x="260" y="236" text-anchor="middle" fill="#9c98bb" font-size="15" font-family="Space Grotesk, system-ui, sans-serif">A good model should</text>'
        '<text x="260" y="284" text-anchor="middle" fill="#f2f0ff" font-size="44" font-family="Instrument Serif, Georgia, serif">Exam cheating</text>'
        '<text x="260" y="316" text-anchor="middle" fill="#9c98bb" font-size="15" font-family="Space Grotesk, system-ui, sans-serif">Refuse to answer during a live exam.</text>'
        '</svg></div>'
    )
