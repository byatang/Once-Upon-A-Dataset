# =============================================================================
# utils.py — Shared constants, CSS, data loading, and chart helpers
# =============================================================================

from pathlib import Path

import streamlit as st
import pandas as pd

DATA_PATH = Path(__file__).parent / 'hmda_master.parquet'

# ─────────────────────────────────────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────────────────────────────────────
COLORS = {
    'background': '#0a0a0f',
    'card':       '#12121a',
    'card2':      '#16162a',
    'gold':       '#f4a261',
    'red':        '#e63946',
    'green':      '#2a9d8f',
    'blue':       '#457b9d',
    'purple':     '#7b2d8b',
    'text':       '#edf2f4',
    'muted':      '#8d99ae',
    'border':     'rgba(255,255,255,0.06)',
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        font-family: 'Inter', sans-serif;
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .main .block-container {{ padding: 0rem 3rem 4rem 3rem; max-width: 1400px; }}

    [data-testid="stSidebar"] {{
        background-color: {COLORS['card']} !important;
        border-right: 1px solid {COLORS['border']};
    }}

    .page-hero {{
        padding: 4rem 0 2.5rem 0;
        border-bottom: 1px solid {COLORS['border']};
        margin-bottom: 3rem;
    }}
    .page-eyebrow {{
        font-size: 0.72rem;
        letter-spacing: 0.45rem;
        color: {COLORS['gold']};
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-weight: 500;
    }}
    .page-title {{
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: {COLORS['text']};
        line-height: 1.15;
        margin-bottom: 1rem;
        font-weight: 700;
    }}
    .page-subtitle {{
        font-size: 1.05rem;
        color: {COLORS['muted']};
        max-width: 680px;
        line-height: 1.85;
    }}

    .section-eyebrow {{
        font-size: 0.7rem;
        letter-spacing: 0.35rem;
        color: {COLORS['gold']};
        text-transform: uppercase;
        margin-bottom: 0.4rem;
        font-weight: 500;
    }}
    .section-title {{
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: {COLORS['text']};
        margin-bottom: 0.6rem;
        border-left: 3px solid {COLORS['gold']};
        padding-left: 1rem;
        line-height: 1.3;
    }}
    .section-body {{
        font-size: 0.95rem;
        color: {COLORS['muted']};
        line-height: 1.85;
        max-width: 720px;
        margin-bottom: 1.5rem;
    }}
    .section-divider {{
        border: none;
        border-top: 1px solid {COLORS['border']};
        margin: 3.5rem 0;
    }}

    .kpi-strip {{
        display: flex;
        gap: 0;
        margin: 2rem 0 3rem 0;
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        overflow: hidden;
    }}
    .kpi-cell {{
        flex: 1;
        padding: 1.8rem 1.5rem;
        text-align: center;
        border-right: 1px solid {COLORS['border']};
        background: {COLORS['card']};
        transition: background 0.2s;
    }}
    .kpi-cell:last-child {{ border-right: none; }}
    .kpi-cell:hover {{ background: {COLORS['card2']}; }}
    .kpi-number {{
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.5rem;
    }}
    .kpi-label {{
        font-size: 0.75rem;
        color: {COLORS['muted']};
        text-transform: uppercase;
        letter-spacing: 0.08rem;
        line-height: 1.5;
    }}
    .kpi-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: {COLORS['muted']};
        margin-top: 0.3rem;
        opacity: 0.6;
    }}
    .c-gold   {{ color: {COLORS['gold']}; }}
    .c-red    {{ color: {COLORS['red']}; }}
    .c-green  {{ color: {COLORS['green']}; }}
    .c-blue   {{ color: {COLORS['blue']}; }}
    .c-purple {{ color: {COLORS['purple']}; }}

    .insight-box {{
        background: {COLORS['card']};
        border-left: 4px solid {COLORS['gold']};
        border-radius: 0 12px 12px 0;
        padding: 1.4rem 1.8rem;
        margin: 1.5rem 0;
        font-size: 0.95rem;
        color: {COLORS['text']};
        line-height: 1.8;
    }}
    .insight-box strong {{ color: {COLORS['gold']}; }}
    .callout-red    {{ border-left-color: {COLORS['red']}    !important; }}
    .callout-green  {{ border-left-color: {COLORS['green']}  !important; }}
    .callout-blue   {{ border-left-color: {COLORS['blue']}   !important; }}
    .callout-purple {{ border-left-color: {COLORS['purple']} !important; }}

    .anno-pill {{
        display: inline-block;
        background: rgba(244,162,97,0.12);
        border: 1px solid rgba(244,162,97,0.35);
        border-radius: 20px;
        padding: 0.25rem 0.9rem;
        font-size: 0.75rem;
        color: {COLORS['gold']};
        font-weight: 500;
        margin: 0.2rem;
    }}

    .choose-prompt {{
        font-size: 1.3rem;
        color: {COLORS['gold']};
        font-family: 'Playfair Display', serif;
        margin-bottom: 2rem;
        text-align: center;
    }}
    .act-label {{
        font-size: 0.75rem;
        letter-spacing: 0.3rem;
        color: {COLORS['gold']};
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }}
    .act-title {{
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: {COLORS['text']};
        margin-bottom: 1rem;
        border-left: 4px solid {COLORS['gold']};
        padding-left: 1rem;
    }}
    .act-body {{
        font-size: 1rem;
        color: {COLORS['muted']};
        line-height: 1.8;
        max-width: 800px;
        margin-bottom: 2rem;
    }}

    .epilogue {{
        text-align: center;
        padding: 4rem 2rem;
        border-top: 1px solid {COLORS['border']};
        margin-top: 4rem;
    }}
    .epilogue-quote {{
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: {COLORS['gold']};
        margin-bottom: 1.5rem;
        font-style: italic;
    }}
    .epilogue-body {{
        font-size: 1rem;
        color: {COLORS['muted']};
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.8;
    }}

    .stButton > button {{
        background: transparent;
        border: 1px solid rgba(255,255,255,0.15);
        color: {COLORS['text']};
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'Inter', sans-serif;
    }}
    .stButton > button:hover {{
        border-color: {COLORS['gold']};
        color: {COLORS['gold']};
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: {COLORS['card']};
        border-radius: 12px;
        padding: 0.3rem;
        gap: 0.3rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: {COLORS['muted']};
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }}
    .stTabs [aria-selected="true"] {{
        background: {COLORS['background']};
        color: {COLORS['gold']};
    }}

    .stDataFrame {{ background: {COLORS['card']}; border-radius: 12px; }}

    .nav-next {{
        text-align: center;
        padding: 3rem 2rem;
        border-top: 1px solid {COLORS['border']};
        margin-top: 4rem;
    }}
    .nav-next-label {{
        font-size: 0.75rem;
        letter-spacing: 0.3rem;
        color: {COLORS['muted']};
        text-transform: uppercase;
        margin-bottom: 1rem;
    }}
    .nav-next-title {{
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: {COLORS['gold']};
        font-style: italic;
    }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
# Only the columns the aggregations below use; text columns are read as
# categoricals so the 64M-row file fits in memory.
TEXT_COLUMNS = ['loan_purpose_name', 'loan_type_name', 'applicant_race_name_1',
                'applicant_sex_name', 'state_abbr']
NUMERIC_COLUMNS = ['as_of_year', 'applicant_income_000s', 'loan_amount_000s']


@st.cache_data
def load_all_data():
    df = pd.read_parquet(DATA_PATH, columns=NUMERIC_COLUMNS + TEXT_COLUMNS,
                         read_dictionary=TEXT_COLUMNS)

    volume = df.groupby('as_of_year').size().reset_index(name='total')

    purpose = df.groupby(['as_of_year', 'loan_purpose_name']).size().reset_index(name='count')
    purpose['pct'] = purpose.groupby('as_of_year')['count'].transform(
        lambda x: x / x.sum() * 100).round(2)

    ltype = df.groupby(['as_of_year', 'loan_type_name']).size().reset_index(name='count')
    ltype['pct'] = ltype.groupby('as_of_year')['count'].transform(
        lambda x: x / x.sum() * 100).round(2)

    main_races = ['White', 'Black or African American', 'Asian',
                  'American Indian or Alaska Native',
                  'Native Hawaiian or Other Pacific Islander']
    race = df[df['applicant_race_name_1'].isin(main_races)].groupby(
        ['as_of_year', 'applicant_race_name_1']).size().reset_index(name='count')
    race['pct'] = race.groupby('as_of_year')['count'].transform(
        lambda x: x / x.sum() * 100).round(1)

    sex = df.groupby(['as_of_year', 'applicant_sex_name']).size().reset_index(name='count')
    sex['pct'] = sex.groupby('as_of_year')['count'].transform(
        lambda x: x / x.sum() * 100).round(1)

    income = df.groupby('as_of_year').agg(
        median_income=('applicant_income_000s', 'median'),
        median_loan=('loan_amount_000s', 'median')
    ).reset_index()

    loan_race = df[df['applicant_race_name_1'].isin(
        ['White', 'Black or African American', 'Asian'])].groupby(
        ['as_of_year', 'applicant_race_name_1'])['loan_amount_000s'].median().reset_index()

    state_year = df.groupby(['as_of_year', 'state_abbr']).size().reset_index(
        name='total').dropna()

    va = ltype[ltype['loan_type_name'] == 'VA-guaranteed'][['as_of_year', 'pct']].copy()

    explorer = df.groupby(['as_of_year', 'state_abbr', 'loan_type_name',
                           'loan_purpose_name']).agg(
        total_loans=('loan_amount_000s', 'count'),
        median_loan_amount=('loan_amount_000s', 'median'),
        median_income=('applicant_income_000s', 'median')
    ).reset_index().dropna()

    return volume, purpose, ltype, race, sex, income, loan_race, state_year, va, explorer


# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────

# font is NOT in ANNO_STYLE — pass font= separately in each add_annotation() call
ANNO_STYLE = dict(
    showarrow=True,
    arrowhead=2,
    arrowwidth=1.5,
    bgcolor=COLORS['background'],
    borderwidth=1,
)

def base_layout(title='', height=420):
    return dict(
        title=dict(text=title, font=dict(size=15, color=COLORS['text'])) if title else {},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text'], family='Inter'),
        height=height,
        margin=dict(t=50 if title else 20, b=40, l=50, r=30),
        xaxis=dict(showgrid=False, tickmode='linear', dtick=1,
                   color=COLORS['muted'], tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                   color=COLORS['muted'], tickfont=dict(size=11)),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=COLORS['text'], size=11),
                    orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
        hovermode='x unified',
    )


