# =============================================================================
# Home.py — Page 1: Market Overview
# Run with: streamlit run Home.py
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import COLORS, inject_css, load_all_data, base_layout, ANNO_STYLE

st.set_page_config(
    page_title="Once Upon a Dataset — Overview",
    page_icon="📊",
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
    📊 <strong style="color:{COLORS['text']}">Overview</strong><br>
    <span style="opacity:0.6;">Market-level data &amp; context</span><br><br>
    📖 Stories<br>
    <span style="opacity:0.6;">Five characters, five decades</span><br><br>
    ⚖️ Compare<br>
    <span style="opacity:0.6;">Side-by-side story arcs</span><br><br>
    🔍 Explore<br>
    <span style="opacity:0.6;">Raw data &amp; filters</span>
</div>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────
with st.spinner('Loading 64 million stories…'):
    volume, purpose, ltype, race, sex, income, loan_race, state_year, va, explorer = load_all_data()

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <div class="page-eyebrow">Once Upon a Dataset · Market Overview · HMDA 2007–2017</div>
    <div class="page-title">Before the Characters,<br>Read the Room.</div>
    <div class="page-subtitle">
        64 million mortgages. One decade. A crash that changed who could own a home —
        and who couldn't. Before you follow any one story, here is what the data
        shows everyone.
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI STRIP ────────────────────────────────────────────────────────────────
total_loans   = volume['total'].sum()
peak_refi_pct = purpose[purpose['loan_purpose_name'] == 'Refinancing']['pct'].max()
crash_drop    = (volume.set_index('as_of_year').loc[2008, 'total'] /
                 volume.set_index('as_of_year').loc[2007, 'total'] - 1) * 100
gov_types     = ['FHA-insured', 'VA-guaranteed', 'FSA/RHS-guaranteed']
gov_2007_pct  = ltype[(ltype['as_of_year'] == 2007) & ltype['loan_type_name'].isin(gov_types)]['pct'].sum()
gov_2010_pct  = ltype[(ltype['as_of_year'] == 2010) & ltype['loan_type_name'].isin(gov_types)]['pct'].sum()
income_change = (income.set_index('as_of_year').loc[2017, 'median_income'] /
                 income.set_index('as_of_year').loc[2007, 'median_income'] - 1) * 100

st.markdown(f"""
<div class="kpi-strip">
    <div class="kpi-cell">
        <div class="kpi-number c-gold">64M</div>
        <div class="kpi-label">Total mortgages<br>funded 2007–2017</div>
        <div class="kpi-sub">HMDA full dataset</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-red">{crash_drop:.0f}%</div>
        <div class="kpi-label">Volume drop<br>in 2008</div>
        <div class="kpi-sub">vs. 2007 peak</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-red">{peak_refi_pct:.0f}%</div>
        <div class="kpi-label">Of 2009 mortgages<br>were refinancing</div>
        <div class="kpi-sub">not new home purchases</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-green">{gov_2010_pct / gov_2007_pct:.1f}×</div>
        <div class="kpi-label">Gov-backed loan<br>share multiplier</div>
        <div class="kpi-sub">2007 → 2010</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-blue">+{income_change:.0f}%</div>
        <div class="kpi-label">Rise in approved<br>borrower income</div>
        <div class="kpi-sub">2007 → 2017</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-gold">2014</div>
        <div class="kpi-label">Real recovery<br>year</div>
        <div class="kpi-sub">buying > refinancing</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — CRASH & RECOVERY TIMELINE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Section 01</div>
<div class="section-title">The Crash, the Illusion, and the Real Recovery</div>
<div class="section-body">
    The market didn't just crash in 2008 — it was then disguised by a surge of
    refinancing that made volume look healthy again. The true recovery, measured
    by actual home purchases, didn't arrive until 2014.
</div>
""", unsafe_allow_html=True)

pp = purpose[purpose['loan_purpose_name'].isin(['Home purchase', 'Refinancing'])]
pp_pivot = pp.pivot(index='as_of_year', columns='loan_purpose_name', values='count').fillna(0)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=volume['as_of_year'], y=volume['total'], name='Total volume',
    marker_color='rgba(255,255,255,0.04)',
    marker_line_color='rgba(255,255,255,0.08)', marker_line_width=1,
    hovertemplate='<b>%{x}</b> — Total: %{y:,.0f}<extra></extra>',
))
if 'Home purchase' in pp_pivot.columns:
    fig1.add_trace(go.Scatter(
        x=pp_pivot.index, y=pp_pivot['Home purchase'], name='Home purchases',
        mode='lines+markers', line=dict(color=COLORS['green'], width=3),
        marker=dict(size=7, color=COLORS['green']),
        fill='tozeroy', fillcolor='rgba(42,157,143,0.12)',
        hovertemplate='<b>%{x}</b> — Purchases: %{y:,.0f}<extra></extra>',
    ))
