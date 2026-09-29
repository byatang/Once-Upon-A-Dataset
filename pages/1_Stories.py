# =============================================================================
# pages/1_Stories.py — Character Stories
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import COLORS, inject_css, load_all_data, base_layout, ANNO_STYLE, CHARACTERS, CHARACTER_MAP_CONFIG

st.set_page_config(
    page_title="Once Upon a Dataset — Stories",
    page_icon="📖",
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
    📖 <strong style="color:{COLORS['text']}">Stories</strong><br>
    <span style="opacity:0.6;">Five characters, five decades</span><br><br>
    ⚖️ Compare<br>
    <span style="opacity:0.6;">Side-by-side story arcs</span><br><br>
    🔍 Explore<br>
    <span style="opacity:0.6;">Raw data &amp; filters</span>
</div>
""", unsafe_allow_html=True)

with st.spinner('Loading 64 million stories…'):
    volume, purpose, ltype, race, sex, income, loan_race, state_year, va, explorer = load_all_data()

if 'character' not in st.session_state:
    st.session_state.character = None

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <div class="page-eyebrow">Once Upon a Dataset · Stories · HMDA 2007–2017</div>
    <div class="page-title">The Decade the American<br>Dream Almost Died</div>
    <div class="page-subtitle">
        64 million mortgages. 10 years. One crisis.<br>
        But the story depends on <em>who you are</em>.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="kpi-strip">
    <div class="kpi-cell"><div class="kpi-number c-gold">64M</div><div class="kpi-label">Mortgages Funded</div></div>
    <div class="kpi-cell"><div class="kpi-number c-red">−24%</div><div class="kpi-label">Crash in 2008</div></div>
    <div class="kpi-cell"><div class="kpi-number c-green">2014</div><div class="kpi-label">Real Recovery Year</div></div>
    <div class="kpi-cell"><div class="kpi-number c-blue">10</div><div class="kpi-label">Years of Data</div></div>
    <div class="kpi-cell"><div class="kpi-number c-gold">5</div><div class="kpi-label">Stories to Tell</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── CHARACTER CARDS ───────────────────────────────────────────────────────────
st.markdown('<div class="choose-prompt">Once upon a dataset… whose story do you want to follow?</div>', unsafe_allow_html=True)

row1 = list(CHARACTERS.items())[:3]
row2 = list(CHARACTERS.items())[3:]

def char_button(key, char):
    selected = st.session_state.character == key
    border   = f"2px solid {char['color']}" if selected else "1px solid rgba(255,255,255,0.08)"
    bg       = "#1a1a2e" if selected else COLORS['card']
    st.markdown(f"""
    <div style="background:{bg};border:{border};border-radius:16px;
                padding:2rem 1.5rem;text-align:center;min-height:200px;">
        <div style="font-size:2.8rem">{char['emoji']}</div>
        <div style="font-size:1rem;font-weight:600;color:{COLORS['text']};margin:0.5rem 0">{char['name']}</div>
        <div style="font-size:0.8rem;color:{char['color']};margin-bottom:0.5rem">{char['role']}</div>
        <div style="font-size:0.78rem;color:{COLORS['muted']};line-height:1.5">{char['tagline']}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"Follow {char['name']} →", key=f"btn_{key}"):
        st.session_state.character = key
        st.rerun()

cols1 = st.columns(3)
for col, (key, char) in zip(cols1, row1):
    with col:
        char_button(key, char)

st.markdown("<br>", unsafe_allow_html=True)
cols2 = st.columns([1, 3, 3, 1])
for col, (key, char) in zip(cols2[1:3], row2):
    with col:
        char_button(key, char)