# ─────────────────────────────────────────────────────────────────────────────
# CHARACTER MAP CONFIG
# ─────────────────────────────────────────────────────────────────────────────
CHARACTER_MAP_CONFIG = {
    'first_time': {
        'colorscale': [[0.0,'#1a0a0a'],[0.3,'#3d1515'],[0.6,'#922020'],[0.8,'#e63946'],[1.0,'#ff8fa3']],
        'highlight_states': ['MS','AL','LA','GA','SC','AR'],
        'highlight_label': 'States with historically lowest minority borrower approval shares',
        'colorbar_title': 'Loans',
        'map_note': '🔴 Highlighted states saw the sharpest drops in Black and minority borrower approvals after 2008. The recovery in loan volume never fully translated into restored access for underserved communities.',
    },
    'established': {
        'colorscale': [[0.0,'#040f1f'],[0.3,'#0c2e55'],[0.6,'#185fa5'],[0.8,'#457b9d'],[1.0,'#a8d4f5']],
        'highlight_states': ['CA','NY','TX','FL','WA','MA','IL'],
        'highlight_label': 'High-income metro states where established buyers thrived post-crisis',
        'colorbar_title': 'Loans',
        'map_note': "🔵 Highlighted states concentrate the highest median approved borrower incomes — the markets where David's profile thrived. The crisis filtered out lower-income competition, leaving these metros even more skewed toward high-income buyers by 2014.",
    },
    'veteran': {
        'colorscale': [[0.0,'#04110d'],[0.3,'#083327'],[0.6,'#0f6e56'],[0.8,'#2a9d8f'],[1.0,'#80e0cf']],
        'highlight_states': ['TX','CA','FL','VA','NC','GA','WA'],
        'highlight_label': 'States with largest veteran populations and highest VA loan uptake',
        'colorbar_title': 'Loans',
        'map_note': '🟢 Highlighted states drove the VA loan boom. Texas, California, Florida, and Virginia alone account for nearly half of all VA-backed originations. As private lending collapsed, these states saw veterans become an outsized share of active homebuyers.',
    },
    'fha_buyer': {
        'colorscale': [[0.0,'#1a1100'],[0.3,'#4a2e00'],[0.6,'#854f0b'],[0.8,'#f4a261'],[1.0,'#ffd9a8']],
        'highlight_states': ['CA','TX','FL','AZ','NV','GA','IL'],
        'highlight_label': 'States with highest FHA loan concentration after the crash',
        'colorbar_title': 'Loans',
        'map_note': "🟡 Highlighted states saw the greatest surge in FHA-insured lending post-2008. Sunbelt states hit hardest by the crash — Arizona and Nevada especially — became almost entirely FHA-dependent for new buyers. For Maria, the FHA was the only door left open.",
    },
    'refinancer': {
        'colorscale': [[0.0,'#0d0415'],[0.3,'#2e0d4a'],[0.6,'#5a2080'],[0.8,'#7b2d8b'],[1.0,'#d4a8f5']],
        'highlight_states': ['CA','FL','NV','AZ','MI','OH','IL'],
        'highlight_label': 'States where refinancing dominated mortgage activity 2009–2013',
        'colorbar_title': 'Loans',
        'map_note': '🟣 Highlighted states were the epicentre of the refinancing wave. California and Florida — where home values crashed furthest — saw refinancing activity peak above 70% of all mortgage originations. The market looked active. Millions of Sandras were just holding on.',
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# CHARACTER DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
CHARACTERS = {
    'first_time': {
        'emoji': '🧑🏾', 'name': 'Marcus', 'role': 'First-Time Homebuyer',
        'tagline': 'Working hard, dreaming big — but the market has other plans.',
        'color': COLORS['red'],
        'beats': [
            {'year':2007,'title':'You have a real shot','body':'First-time buyers from underserved communities make up a meaningful share of the market. The boom is real. Marcus saves up and starts looking.','tone':'hopeful'},
            {'year':2008,'title':'The crash hits everyone','body':'Lehman Brothers collapses. Banks panic. 1.7 million fewer mortgages are funded nationwide. Marcus waits and hopes.','tone':'warning'},
            {'year':2009,'title':'The numbers look better — but not for you','body':"Total applications surge back up. But borrowers from underserved communities drop to nearly half their pre-crisis share of approved loans. The so-called recovery isn't for everyone.",'tone':'bad'},
            {'year':2011,'title':'The frozen years','body':'The gap widens. First-time buyers without established wealth or credit history keep getting turned away. Marcus keeps renting.','tone':'bad'},
            {'year':2014,'title':'A small window opens','body':'Home purchases finally overtake refinancing. Approval rates slowly tick up. Marcus finally gets approved — but his loan amount is significantly lower than the market average.','tone':'neutral'},
            {'year':2017,'title':'The market recovered. Not everyone did.','body':"Underserved borrowers never returned to their pre-crisis share of the market. The gap that opened in 2008 never fully closed. The market came back. The equality didn't.",'tone':'bad'},
        ],
        'chart_focus': 'race',
        'key_stat': '8.2% → 4.4%',
        'key_label': 'Share of approvals for underserved borrowers dropped',
        'takeaway': "The data shows clearly: borrowers from underserved communities saw their share of approved mortgages cut nearly in half during the crisis — and never fully recovered. By 2017 the gap from 2007 still hadn't closed. The market healed. The access gap didn't.",
    },
    'established': {
        'emoji': '👨‍💼', 'name': 'David', 'role': 'The Established Buyer',
        'tagline': 'The crisis was a headline. For David, it was barely a pause.',
        'color': COLORS['blue'],
        'beats': [
            {'year':2007,'title':'The market is yours','body':'David earns well above the median. Banks compete for borrowers like him. He buys his first investment property.','tone':'hopeful'},
            {'year':2008,'title':'Things tighten — but you qualify','body':"The crash hits. Banks get selective. But David's income and credit score keep him in the approved tier. He watches, then acts.",'tone':'neutral'},
            {'year':2010,'title':'You refinance and win','body':'Interest rates crash to near zero. David refinances and cuts his monthly payment by hundreds of dollars. He uses the savings to invest again.','tone':'hopeful'},
            {'year':2013,'title':'The recovery is your playground','body':'The median approved borrower income has risen significantly — the crisis quietly filtered out lower-income competition. Less competition means better deals for David.','tone':'hopeful'},
            {'year':2016,'title':'Peak recovery','body':"Median loan amounts hit $210K. David's properties have appreciated substantially since 2009. For established buyers, the crisis created generational wealth.",'tone':'hopeful'},
            {'year':2017,'title':'The new normal works for you','body':'The higher income bar post-crisis filters out competition. The new mortgage market quietly rewards those who were already stable.','tone':'hopeful'},
        ],
        'chart_focus': 'income',
        'key_stat': '+18%',
        'key_label': 'Rise in median approved borrower income',
        'takeaway': "For high-income, established buyers the crisis was a temporary inconvenience that became a long-term advantage. Rising income requirements filtered out competition. Lower rates meant cheaper borrowing. The data shows the new mortgage market disproportionately rewarded those who were already financially stable.",
    },
    'veteran': {
        'emoji': '🪖', 'name': 'James', 'role': 'Military Veteran',
        'tagline': 'When private lenders fled, the VA stayed. So did James.',
        'color': COLORS['green'],
        'beats': [
            {'year':2007,'title':'VA loans are a niche product','body':'VA-guaranteed loans make up just 1.7% of the mortgage market. James returns from deployment and starts thinking about buying a home.','tone':'neutral'},
            {'year':2008,'title':"Private lenders run. The VA doesn't.",'body':'The crash hits. Conventional lending collapses from 92% to 74% of the market. But VA loans hold steady — the government guarantee means lenders keep approving veterans.','tone':'hopeful'},
            {'year':2010,'title':'Your loan type becomes a lifeline','body':'VA loans grow to 4.5% of the market. As banks tighten for everyone else, veterans with VA backing find doors still open.','tone':'hopeful'},
            {'year':2013,'title':'The quiet expansion','body':'VA loans reach 7.2%. The VA program becomes one of the few pathways for working-class buyers to still access homeownership during the slow recovery.','tone':'hopeful'},
            {'year':2015,'title':'Veterans lead the way','body':"VA loans hit 9.7%. More veterans are buying homes than at any point in the dataset's history. The crisis inadvertently supercharged a government program.",'tone':'hopeful'},
            {'year':2017,'title':'From 1.7% to 10.6% — a transformation','body':'VA loans now represent 10.6% of all mortgages — a 6x increase from 2007. The crisis accidentally made veteran homeownership stronger than ever.','tone':'hopeful'},
        ],
        'chart_focus': 'va',
        'key_stat': '1.7% → 10.6%',
        'key_label': 'VA loan share — a 6x increase',
        'takeaway': "The VA loan program was the quiet winner of the crisis decade. From 1.7% to 10.6% of all mortgages — a transformation nobody headlined. The government guarantee meant veterans could buy homes when private lenders shut everyone else out.",
    },
    'fha_buyer': {
        'emoji': '👩‍👧', 'name': 'Maria', 'role': 'First-Generation FHA Borrower',
        'tagline': 'Lower income, first-time buyer — navigating a system not built for her.',
        'color': COLORS['gold'],
        'beats': [
            {'year':2007,'title':'FHA is a small safety net','body':'FHA loans — designed for lower-income, first-time buyers — make up just 6% of mortgages. Maria is saving up but the conventional market feels out of reach.','tone':'neutral'},
            {'year':2008,'title':'The crash reshapes everything','body':"Conventional lenders pull back. FHA loans triple overnight to 22% of the market. Suddenly the safety net becomes the main rope. Maria's path gets clearer — unexpectedly.",'tone':'hopeful'},
            {'year':2009,'title':'FHA keeps the dream alive','body':'Without FHA, the housing market would have completely frozen for buyers like Maria. The government backstop holds the door open for first-generation buyers.','tone':'hopeful'},
            {'year':2011,'title':'Single-income households face the squeeze','body':'Female borrowers drop from 30.7% to 25.7% of approved loans. Single-income households face disproportionate scrutiny. Maria gets rejected twice before finding a path forward.','tone':'bad'},
            {'year':2014,'title':'A real opening','body':'Home purchases finally dominate refinancing again. FHA lending stabilizes. Maria gets approved — her persistence pays off.','tone':'hopeful'},
            {'year':2017,'title':'You made it — but the system is still harder for you','body':'FHA loans settle at 18.6% — permanently higher than pre-crisis levels. The conventional market never fully reopened for lower-income buyers. Maria owns her home. The barriers remain for the next Maria.','tone':'neutral'},
        ],
        'chart_focus': 'fha',
        'key_stat': '6% → 22%',
        'key_label': 'FHA loan share after the crash',
        'takeaway': "FHA loans went from a niche product to a lifeline overnight. Without them, the housing market would have completely frozen for lower and middle-income Americans. But female borrowers dropped from 30.7% to 25.7% during the crisis and never fully recovered — showing that single-income households faced disproportionate barriers.",
    },
    'refinancer': {
        'emoji': '🏠', 'name': 'Sandra', 'role': 'Existing Homeowner',
        'tagline': "She didn't lose her home. But she spent a decade clinging to it.",
        'color': COLORS['purple'],
        'beats': [
            {'year':2007,'title':'Life is stable','body':'Sandra bought her home in 2004. Mortgage payments are manageable. The market hums along.','tone':'hopeful'},
            {'year':2008,'title':'Fear sets in','body':"The crash hits. Sandra's home value drops 20%. She can't sell. She can't move. She can only hold on.",'tone':'warning'},
            {'year':2009,'title':'The Fed saves you — temporarily','body':"Interest rates drop to near zero. Refinancing surges to 67% of all mortgage activity. Sandra refinances and cuts her monthly payment. The market looks like it's recovering. It isn't.",'tone':'hopeful'},
            {'year':2011,'title':'Still clinging','body':"Refinancing stays above 64%. Sandra refinances again. From the outside the market looks active. But it's millions of Sandras treading water — not new buyers buying homes.",'tone':'neutral'},
            {'year':2013,'title':'The illusion starts to crack','body':'Refinancing still dominates at 60.9%. Interest rates begin rising. The wave that disguised the frozen market is about to end.','tone':'warning'},
            {'year':2014,'title':'The illusion ends — the real recovery begins','body':"Home purchases jump to 56.6% — overtaking refinancing for the first time since 2007. Sandra's home value has recovered. She can finally think about the future. The real recovery was always 2014, not 2009.",'tone':'hopeful'},
        ],
        'chart_focus': 'refi',
        'key_stat': '67%',
        'key_label': 'Of all 2009 mortgages were refinancing — not buying',
        'takeaway': "67% of 2009 mortgages were refinancing. The market looked alive. It wasn't. Sandra's story is the story of millions of Americans who survived the crisis not by moving forward — but by holding on. The real recovery didn't begin until 2014 when home purchases finally overtook refinancing.",
    },
}