if 'Refinancing' in pp_pivot.columns:
    fig1.add_trace(go.Scatter(
        x=pp_pivot.index, y=pp_pivot['Refinancing'], name='Refinancing',
        mode='lines+markers', line=dict(color=COLORS['red'], width=3),
        marker=dict(size=7, color=COLORS['red']),
        fill='tozeroy', fillcolor='rgba(230,57,70,0.10)',
        hovertemplate='<b>%{x}</b> — Refis: %{y:,.0f}<extra></extra>',
    ))

fig1.add_annotation(
    x=2008, y=volume.set_index('as_of_year').loc[2008, 'total'],
    text="<b>2008 — The Crash</b><br>−24% total volume",
    arrowcolor=COLORS['red'], bordercolor=COLORS['red'],
    font=dict(color=COLORS['red'], size=11),
    ax=60, ay=-55, **ANNO_STYLE)
fig1.add_annotation(
    x=2009, y=pp_pivot.loc[2009, 'Refinancing'] if 'Refinancing' in pp_pivot.columns else 0,
    text="<b>2009 — The Illusion</b><br>Refis surge. Market<br>looks healthy. Isn't.",
    arrowcolor=COLORS['gold'], bordercolor=COLORS['gold'],
    font=dict(color=COLORS['gold'], size=11),
    ax=-90, ay=-60, **ANNO_STYLE)
fig1.add_annotation(
    x=2014, y=pp_pivot.loc[2014, 'Home purchase'] if 'Home purchase' in pp_pivot.columns else 0,
    text="<b>2014 — Real Recovery</b><br>Purchases finally<br>overtake refis",
    arrowcolor=COLORS['green'], bordercolor=COLORS['green'],
    font=dict(color=COLORS['green'], size=11),
    ax=80, ay=-70, **ANNO_STYLE)

l1 = base_layout(height=460)
l1['barmode'] = 'overlay'
l1['yaxis']['tickformat'] = ','
l1['yaxis']['title'] = dict(text='Number of mortgages', font=dict(color=COLORS['muted'], size=12))
fig1.update_layout(**l1)
st.plotly_chart(fig1, width='stretch')

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"""<div class="insight-box callout-red">
        <strong>The 2008 crash was real and severe.</strong> Total mortgage originations
        fell by nearly a quarter in a single year. Lending didn't just slow — it seized.
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""<div class="insight-box" style="border-left-color:{COLORS['gold']}">
        <strong>The 2009 "recovery" was a mirage.</strong> Volume rebounded — but
        {peak_refi_pct:.0f}% of it was existing homeowners refinancing, not new buyers
        entering the market. The recovery headline hid a frozen market underneath.
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — GOVERNMENT INTERVENTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Section 02</div>
<div class="section-title">When Private Lenders Fled, the Government Stepped In</div>
<div class="section-body">
    As conventional lending collapsed, FHA and VA programs became the market's
    backbone. Without government-backed loans, millions of buyers would have been
    completely locked out of homeownership.
</div>
""", unsafe_allow_html=True)