# ── STORY CONTENT ─────────────────────────────────────────────────────────────
if st.session_state.character:
    char    = CHARACTERS[st.session_state.character]
    ckey    = st.session_state.character
    map_cfg = CHARACTER_MAP_CONFIG[ckey]

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:1.5rem;margin-bottom:2rem;">
        <div style="font-size:4rem">{char['emoji']}</div>
        <div>
            <div style="font-size:0.75rem;letter-spacing:0.3rem;color:{char['color']};text-transform:uppercase;">Your Story</div>
            <div style="font-family:'Playfair Display',serif;font-size:2.2rem;color:{COLORS['text']}">{char['name']}'s Story</div>
            <div style="color:{COLORS['muted']};font-size:1rem">{char['tagline']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:{COLORS['card']};border:1px solid {char['color']};
                border-radius:12px;padding:1.5rem 2rem;margin-bottom:2rem;">
        <span style="font-size:2.5rem;font-weight:bold;color:{char['color']}">{char['key_stat']}</span>
        <span style="color:{COLORS['muted']};margin-left:1rem;font-size:1rem">{char['key_label']}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Filter the charts by year range:**")
    year_min, year_max = st.select_slider(
        "Year Range",
        options=sorted(volume['as_of_year'].unique()),
        value=(2007, 2017),
        key=f"yr_{ckey}",
        label_visibility='collapsed'
    )

    tone_colors = {'hopeful': COLORS['green'], 'neutral': COLORS['blue'],
                   'warning': COLORS['gold'],  'bad':     COLORS['red']}
    tone_icons  = {'hopeful': '✅', 'neutral': '➡️', 'warning': '⚠️', 'bad': '🔴'}

    st.markdown(f'<div class="act-label">The Journey</div><div class="act-title">{char["name"]}\'s Decade</div>', unsafe_allow_html=True)

    for beat in char['beats']:
        if year_min <= beat['year'] <= year_max:
            tc = tone_colors[beat['tone']]
            ti = tone_icons[beat['tone']]
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:1.5rem;margin:1rem 0;
                        padding:1.5rem;background:{COLORS['card']};border-radius:12px;
                        border-left:4px solid {tc};">
                <div style="min-width:70px;text-align:center;">
                    <div style="font-size:1.5rem;font-weight:bold;font-family:'Playfair Display',serif;color:{tc}">{beat['year']}</div>
                    <div style="font-size:1.2rem">{ti}</div>
                </div>
                <div>
                    <div style="font-size:1rem;font-weight:600;color:{COLORS['text']};margin-bottom:0.4rem">{beat['title']}</div>
                    <div style="font-size:0.9rem;color:{COLORS['muted']};line-height:1.7">{beat['body']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="act-label">The Data Behind {char["name"]}\'s Story</div><div class="act-title">What the Numbers Show</div>', unsafe_allow_html=True)

    focus    = char['chart_focus']
    purp_f   = purpose[(purpose['as_of_year'] >= year_min) & (purpose['as_of_year'] <= year_max)]
    ltype_f  = ltype[(ltype['as_of_year'] >= year_min)     & (ltype['as_of_year'] <= year_max)]
    race_f   = race[(race['as_of_year'] >= year_min)       & (race['as_of_year'] <= year_max)]
    sex_f    = sex[(sex['as_of_year'] >= year_min)         & (sex['as_of_year'] <= year_max)]
    income_f = income[(income['as_of_year'] >= year_min)   & (income['as_of_year'] <= year_max)]
    lr_f     = loan_race[(loan_race['as_of_year'] >= year_min) & (loan_race['as_of_year'] <= year_max)]
    va_f     = va[(va['as_of_year'] >= year_min)           & (va['as_of_year'] <= year_max)]

    # ── RACE — Marcus ────────────────────────────────────────────────────────
    if focus == 'race':
        race_focus = race_f[race_f['applicant_race_name_1'].isin(
            ['White', 'Black or African American', 'Asian'])]
        rc = {'White': COLORS['blue'], 'Black or African American': COLORS['red'], 'Asian': COLORS['gold']}
        fig = go.Figure()
        for rname, rcolor in rc.items():
            rd = race_focus[race_focus['applicant_race_name_1'] == rname]
            fig.add_trace(go.Scatter(
                x=rd['as_of_year'], y=rd['pct'], name=rname, mode='lines+markers',
                line=dict(color=rcolor, width=4 if rname == 'Black or African American' else 2),
                marker=dict(size=9 if rname == 'Black or African American' else 6),
                hovertemplate=f'<b>{rname}</b><br>%{{x}}: %{{y:.1f}}%<extra></extra>'
            ))
        if year_min <= 2009 <= year_max:
            fig.add_annotation(x=2009, y=4.4, text="Nearly halved",
                arrowcolor=COLORS['red'], bordercolor=COLORS['red'],
                font=dict(color=COLORS['red'], size=11),
                ax=70, ay=30, **ANNO_STYLE)
        l = base_layout(height=420)
        l['yaxis']['ticksuffix'] = '%'
        fig.update_layout(**l)
        st.plotly_chart(fig, width='stretch')

        st.markdown('<div class="act-label" style="margin-top:2rem">Bonus Chart</div><div class="act-title">The Loan Size Gap</div><div class="act-body">Even among approved borrowers, loan sizes varied dramatically by demographic group — limiting which neighborhoods people could buy into.</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        for rname, rcolor in rc.items():
            rd = lr_f[lr_f['applicant_race_name_1'] == rname]
            fig2.add_trace(go.Scatter(
                x=rd['as_of_year'], y=rd['loan_amount_000s'], name=rname, mode='lines+markers',
                line=dict(color=rcolor, width=4 if rname == 'Black or African American' else 2),
                marker=dict(size=7),
                hovertemplate=f'<b>{rname}</b><br>%{{x}}: $%{{y}}K<extra></extra>'
            ))
        l2 = base_layout(height=380)
        l2['yaxis']['tickprefix'] = '$'
        l2['yaxis']['ticksuffix'] = 'K'
        fig2.update_layout(**l2)
        st.plotly_chart(fig2, width='stretch')

    # ── INCOME — David ───────────────────────────────────────────────────────
    elif focus == 'income':
        fig = go.Figure()
        bar_colors = [COLORS['red'] if y <= 2009 else COLORS['gold'] if y <= 2013 else COLORS['green']
                      for y in income_f['as_of_year']]
        fig.add_trace(go.Bar(
            x=income_f['as_of_year'], y=income_f['median_income'],
            marker_color=bar_colors,
            text=['$' + str(int(v)) + 'K' for v in income_f['median_income']],
            textposition='outside', textfont=dict(color=COLORS['text'], size=11),
            hovertemplate='<b>%{x}</b><br>Median income: $%{y}K<extra></extra>'
        ))
        if year_min <= 2007 <= year_max:
            fig.add_annotation(x=2007, y=71, text="$71K pre-crisis baseline",
                showarrow=False, font=dict(color=COLORS['muted'], size=10), yshift=10)
        if year_min <= 2016 <= year_max:
            fig.add_annotation(x=2016, y=84, text="+18% from baseline",
                arrowcolor=COLORS['gold'], bordercolor=COLORS['gold'],
                font=dict(color=COLORS['gold'], size=11),
                ax=-60, ay=-40, **ANNO_STYLE)
        l = base_layout(height=420)
        l['showlegend']           = False
        l['yaxis']['tickprefix']  = '$'
        l['yaxis']['ticksuffix']  = 'K'
        l['yaxis']['range']       = [60, 95]
        fig.update_layout(**l)
        st.plotly_chart(fig, width='stretch')

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=income_f['as_of_year'], y=income_f['median_loan'], mode='lines+markers',
            line=dict(color=COLORS['blue'], width=3), marker=dict(size=8),
            fill='tozeroy', fillcolor='rgba(69,123,157,0.15)',
            hovertemplate='<b>%{x}</b><br>Median loan: $%{y}K<extra></extra>'
        ))
        l2 = base_layout(height=380)
        l2['showlegend']          = False
        l2['yaxis']['tickprefix'] = '$'
        l2['yaxis']['ticksuffix'] = 'K'
        fig2.update_layout(**l2)
        st.plotly_chart(fig2, width='stretch')

    # ── VA — James ───────────────────────────────────────────────────────────
    elif focus == 'va':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=va_f['as_of_year'], y=va_f['pct'], mode='lines+markers',
            line=dict(color=COLORS['green'], width=4),
            marker=dict(size=10, color=COLORS['green']),
            fill='tozeroy', fillcolor='rgba(42,157,143,0.2)',
            hovertemplate='<b>%{x}</b><br>VA loans: %{y:.1f}%<extra></extra>'
        ))
        if year_min <= 2007 <= year_max:
            fig.add_annotation(x=2007, y=1.7, text="1.7% in 2007", showarrow=False,
                font=dict(color=COLORS['muted'], size=11), yshift=15)
        if year_min <= 2017 <= year_max:
            fig.add_annotation(x=2017, y=10.6, text="10.6% — 6x growth",
                arrowcolor=COLORS['green'], bordercolor=COLORS['green'],
                font=dict(color=COLORS['green'], size=11),
                ax=-100, ay=-40, **ANNO_STYLE)
        l = base_layout(height=420)
        l['showlegend']          = False
        l['yaxis']['ticksuffix'] = '%'
        fig.update_layout(**l)
        st.plotly_chart(fig, width='stretch')

        fig2 = go.Figure()
        lt_colors = {'Conventional': COLORS['blue'], 'FHA-insured': COLORS['gold'],
                     'VA-guaranteed': COLORS['green'], 'FSA/RHS-guaranteed': COLORS['red']}
        ltp = ltype_f.pivot(index='as_of_year', columns='loan_type_name', values='pct').fillna(0).reset_index()
        for lname, lcolor in lt_colors.items():
            if lname in ltp.columns:
                fig2.add_trace(go.Scatter(
                    x=ltp['as_of_year'], y=ltp[lname], name=lname, mode='lines+markers',
                    line=dict(color=lcolor, width=4 if lname == 'VA-guaranteed' else 2),
                    marker=dict(size=8 if lname == 'VA-guaranteed' else 5),
                    hovertemplate=f'<b>{lname}</b><br>%{{x}}: %{{y:.1f}}%<extra></extra>'
                ))
        l2 = base_layout(height=380)
        l2['yaxis']['ticksuffix'] = '%'
        fig2.update_layout(**l2)
        st.plotly_chart(fig2, width='stretch')

    # ── FHA — Maria ──────────────────────────────────────────────────────────
    elif focus == 'fha':
        fha_data = ltype_f[ltype_f['loan_type_name'] == 'FHA-insured']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=fha_data['as_of_year'], y=fha_data['pct'],
            marker_color=[COLORS['red'] if y == 2008 else COLORS['gold'] if y <= 2011 else COLORS['green']
                          for y in fha_data['as_of_year']],
            text=[f"{v:.1f}%" for v in fha_data['pct']],
            textposition='outside', textfont=dict(color=COLORS['text'], size=11),
            hovertemplate='<b>%{x}</b><br>FHA share: %{y:.1f}%<extra></extra>'
        ))
        if year_min <= 2008 <= year_max:
            fig.add_annotation(x=2008, y=22, text="Triples overnight",
                arrowcolor=COLORS['gold'], bordercolor=COLORS['gold'],
                font=dict(color=COLORS['gold'], size=11),
                ax=70, ay=-30, **ANNO_STYLE)
        l = base_layout(height=420)
        l['showlegend']          = False
        l['yaxis']['ticksuffix'] = '%'
        fig.update_layout(**l)
        st.plotly_chart(fig, width='stretch')

        st.markdown('<div class="act-label" style="margin-top:2rem">Bonus Chart</div><div class="act-title">Single-Income Households</div><div class="act-body">Female borrowers dropped from 30.7% in 2007 to 25.7% in 2011 and never fully recovered — showing single-income households faced disproportionate barriers post-crisis.</div>', unsafe_allow_html=True)
        female = sex_f[sex_f['applicant_sex_name'] == 'Female']
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=female['as_of_year'], y=female['pct'], mode='lines+markers',
            line=dict(color=COLORS['gold'], width=3), marker=dict(size=8),
            fill='tozeroy', fillcolor='rgba(244,162,97,0.15)',
            hovertemplate='<b>%{x}</b><br>Female borrowers: %{y:.1f}%<extra></extra>'
        ))
        if year_min <= 2007 <= year_max:
            fig2.add_annotation(x=2007, y=30.7, text="30.7% peak", showarrow=False,
                font=dict(color=COLORS['gold'], size=10), yshift=12)
        if year_min <= 2011 <= year_max:
            fig2.add_annotation(x=2011, y=25.7, text="Lowest point",
                arrowcolor=COLORS['red'], bordercolor=COLORS['red'],
                font=dict(color=COLORS['red'], size=10),
                ax=60, ay=20, **ANNO_STYLE)
        l2 = base_layout(height=380)
        l2['showlegend']          = False
        l2['yaxis']['ticksuffix'] = '%'
        l2['yaxis']['range']      = [20, 35]
        fig2.update_layout(**l2)
        st.plotly_chart(fig2, width='stretch')

    # ── REFI — Sandra ────────────────────────────────────────────────────────
    elif focus == 'refi':
        pp = purp_f.pivot(index='as_of_year', columns='loan_purpose_name', values='pct').fillna(0).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pp['as_of_year'], y=pp.get('Refinancing', pd.Series([0] * len(pp))),
            name='Refinancing', fill='tozeroy', mode='lines',
            line=dict(color=COLORS['red'], width=2), fillcolor='rgba(230,57,70,0.25)',
            hovertemplate='%{x}: <b>%{y:.1f}%</b> refinancing<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=pp['as_of_year'], y=pp.get('Home purchase', pd.Series([0] * len(pp))),
            name='Home Purchase', fill='tozeroy', mode='lines',
            line=dict(color=COLORS['green'], width=2), fillcolor='rgba(42,157,143,0.25)',
            hovertemplate='%{x}: <b>%{y:.1f}%</b> home purchase<extra></extra>'
        ))
        if year_min <= 2009 <= year_max:
            fig.add_annotation(x=2009, y=67, text="67% refinancing — the illusion peak",
                arrowcolor=COLORS['red'], bordercolor=COLORS['red'],
                font=dict(color=COLORS['red'], size=11),
                ax=90, ay=20, **ANNO_STYLE)
        if year_min <= 2014 <= year_max:
            fig.add_annotation(x=2014, y=57, text="Real recovery: buying > refinancing",
                arrowcolor=COLORS['green'], bordercolor=COLORS['green'],
                font=dict(color=COLORS['green'], size=11),
                ax=-110, ay=-40, **ANNO_STYLE)
        l = base_layout(height=420)
        l['yaxis']['ticksuffix'] = '%'
        fig.update_layout(**l)
        st.plotly_chart(fig, width='stretch')

    # ── CHARACTER MAP ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="act-label">Geographic View</div>
    <div class="act-title">Where Did {char['name']}'s Story Play Out?</div>
    <div class="act-body">
        The national story was never uniform. Use the slider to watch how mortgage
        activity shifted state by state — and see which states shaped {char['name']}'s
        experience most directly.
    </div>
    """, unsafe_allow_html=True)

    map_years = sorted(state_year[
        (state_year['as_of_year'] >= year_min) & (state_year['as_of_year'] <= year_max)
    ]['as_of_year'].unique())

    sel_yr   = st.select_slider('Select Year', options=map_years, value=map_years[0], key=f"map_{ckey}")
    map_data = state_year[state_year['as_of_year'] == sel_yr].copy()
    highlight_set = set(map_cfg['highlight_states'])

    fig_map = go.Figure()
    fig_map.add_trace(go.Choropleth(
        locations=map_data['state_abbr'], z=map_data['total'],
        locationmode='USA-states', colorscale=map_cfg['colorscale'],
        colorbar=dict(
            title=dict(text=map_cfg['colorbar_title'], font=dict(color=COLORS['text'])),
            tickfont=dict(color=COLORS['text']), bgcolor='rgba(0,0,0,0)'),
        hovertemplate='<b>%{location}</b><br>%{z:,.0f} loans<extra></extra>',
        marker_line_width=0.5, marker_line_color='rgba(255,255,255,0.12)',
    ))
    highlight_data = map_data[map_data['state_abbr'].isin(highlight_set)]
    if not highlight_data.empty:
        fig_map.add_trace(go.Choropleth(
            locations=highlight_data['state_abbr'], z=highlight_data['total'],
            locationmode='USA-states', colorscale=map_cfg['colorscale'],
            showscale=False,
            hovertemplate='<b>%{location}</b> ★<br>%{z:,.0f} loans<extra></extra>',
            marker_line_width=2.5, marker_line_color=char['color'],
            zmin=map_data['total'].min(), zmax=map_data['total'].max(),
        ))
    fig_map.update_layout(
        geo=dict(scope='usa', bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)',
                 landcolor='#1a1a2e', showlakes=True, showframe=False,
                 coastlinecolor='rgba(255,255,255,0.12)', showcoastlines=True),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color=COLORS['text']),
        margin=dict(t=30, b=0, l=0, r=0), height=480,
        title=dict(text=f'Mortgage Originations by State — {sel_yr}',
                   font=dict(size=17, color=COLORS['text']))
    )
    st.plotly_chart(fig_map, width='stretch')

    highlighted_in_year = map_data[map_data['state_abbr'].isin(highlight_set)]
    highlight_summary   = '  ·  '.join([
        f"<b>{r['state_abbr']}</b>: {r['total']:,.0f}"
        for _, r in highlighted_in_year.nlargest(5, 'total').iterrows()
    ])
    st.markdown(f"""<div class="insight-box" style="border-color:{char['color']}">
        <strong style="color:{char['color']}">★ {map_cfg['highlight_label']}:</strong><br>
        <span style="font-size:0.9rem">{highlight_summary}</span><br><br>
        {map_cfg['map_note']}
    </div>""", unsafe_allow_html=True)

    top5 = map_data.nlargest(5, 'total')[['state_abbr', 'total']]
    st.markdown(f"""<div class="insight-box">
        <strong>Top 5 states by volume in {sel_yr}:</strong>
        {'  ·  '.join([f"{r['state_abbr']}: {r['total']:,.0f}" for _, r in top5.iterrows()])}
    </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(f"""<div class="insight-box" style="border-color:{char['color']}">
        <strong>{char['name']}'s Takeaway:</strong> {char['takeaway']}
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Choose a different character"):
        st.session_state.character = None
        st.rerun()

# ── EPILOGUE ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="epilogue">
    <div class="epilogue-quote">"The crisis ended. The access gap didn't."</div>
    <div class="epilogue-body">
        64 million mortgages. 10 years. Five stories.<br><br>
        The American housing market survived the worst financial crisis in a century.
        But the version that emerged was quieter, more cautious, and more exclusive
        than the one that went in.<br><br>
        For some, the door reopened. For others, it never quite did.
    </div>
    <br><br>
    <div style="color:rgba(255,255,255,0.18);font-size:0.75rem;letter-spacing:0.2rem;text-transform:uppercase;">
        Data: HMDA Historic Data 2007–2017 · CFPB · Once Upon a Dataset
    </div>
</div>
""", unsafe_allow_html=True)
