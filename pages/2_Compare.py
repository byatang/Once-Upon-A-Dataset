# =============================================================================
# pages/2_Compare.py — Compare Characters
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import COLORS, inject_css, load_all_data, base_layout, CHARACTERS

st.set_page_config(
    page_title="Once Upon a Dataset — Compare",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

st.sidebar.markdown(f"""
<div style="padding:1.5rem 0.5rem 1rem 0.5rem;">
    <div style="font-size:0.65rem;letter-spacing:0.3rem;color:{COLORS['gold']};text-transform:uppercase;margin-bottom:0.5rem;">Once Upon a Dataset</div>
    <div style="font-family:'Playfair Display',serif;font-size:1.1rem;color:{COLORS['text']};">HMDA 2007–2017</div>
</div>
<hr style="border:none;border-top:1px solid {COLORS['border']};margin:0 0 1rem 0;">
<div style="font-size:0.8rem;color:{COLORS['muted']};line-height:1.8;padding:0 0.5rem;">
    📊 Overview<br>
    <span style="opacity:0.6;">Market-level data &amp; context</span><br><br>
    📖 Stories<br>
    <span style="opacity:0.6;">Five characters, five decades</span><br><br>
    ⚖️ <strong style="color:{COLORS['text']}">Compare</strong><br>
    <span style="opacity:0.6;">Side-by-side story arcs</span><br><br>
    🔍 Explore<br>
    <span style="opacity:0.6;">Raw data &amp; filters</span>
</div>
""", unsafe_allow_html=True)

with st.spinner('Loading 64 million stories…'):
    volume, purpose, ltype, race, sex, income, loan_race, state_year, va, explorer = load_all_data()

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <div class="page-eyebrow">Once Upon a Dataset · Compare · HMDA 2007–2017</div>
    <div class="page-title">The Same Crisis.<br>Two Completely Different Decades.</div>
    <div class="page-subtitle">
        Select any two characters and watch their stories diverge across the same
        ten years of data. The market didn't treat everyone equally.
    </div>
</div>
""", unsafe_allow_html=True)

# ── SELECTORS ─────────────────────────────────────────────────────────────────
char_names = {k: f"{v['emoji']} {v['name']} — {v['role']}" for k, v in CHARACTERS.items()}

col1, col2 = st.columns(2)
with col1:
    c1 = st.selectbox("First character", options=list(char_names.keys()),
                      format_func=lambda x: char_names[x], index=0, key="cmp1")
with col2:
    c2 = st.selectbox("Second character", options=list(char_names.keys()),
                      format_func=lambda x: char_names[x], index=1, key="cmp2")

if c1 == c2:
    st.warning("Pick two different characters to compare.")
    st.stop()

ch1 = CHARACTERS[c1]
ch2 = CHARACTERS[c2]

# ── STAT CARDS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin:1.5rem 0 2.5rem 0;">
    <div style="background:{COLORS['card']};border:1px solid {ch1['color']};border-radius:14px;padding:2rem;text-align:center;">
        <div style="font-size:3rem;margin-bottom:0.5rem">{ch1['emoji']}</div>
        <div style="color:{ch1['color']};font-weight:600;font-size:1rem">{ch1['name']}</div>
        <div style="color:{COLORS['muted']};font-size:0.85rem;margin-bottom:1rem">{ch1['role']}</div>
        <div style="font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:700;color:{ch1['color']}">{ch1['key_stat']}</div>
        <div style="color:{COLORS['muted']};font-size:0.8rem;margin-top:0.3rem">{ch1['key_label']}</div>
        <div style="margin-top:1rem;font-size:0.82rem;color:{COLORS['muted']};line-height:1.6;font-style:italic">"{ch1['tagline']}"</div>
    </div>
    <div style="background:{COLORS['card']};border:1px solid {ch2['color']};border-radius:14px;padding:2rem;text-align:center;">
        <div style="font-size:3rem;margin-bottom:0.5rem">{ch2['emoji']}</div>
        <div style="color:{ch2['color']};font-weight:600;font-size:1rem">{ch2['name']}</div>
        <div style="color:{COLORS['muted']};font-size:0.85rem;margin-bottom:1rem">{ch2['role']}</div>
        <div style="font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:700;color:{ch2['color']}">{ch2['key_stat']}</div>
        <div style="color:{COLORS['muted']};font-size:0.8rem;margin-top:0.3rem">{ch2['key_label']}</div>
        <div style="margin-top:1rem;font-size:0.82rem;color:{COLORS['muted']};line-height:1.6;font-style:italic">"{ch2['tagline']}"</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── SHARED VOLUME CHART ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Shared Context</div>
<div class="section-title">The Same Market — Different Realities</div>
<div class="section-body">
    Both characters lived through the same national mortgage market. But volume
    statistics tell very different stories depending on who you are.
</div>
""", unsafe_allow_html=True)

fig_vol = go.Figure()
fig_vol.add_trace(go.Bar(
    x=volume['as_of_year'], y=volume['total'], name='All Loans',
    marker_color=[ch1['color'] if y <= 2009 else ch2['color'] if y >= 2014 else COLORS['muted']
                  for y in volume['as_of_year']],
    hovertemplate='<b>%{x}</b><br>%{y:,.0f} loans<extra></extra>'
))
fig_vol.add_annotation(
    x=2009, y=volume[volume['as_of_year'] == 2009]['total'].values[0],
    text=f"{ch1['name']}'s hardest year",
    arrowcolor=ch1['color'], bordercolor=ch1['color'],
    font=dict(color=ch1['color'], size=10),
    ax=0, ay=-60, **{'showarrow': True, 'arrowhead': 2, 'arrowwidth': 1.5,
                     'bgcolor': COLORS['background'], 'borderwidth': 1})