lt_order = ['Conventional', 'FHA-insured', 'VA-guaranteed', 'FSA/RHS-guaranteed']
lt_colors_map = {
    'Conventional':       COLORS['blue'],
    'FHA-insured':        COLORS['gold'],
    'VA-guaranteed':      COLORS['green'],
    'FSA/RHS-guaranteed': COLORS['purple'],
}
lt_pivot = ltype.pivot(index='as_of_year', columns='loan_type_name', values='pct').fillna(0)

fig2 = go.Figure()
for lname in lt_order:
    if lname in lt_pivot.columns:
        fig2.add_trace(go.Bar(
            x=lt_pivot.index, y=lt_pivot[lname], name=lname,
            marker_color=lt_colors_map.get(lname, COLORS['muted']),
            marker_line_width=0,
            hovertemplate=f'<b>{lname}</b> %{{x}}: %{{y:.1f}}%<extra></extra>',
        ))

fig2.add_annotation(
    x=2007, y=95,
    text="Conventional dominates<br>~92% of market",
    arrowcolor=COLORS['blue'], bordercolor=COLORS['blue'],
    font=dict(color=COLORS['blue'], size=10),
    ax=80, ay=-40, **ANNO_STYLE)
fig2.add_annotation(
    x=2009, y=75,
    text="<b>FHA triples overnight</b><br>From 6% → 22%",
    arrowcolor=COLORS['gold'], bordercolor=COLORS['gold'],
    font=dict(color=COLORS['gold'], size=10),
    ax=-80, ay=40, **ANNO_STYLE)
fig2.add_annotation(
    x=2017, y=88,
    text="VA reaches 10.6%<br>6× growth since 2007",
    arrowcolor=COLORS['green'], bordercolor=COLORS['green'],
    font=dict(color=COLORS['green'], size=10),
    ax=-90, ay=-50, **ANNO_STYLE)

l2 = base_layout(height=440)
l2['barmode'] = 'stack'
l2['yaxis']['ticksuffix'] = '%'
l2['yaxis']['range'] = [0, 105]
l2['yaxis']['title'] = dict(text='Share of all mortgages (%)', font=dict(color=COLORS['muted'], size=12))
fig2.update_layout(**l2)
st.plotly_chart(fig2, width='stretch')

gov_by_year  = ltype[ltype['loan_type_name'].isin(gov_types)].groupby('as_of_year')['pct'].sum().reset_index()
peak_gov_yr  = gov_by_year.loc[gov_by_year['pct'].idxmax(), 'as_of_year']
peak_gov_pct = gov_by_year['pct'].max()
base_gov_pct = gov_by_year[gov_by_year['as_of_year'] == 2007]['pct'].values[0]
late_gov_pct = gov_by_year[gov_by_year['as_of_year'] == 2017]['pct'].values[0]

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f"""<div class="insight-box callout-blue">
        <strong>Conventional lenders collapsed.</strong> Private loans fell from ~92%
        to ~74% of the market at the crash's nadir — an unprecedented retreat from
        residential lending.
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""<div class="insight-box">
        <strong>FHA became the market's floor.</strong> Government-backed loans peaked at
        {peak_gov_pct:.0f}% of all originations in {peak_gov_yr} — up from just
        {base_gov_pct:.0f}% before the crisis. Without FHA, the housing market would
        have frozen for millions of buyers.
    </div>""", unsafe_allow_html=True)
with col_c:
    st.markdown(f"""<div class="insight-box callout-green">
        <strong>VA loans never went back.</strong> The crisis permanently expanded veteran
        homeownership. By 2017, VA loans held {late_gov_pct - base_gov_pct:.0f} more
        percentage points of the market than before the crash.
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — THE RISING BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Section 03</div>
<div class="section-title">Banks Quietly Raised the Bar</div>
<div class="section-body">
    Even as the market "recovered," approved borrowers were progressively richer.
    Median borrower income rose steadily after the crash — not because incomes
    improved, but because lower-income applicants stopped getting approved.
</div>
""", unsafe_allow_html=True)

