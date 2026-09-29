# =============================================================================
# pages/3_Explore.py — Data Explorer
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import COLORS, inject_css, load_all_data, base_layout

st.set_page_config(
    page_title="Once Upon a Dataset — Explore",
    page_icon="🔍",
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
    ⚖️ Compare<br>
    <span style="opacity:0.6;">Side-by-side story arcs</span><br><br>
    🔍 <strong style="color:{COLORS['text']}">Explore</strong><br>
    <span style="opacity:0.6;">Raw data &amp; filters</span>
</div>
""", unsafe_allow_html=True)

with st.spinner('Loading 64 million stories…'):
    volume, purpose, ltype, race, sex, income, loan_race, state_year, va, explorer = load_all_data()

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <div class="page-eyebrow">Once Upon a Dataset · Data Explorer · HMDA 2007–2017</div>
    <div class="page-title">The Raw Numbers.</div>
    <div class="page-subtitle">
        Every chart in this project is built from these aggregates. Filter by year,
        state, loan type, and purpose — then see the data behind the stories.
    </div>
</div>
""", unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Filters</div>
<div class="section-title">Slice the Data</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    yr_filter = st.multiselect("Year",
        options=sorted(explorer['as_of_year'].unique()),
        default=sorted(explorer['as_of_year'].unique()))
with col2:
    state_filter = st.multiselect("State",
        options=sorted(explorer['state_abbr'].dropna().unique()),
        default=[])
with col3:
    type_filter = st.multiselect("Loan Type",
        options=sorted(explorer['loan_type_name'].unique()),
        default=[])
with col4:
    purpose_filter = st.multiselect("Loan Purpose",
        options=sorted(explorer['loan_purpose_name'].unique()),
        default=[])

exp_filtered = explorer[explorer['as_of_year'].isin(yr_filter)]
if state_filter:
    exp_filtered = exp_filtered[exp_filtered['state_abbr'].isin(state_filter)]
if type_filter:
    exp_filtered = exp_filtered[exp_filtered['loan_type_name'].isin(type_filter)]
if purpose_filter:
    exp_filtered = exp_filtered[exp_filtered['loan_purpose_name'].isin(purpose_filter)]

# ── KPI STRIP ────────────────────────────────────────────────────────────────
total    = exp_filtered['total_loans'].sum()
med_loan = exp_filtered['median_loan_amount'].median()
med_inc  = exp_filtered['median_income'].median()
n_states = exp_filtered['state_abbr'].nunique()
n_years  = exp_filtered['as_of_year'].nunique()

st.markdown(f"""
<div class="kpi-strip" style="margin-top:2rem;">
    <div class="kpi-cell">
        <div class="kpi-number c-gold">{total:,.0f}</div>
        <div class="kpi-label">Total Loans in Selection</div>
        <div class="kpi-sub">filtered rows summed</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-blue">${med_loan:,.0f}K</div>
        <div class="kpi-label">Median Loan Amount</div>
        <div class="kpi-sub">across selection</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-green">${med_inc:,.0f}K</div>
        <div class="kpi-label">Median Borrower Income</div>
        <div class="kpi-sub">across selection</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-gold">{n_states}</div>
        <div class="kpi-label">States in Selection</div>
        <div class="kpi-sub">distinct state codes</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-number c-purple">{n_years}</div>
        <div class="kpi-label">Years Covered</div>
        <div class="kpi-sub">in current filter</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── VOLUME CHART ─────────────────────────────────────────────────────────────
if yr_filter:
    st.markdown("""
    <div class="section-eyebrow">Trend</div>
    <div class="section-title">Loan Volume for Your Selection</div>
    """, unsafe_allow_html=True)

    vol_exp = exp_filtered.groupby('as_of_year')['total_loans'].sum().reset_index()
    fig_exp = go.Figure()
    fig_exp.add_trace(go.Bar(
        x=vol_exp['as_of_year'], y=vol_exp['total_loans'],
        marker_color=[COLORS['red'] if y <= 2009 else COLORS['gold'] if y <= 2013 else COLORS['green']
                      for y in vol_exp['as_of_year']],
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>%{y:,.0f} loans<extra></extra>'
    ))
    le = base_layout(height=360)
    le['showlegend']          = False
    le['yaxis']['tickformat'] = ','
    le['yaxis']['title']      = dict(text='Total loans', font=dict(color=COLORS['muted'], size=12))
    fig_exp.update_layout(**le)
    st.plotly_chart(fig_exp, width='stretch')

    # Loan type breakdown
    if not type_filter:
        st.markdown("""
        <div class="section-eyebrow" style="margin-top:1rem">Breakdown</div>
        <div class="section-title">Loan Type Mix in Your Selection</div>
        """, unsafe_allow_html=True)

        lt_exp     = exp_filtered.groupby(['as_of_year', 'loan_type_name'])['total_loans'].sum().reset_index()
        lt_exp_pct = lt_exp.copy()
        lt_exp_pct['pct'] = lt_exp_pct.groupby('as_of_year')['total_loans'].transform(
            lambda x: x / x.sum() * 100).round(1)
        lt_pivot = lt_exp_pct.pivot(index='as_of_year', columns='loan_type_name', values='pct').fillna(0)

        lt_colors = {'Conventional': COLORS['blue'], 'FHA-insured': COLORS['gold'],
                     'VA-guaranteed': COLORS['green'], 'FSA/RHS-guaranteed': COLORS['purple']}
        fig_lt = go.Figure()
        for lname, lcolor in lt_colors.items():
            if lname in lt_pivot.columns:
                fig_lt.add_trace(go.Bar(
                    x=lt_pivot.index, y=lt_pivot[lname], name=lname,
                    marker_color=lcolor, marker_line_width=0,
                    hovertemplate=f'<b>{lname}</b> %{{x}}: %{{y:.1f}}%<extra></extra>',
                ))
        llt = base_layout(height=320)
        llt['barmode']            = 'stack'
        llt['yaxis']['ticksuffix'] = '%'
        llt['yaxis']['range']     = [0, 105]
        fig_lt.update_layout(**llt)
        st.plotly_chart(fig_lt, width='stretch')

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-eyebrow">Data</div>
<div class="section-title">Detailed Records</div>
""", unsafe_allow_html=True)

display_df = exp_filtered.rename(columns={
    'as_of_year':         'Year',
    'state_abbr':         'State',
    'loan_type_name':     'Loan Type',
    'loan_purpose_name':  'Purpose',
    'total_loans':        'Total Loans',
    'median_loan_amount': 'Median Loan ($K)',
    'median_income':      'Median Income ($K)',
}).sort_values('Total Loans', ascending=False)

st.dataframe(
    display_df.head(200),
    width='stretch',
    hide_index=True,
    column_config={
        'Total Loans':       st.column_config.NumberColumn(format="%d"),
        'Median Loan ($K)':  st.column_config.NumberColumn(format="$%.0fK"),
        'Median Income ($K)':st.column_config.NumberColumn(format="$%.0fK"),
    }
)
st.caption(f"Showing top 200 rows of {len(display_df):,} total. Adjust filters above to narrow down.")

st.markdown(f"""
<div style="text-align:center;padding:2rem 0;margin-top:2rem;border-top:1px solid {COLORS['border']};">
    <div style="color:rgba(255,255,255,0.18);font-size:0.75rem;letter-spacing:0.2rem;text-transform:uppercase;">
        Data: HMDA Historic Data 2007–2017 · CFPB · Once Upon a Dataset
    </div>
</div>
""", unsafe_allow_html=True)