fig_vol.add_annotation(
    x=2014, y=volume[volume['as_of_year'] == 2014]['total'].values[0],
    text=f"{ch2['name']}'s turning point",
    arrowcolor=ch2['color'], bordercolor=ch2['color'],
    font=dict(color=ch2['color'], size=10),
    ax=0, ay=-60, **{'showarrow': True, 'arrowhead': 2, 'arrowwidth': 1.5,
                     'bgcolor': COLORS['background'], 'borderwidth': 1})

lv = base_layout(height=400)
lv['showlegend']          = False
lv['yaxis']['tickformat'] = ','
lv['yaxis']['title']      = dict(text='Total mortgages originated', font=dict(color=COLORS['muted'], size=12))
fig_vol.update_layout(**lv)
st.plotly_chart(fig_vol, width='stretch')

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── SIDE BY SIDE BEATS ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="section-eyebrow">Story Comparison</div>
<div class="section-title">{ch1['name']} vs {ch2['name']}, Year by Year</div>
<div class="section-body">
    The same years. Completely different experiences. Color indicates tone:
    <span style="color:{COLORS['green']}">■ hopeful</span>&nbsp;
    <span style="color:{COLORS['blue']}">■ neutral</span>&nbsp;
    <span style="color:{COLORS['gold']}">■ warning</span>&nbsp;
    <span style="color:{COLORS['red']}">■ difficult</span>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns(2)
with col_h1:
    st.markdown(f"""<div style="background:{COLORS['card']};border:1px solid {ch1['color']};border-radius:10px;
                padding:1rem 1.5rem;text-align:center;margin-bottom:1rem;">
        <span style="font-size:1.5rem">{ch1['emoji']}</span>
        <span style="color:{ch1['color']};font-weight:600;margin-left:0.5rem">{ch1['name']}</span>
    </div>""", unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""<div style="background:{COLORS['card']};border:1px solid {ch2['color']};border-radius:10px;
                padding:1rem 1.5rem;text-align:center;margin-bottom:1rem;">
        <span style="font-size:1.5rem">{ch2['emoji']}</span>
        <span style="color:{ch2['color']};font-weight:600;margin-left:0.5rem">{ch2['name']}</span>
    </div>""", unsafe_allow_html=True)

tone_colors = {'hopeful': COLORS['green'], 'neutral': COLORS['blue'],
               'warning': COLORS['gold'],  'bad':     COLORS['red']}
tone_icons  = {'hopeful': '✅', 'neutral': '➡️', 'warning': '⚠️', 'bad': '🔴'}

years  = sorted(set([b['year'] for b in ch1['beats']] + [b['year'] for b in ch2['beats']]))
b1_map = {b['year']: b for b in ch1['beats']}
b2_map = {b['year']: b for b in ch2['beats']}

for yr in years:
    col_a, col_b = st.columns(2)
    with col_a:
        if yr in b1_map:
            b  = b1_map[yr]
            tc = tone_colors[b['tone']]
            st.markdown(f"""<div style="padding:1rem 1.2rem;background:{COLORS['card']};border-radius:10px;
                        border-left:3px solid {tc};margin-bottom:0.5rem;">
                <div style="color:{tc};font-weight:600;font-size:0.9rem">{tone_icons[b['tone']]} {yr} — {b['title']}</div>
                <div style="color:{COLORS['muted']};font-size:0.82rem;margin-top:0.3rem;line-height:1.6">{b['body']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="padding:1rem 1.2rem;background:rgba(255,255,255,0.02);border-radius:10px;
                        border:1px dashed rgba(255,255,255,0.06);margin-bottom:0.5rem;opacity:0.4;">
                <div style="color:{COLORS['muted']};font-size:0.8rem;font-style:italic">{yr} — no beat for {ch1['name']}</div>
            </div>""", unsafe_allow_html=True)
    with col_b:
        if yr in b2_map:
            b  = b2_map[yr]
            tc = tone_colors[b['tone']]
            st.markdown(f"""<div style="padding:1rem 1.2rem;background:{COLORS['card']};border-radius:10px;
                        border-left:3px solid {tc};margin-bottom:0.5rem;">
                <div style="color:{tc};font-weight:600;font-size:0.9rem">{tone_icons[b['tone']]} {yr} — {b['title']}</div>
                <div style="color:{COLORS['muted']};font-size:0.82rem;margin-top:0.3rem;line-height:1.6">{b['body']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="padding:1rem 1.2rem;background:rgba(255,255,255,0.02);border-radius:10px;
                        border:1px dashed rgba(255,255,255,0.06);margin-bottom:0.5rem;opacity:0.4;">
                <div style="color:{COLORS['muted']};font-size:0.8rem;font-style:italic">{yr} — no beat for {ch2['name']}</div>
            </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── TAKEAWAYS ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Conclusion</div>
<div class="section-title">What the Data Says About Each of Them</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"""<div class="insight-box" style="border-color:{ch1['color']}">
        <strong style="color:{ch1['color']}">{ch1['name']}'s Takeaway</strong><br><br>
        {ch1['takeaway']}
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""<div class="insight-box" style="border-color:{ch2['color']}">
        <strong style="color:{ch2['color']}">{ch2['name']}'s Takeaway</strong><br><br>
        {ch2['takeaway']}
    </div>""", unsafe_allow_html=True)