fig3 = make_subplots(specs=[[{"secondary_y": True}]])
income_bar_colors = [
    COLORS['red'] if y <= 2009 else COLORS['gold'] if y <= 2013 else COLORS['green']
    for y in income['as_of_year']
]
fig3.add_trace(go.Bar(
    x=income['as_of_year'], y=income['median_income'],
    name='Median borrower income ($K)',
    marker_color=income_bar_colors, marker_line_width=0, opacity=0.85,
    hovertemplate='<b>%{x}</b> — Income: $%{y:.0f}K<extra></extra>',
), secondary_y=False)
fig3.add_trace(go.Scatter(
    x=income['as_of_year'], y=income['median_loan'],
    name='Median loan amount ($K)', mode='lines+markers',
    line=dict(color=COLORS['blue'], width=3, dash='dot'),
    marker=dict(size=8, color=COLORS['blue'], symbol='diamond'),
    hovertemplate='<b>%{x}</b> — Loan: $%{y:.0f}K<extra></extra>',
), secondary_y=True)

base_inc    = income.set_index('as_of_year').loc[2007, 'median_income']
peak_inc    = income['median_income'].max()
peak_inc_yr = income.loc[income['median_income'].idxmax(), 'as_of_year']

fig3.add_annotation(
    x=2007, y=base_inc,
    text=f"<b>Pre-crisis baseline</b><br>${base_inc:.0f}K",
    arrowcolor=COLORS['muted'], bordercolor=COLORS['muted'],
    font=dict(color=COLORS['muted'], size=10),
    ax=80, ay=-40, **ANNO_STYLE)
fig3.add_annotation(
    x=peak_inc_yr, y=peak_inc,
    text=f"<b>+{((peak_inc/base_inc)-1)*100:.0f}% from baseline</b><br>Lower-income buyers filtered out",
    arrowcolor=COLORS['gold'], bordercolor=COLORS['gold'],
    font=dict(color=COLORS['gold'], size=10),
    ax=-80, ay=-50, **ANNO_STYLE)
fig3.add_vrect(
    x0=2009.5, x1=2013.5,
    fillcolor='rgba(244,162,97,0.05)', layer='below', line_width=0,
    annotation_text='Tightening years', annotation_position='top left',
    annotation_font_size=10, annotation_font_color=COLORS['muted'])

l3 = base_layout(height=440)
l3['yaxis']['title']      = dict(text='Median borrower income ($K)', font=dict(color=COLORS['muted'], size=12))
l3['yaxis']['tickprefix'] = '$'
l3['yaxis']['ticksuffix'] = 'K'
l3['yaxis2'] = dict(
    title=dict(text='Median loan amount ($K)', font=dict(color=COLORS['blue'], size=12)),
    tickprefix='$', ticksuffix='K', overlaying='y', side='right',
    showgrid=False, color=COLORS['blue'], tickfont=dict(color=COLORS['blue'], size=11),
)
fig3.update_layout(**l3)
st.plotly_chart(fig3, width='stretch')

col_a, col_b = st.columns([3, 2])
with col_a:
    st.markdown(f"""<div class="insight-box">
        <strong>The rising bar was invisible to most observers.</strong>
        There were no policy announcements, no headlines. Banks simply became
        more selective — raising income and credit requirements quietly,
        applicant by application. The result: the approved borrower pool became
        systematically wealthier every year after 2008.
        <br><br>
        Lower-income first-time buyers, single-income households, and borrowers
        in underserved communities found themselves filtered out of a market that
        looked, on the surface, like it was recovering.
    </div>""", unsafe_allow_html=True)
with col_b:
    i07 = income.set_index('as_of_year').loc[2007, 'median_income']
    i17 = income.set_index('as_of_year').loc[2017, 'median_income']
    l07 = income.set_index('as_of_year').loc[2007, 'median_loan']
    l17 = income.set_index('as_of_year').loc[2017, 'median_loan']
    st.markdown(f"""<div class="insight-box callout-blue" style="margin-top:0;">
        <strong>By the numbers:</strong><br><br>
        📈 Median income: <strong style="color:{COLORS['gold']}">${i07:.0f}K → ${i17:.0f}K</strong><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(+{((i17/i07)-1)*100:.0f}% over the decade)<br><br>
        🏠 Median loan: <strong style="color:{COLORS['blue']}">${l07:.0f}K → ${l17:.0f}K</strong><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(+{((l17/l07)-1)*100:.0f}% over the decade)
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — GENDER GAP
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Section 04</div>
<div class="section-title">The Gender Gap Nobody Headlined</div>
<div class="section-body">
    Female borrowers — who disproportionately represent single-income households —
    saw their share of approved loans drop sharply during the crisis and never
    fully recover. The same tightening that pruned lower incomes also pruned
    single-income applicants.
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([3, 2])

with col_a:
    sex_filtered = sex[sex['applicant_sex_name'].isin(['Male', 'Female', 'Joint (Male/Female)'])]
    sex_pivot    = sex_filtered.pivot(index='as_of_year', columns='applicant_sex_name', values='pct').fillna(0)
    gender_colors = {
        'Male':                COLORS['blue'],
        'Female':              COLORS['gold'],
        'Joint (Male/Female)': COLORS['green'],
    }

    fig4a = go.Figure()
    for gcat in ['Male', 'Female', 'Joint (Male/Female)']:
        if gcat in sex_pivot.columns:
            is_female = gcat == 'Female'
            fig4a.add_trace(go.Scatter(
                x=sex_pivot.index, y=sex_pivot[gcat], name=gcat,
                mode='lines+markers',
                line=dict(color=gender_colors[gcat], width=4 if is_female else 2),
                marker=dict(size=9 if is_female else 6),
                hovertemplate=f'<b>{gcat}</b> %{{x}}: %{{y:.1f}}%<extra></extra>',
            ))

    if 'Female' in sex_pivot.columns:
        fig4a.add_annotation(
            x=2007, y=sex_pivot.loc[2007, 'Female'],
            text="30.7% — peak", showarrow=False,
            font=dict(color=COLORS['gold'], size=10), yshift=14)
        fig4a.add_annotation(
            x=2011, y=sex_pivot.loc[2011, 'Female'],
            text="<b>Lowest — 25.7%</b><br>−5pp in 4 years",
            arrowcolor=COLORS['red'], bordercolor=COLORS['red'],
            font=dict(color=COLORS['red'], size=10),
            ax=80, ay=30, **ANNO_STYLE)
        fig4a.add_annotation(
            x=2017, y=sex_pivot.loc[2017, 'Female'],
            text="Still below 2007",
            arrowcolor=COLORS['gold'], bordercolor=COLORS['gold'],
            font=dict(color=COLORS['gold'], size=10),
            ax=-80, ay=-35, **ANNO_STYLE)

    l4a = base_layout(height=400)
    l4a['yaxis']['ticksuffix'] = '%'
    l4a['yaxis']['title'] = dict(text='Share of approved borrowers (%)', font=dict(color=COLORS['muted'], size=12))
    fig4a.update_layout(**l4a)
    st.plotly_chart(fig4a, width='stretch')

with col_b:
    f07_vals = sex[(sex['as_of_year'] == 2007) & (sex['applicant_sex_name'] == 'Female')]['pct'].values
    f11_vals = sex[(sex['as_of_year'] == 2011) & (sex['applicant_sex_name'] == 'Female')]['pct'].values
    f17_vals = sex[(sex['as_of_year'] == 2017) & (sex['applicant_sex_name'] == 'Female')]['pct'].values
    f07 = float(f07_vals[0]) if len(f07_vals) else 30.7
    f11 = float(f11_vals[0]) if len(f11_vals) else 25.7
    f17 = float(f17_vals[0]) if len(f17_vals) else 27.0

    st.markdown(f"""
    <div class="insight-box" style="border-left-color:{COLORS['gold']};margin-top:0;margin-bottom:1rem;">
        <strong style="color:{COLORS['gold']}">Female borrowers</strong><br><br>
        <span style="font-family:'Playfair Display',serif;font-size:1.6rem;color:{COLORS['gold']}">{f07:.1f}%</span>
        <span style="color:{COLORS['muted']};font-size:0.85rem;"> 2007 — pre-crisis share</span><br><br>
        <span style="font-family:'Playfair Display',serif;font-size:1.6rem;color:{COLORS['red']}">{f11:.1f}%</span>
        <span style="color:{COLORS['muted']};font-size:0.85rem;"> 2011 — post-crash low</span><br><br>
        <span style="font-family:'Playfair Display',serif;font-size:1.6rem;color:{COLORS['gold']}">{f17:.1f}%</span>
        <span style="color:{COLORS['muted']};font-size:0.85rem;"> 2017 — still not recovered</span>
    </div>
    <div class="insight-box callout-red">
        <strong>Single-income households bore the brunt.</strong>
        The crisis-era tightening fell disproportionately on single applicants.
        Female borrowers lost 5 percentage points of market share between 2007
        and 2011 — and never fully regained it by 2017.
    </div>
    <div class="insight-box callout-green">
        <strong>Joint applications held steadier.</strong>
        Two-income households were better insulated from the new income
        thresholds banks quietly imposed after the crash.
    </div>
    """, unsafe_allow_html=True)

# Correlation chart
st.markdown(f"""<div class="section-body" style="margin-top:1rem;">
    As banks demanded higher incomes, single-applicant households were
    disproportionately filtered out — the two lines below tell the story.
</div>""", unsafe_allow_html=True)

female_ts = sex[sex['applicant_sex_name'] == 'Female'].set_index('as_of_year')['pct']
fig4b = make_subplots(specs=[[{"secondary_y": True}]])
fig4b.add_trace(go.Scatter(
    x=female_ts.index, y=female_ts.values,
    name='Female borrower share (%)',
    mode='lines+markers', line=dict(color=COLORS['gold'], width=3),
    marker=dict(size=8),
    fill='tozeroy', fillcolor='rgba(244,162,97,0.1)',
    hovertemplate='<b>%{x}</b> — Female share: %{y:.1f}%<extra></extra>',
), secondary_y=False)
fig4b.add_trace(go.Scatter(
    x=income['as_of_year'], y=income['median_income'],
    name='Median borrower income ($K)',
    mode='lines+markers', line=dict(color=COLORS['red'], width=2, dash='dot'),
    marker=dict(size=6, symbol='diamond'),
    hovertemplate='<b>%{x}</b> — Median income: $%{y:.0f}K<extra></extra>',
), secondary_y=True)

l4b = base_layout(height=320)
l4b['yaxis']['ticksuffix'] = '%'
l4b['yaxis']['range']      = [22, 33]
l4b['yaxis']['title']      = dict(text='Female borrower share (%)', font=dict(color=COLORS['gold'], size=11))
l4b['yaxis2'] = dict(
    title=dict(text='Median borrower income ($K)', font=dict(color=COLORS['red'], size=11)),
    tickprefix='$', ticksuffix='K', overlaying='y', side='right',
    showgrid=False, color=COLORS['red'], tickfont=dict(color=COLORS['red'], size=10),
)
fig4b.update_layout(**l4b)
st.plotly_chart(fig4b, width='stretch')

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — GEOGRAPHIC PULSE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Section 05</div>
<div class="section-title">The Geographic Pulse of the Market</div>
<div class="section-body">
    The crisis and recovery were never uniform. Use the slider to watch how
    mortgage activity shifted state by state across the decade.
</div>
""", unsafe_allow_html=True)

years_avail = sorted(state_year['as_of_year'].unique())
map_year    = st.select_slider('Select year', options=years_avail, value=2009, key='overview_map')
map_df      = state_year[state_year['as_of_year'] == map_year]
nat_total   = volume.set_index('as_of_year').loc[map_year, 'total']

fig_map = go.Figure(go.Choropleth(
    locations=map_df['state_abbr'], z=map_df['total'],
    locationmode='USA-states',
    colorscale=[[0.0,'#0d0d1a'],[0.25,'#16213e'],[0.5,'#1a3a5c'],[0.75,'#2e6da4'],[1.0,'#f4a261']],
    colorbar=dict(
        title=dict(text='Mortgages', font=dict(color=COLORS['text'])),
        tickfont=dict(color=COLORS['text']), bgcolor='rgba(0,0,0,0)', len=0.6),
    hovertemplate='<b>%{location}</b><br>%{z:,.0f} mortgages<extra></extra>',
    marker_line_color='rgba(255,255,255,0.1)', marker_line_width=0.5,
))
fig_map.update_layout(
    geo=dict(scope='usa', bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)',
             landcolor='#12121a', showlakes=True, showframe=False,
             coastlinecolor='rgba(255,255,255,0.1)', showcoastlines=True),
    paper_bgcolor='rgba(0,0,0,0)', font=dict(color=COLORS['text']),
    margin=dict(t=10, b=0, l=0, r=0), height=440,
)
st.plotly_chart(fig_map, width='stretch')

top5 = map_df.nlargest(5, 'total')
bot5 = map_df.nsmallest(5, 'total')
col_a, col_b, col_c = st.columns([2, 2, 3])
with col_a:
    top_pills = ''.join([
        f"<span class='anno-pill'>{'★ ' if i == 0 else ''}{r['state_abbr']}: {r['total']:,.0f}</span>"
        for i, (_, r) in enumerate(top5.iterrows())
    ])
    st.markdown(f"""<div class="insight-box"><strong>Top 5 states — {map_year}</strong><br><br>{top_pills}</div>""", unsafe_allow_html=True)
with col_b:
    bot_pills = ''.join([
        f"<span class='anno-pill' style='background:rgba(230,57,70,0.1);border-color:rgba(230,57,70,0.3);color:{COLORS['red']}'>{r['state_abbr']}: {r['total']:,.0f}</span>"
        for _, r in bot5.iterrows()
    ])
    st.markdown(f"""<div class="insight-box callout-red"><strong>Lowest 5 states — {map_year}</strong><br><br>{bot_pills}</div>""", unsafe_allow_html=True)
with col_c:
    if map_year > 2007:
        prev_total = volume.set_index('as_of_year').loc[map_year - 1, 'total']
        yoy        = (nat_total / prev_total - 1) * 100
        yoy_color  = COLORS['green'] if yoy > 0 else COLORS['red']
        yoy_str    = f'<strong>Year-over-year:</strong> <span style="color:{yoy_color}">{"▲" if yoy > 0 else "▼"} {abs(yoy):.1f}%</span><br>'
    else:
        yoy_str = ''
    st.markdown(f"""<div class="insight-box">
        <strong>National total — {map_year}:</strong>
        <span style="font-family:'Playfair Display',serif;font-size:1.4rem;color:{COLORS['gold']};margin-left:0.5rem">{nat_total:,.0f}</span>
        <br><br>{yoy_str}
        <span style="font-size:0.85rem;color:{COLORS['muted']}">
            California, Texas, and Florida consistently account for roughly
            30–35% of all national mortgage originations.
        </span>
    </div>""", unsafe_allow_html=True)

# ── NAV FOOTER ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nav-next">
    <div class="nav-next-label">Now that you know the landscape</div>
    <div class="nav-next-title">Meet the people who lived inside it →</div>
    <br>
    <div style="color:{COLORS['muted']};font-size:0.9rem;max-width:520px;margin:0 auto;line-height:1.8;">
        Five characters. Five completely different experiences of the same decade.
        Use the sidebar to navigate to <strong style="color:{COLORS['text']}">Stories</strong>.
    </div>
</div>
""", unsafe_allow_html=True)
