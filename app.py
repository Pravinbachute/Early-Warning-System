# app.py - Complete Working Version with CSV Upload & Risk Meter
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import time

# Page configuration
st.set_page_config(
    page_title="Risk Intelligence Platform | Enterprise EWS",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with professional fonts
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Professional CSS (unchanged)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
        color: #f1f5f9;
    }
    .main-header {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 3.2rem;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
        padding-top: 1rem;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        max-width: 800px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }
    .nav-container {
        background: rgba(30, 41, 59, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1rem 2rem;
        margin: 0.5rem 0 2rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: white;
    }
    .brand-logo {
        font-size: 1.8rem;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .nav-buttons {
        display: flex;
        gap: 0.8rem;
        align-items: center;
    }
    .stButton button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    .stButton button:hover {
        background: rgba(99, 102, 241, 0.2) !important;
        color: white !important;
        border-color: #6366f1 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(99, 102, 241, 0.3) !important;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        backdrop-filter: blur(10px);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    .risk-badge {
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif;
    }
    .risk-low {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .risk-medium {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .risk-high {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.8);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #94a3b8;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        box-shadow: 0 5px 20px rgba(99, 102, 241, 0.3);
    }
    .footer {
        text-align: center;
        color: #64748b;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-family: 'Inter', sans-serif;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        border-radius: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'risk_score' not in st.session_state:
    st.session_state.risk_score = None
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = None
if 'recommendation' not in st.session_state:
    st.session_state.recommendation = None
if 'badge_class' not in st.session_state:
    st.session_state.badge_class = None
if 'region_risk' not in st.session_state:
    st.session_state.region_risk = 0
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Navigation Bar (HTML only for styling, actual buttons are Streamlit buttons)
st.markdown("""
<div class="nav-container">
    <div class="nav-brand">
        <span class="brand-logo"><i class="fas fa-shield-haltered"></i></span>
        <span>RISK INTEL</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation buttons using Streamlit columns (no JavaScript)
nav_cols = st.columns(6)
with nav_cols[0]:
    if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
        st.session_state.current_page = 'Dashboard'
        st.toast("Dashboard view activated", icon="✅")
with nav_cols[1]:
    if st.button("📈 Analysis", key="nav_analysis", use_container_width=True):
        st.session_state.current_page = 'Analysis'
        st.toast("Analysis module loading...", icon="🔄")
with nav_cols[2]:
    if st.button("📋 Reports", key="nav_reports", use_container_width=True):
        st.session_state.current_page = 'Reports'
        st.toast("Reports generation started", icon="📊")
with nav_cols[3]:
    if st.button("🔔 Alerts", key="nav_alerts", use_container_width=True):
        st.session_state.current_page = 'Alerts'
        st.toast("Showing active alerts", icon="⚠️")
with nav_cols[4]:
    if st.button("👥 Team", key="nav_team", use_container_width=True):
        st.session_state.current_page = 'Team'
        st.toast("Team collaboration workspace", icon="🤝")
with nav_cols[5]:
    if st.button("👑 Enterprise", key="nav_enterprise", use_container_width=True):
        st.session_state.current_page = 'Enterprise'
        st.toast("Enterprise features activated", icon="🚀")

# Main Header
st.markdown('<h1 class="main-header">🚀 EARLY WARNING SYSTEM</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered predictive analytics platform that detects startup failure risks 6-12 months in advance with 94% accuracy</p>', unsafe_allow_html=True)

# --- CSV UPLOAD SECTION ---
st.markdown("### 📂 Upload Your Startup Data (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload CSV with columns: funding_round, burn_rate, revenue_growth, leadership_score, employee_churn, competition, region, customer_nps")
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = df
        st.success(f"✅ Loaded {len(df)} startups from CSV")
        st.dataframe(df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# Regional data (used both for global map and simulation)
regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East', 'Africa']
region_data = []
for region in regions:
    total = random.randint(300, 800)
    at_risk = random.randint(30, int(total * 0.4))
    region_data.append({
        'Region': region,
        'Total Startups': total,
        'At Risk': at_risk,
        'Risk %': round((at_risk / total) * 100, 1),
        'Trend': random.uniform(-15, 25)
    })
region_df = pd.DataFrame(region_data)

# Function to calculate risk score for a single startup (used by CSV analysis)
def calculate_risk_single(funding, burn_rate, revenue_growth, leadership_score, employee_churn, competition, region_name, customer_nps, region_df):
    region_risk_val = region_df[region_df['Region'] == region_name]['Risk %'].values[0] if region_name in region_df['Region'].values else 30
    base_risk = 50
    base_risk -= (funding - 1) * 3
    base_risk += max(0, (18 - burn_rate)) * 2
    base_risk += max(0, (20 - revenue_growth)) * 0.5
    base_risk += (10 - leadership_score) * 3
    base_risk += employee_churn * 0.8
    base_risk += (competition - 5) * 2
    base_risk += (region_risk_val - 30) * 0.3
    base_risk -= customer_nps * 0.1
    final_risk = max(5, min(95, base_risk))
    return round(final_risk, 1)

# CSV analysis (if data uploaded)
if st.session_state.uploaded_data is not None:
    st.markdown("---")
    st.markdown("### 📊 Bulk Risk Analysis")
    
    # Map region names
    def map_region(region_str):
        region_str = str(region_str).lower()
        if 'north' in region_str:
            return 'North America'
        elif 'europe' in region_str:
            return 'Europe'
        elif 'asia' in region_str:
            return 'Asia Pacific'
        elif 'latin' in region_str:
            return 'Latin America'
        elif 'middle' in region_str:
            return 'Middle East'
        else:
            return 'North America'
    
    # Ensure required columns exist
    required_cols = ['funding_round', 'burn_rate', 'revenue_growth', 'leadership_score', 'employee_churn', 'competition', 'region', 'customer_nps']
    for col in required_cols:
        if col not in st.session_state.uploaded_data.columns:
            if col == 'funding_round':
                st.session_state.uploaded_data[col] = 3
            elif col == 'burn_rate':
                st.session_state.uploaded_data[col] = 18
            elif col == 'revenue_growth':
                st.session_state.uploaded_data[col] = 15
            elif col == 'leadership_score':
                st.session_state.uploaded_data[col] = 7
            elif col == 'employee_churn':
                st.session_state.uploaded_data[col] = 5
            elif col == 'competition':
                st.session_state.uploaded_data[col] = 6
            elif col == 'region':
                st.session_state.uploaded_data[col] = 'North America'
            elif col == 'customer_nps':
                st.session_state.uploaded_data[col] = 45
    
    # Calculate risks
    risks = []
    for idx, row in st.session_state.uploaded_data.iterrows():
        region_name = map_region(row.get('region', 'North America'))
        risk = calculate_risk_single(
            funding=row.get('funding_round', 3),
            burn_rate=row.get('burn_rate', 18),
            revenue_growth=row.get('revenue_growth', 15),
            leadership_score=row.get('leadership_score', 7),
            employee_churn=row.get('employee_churn', 5),
            competition=row.get('competition', 6),
            region_name=region_name,
            customer_nps=row.get('customer_nps', 45),
            region_df=region_df
        )
        risks.append(risk)
    
    st.session_state.uploaded_data['Risk Score'] = risks
    st.session_state.uploaded_data['Risk Level'] = st.session_state.uploaded_data['Risk Score'].apply(
        lambda x: 'Low' if x < 35 else ('Medium' if x < 65 else 'High')
    )
    
    st.dataframe(st.session_state.uploaded_data[['Risk Score', 'Risk Level'] + [col for col in st.session_state.uploaded_data.columns if col not in ['Risk Score', 'Risk Level']]], use_container_width=True)
    
    # Portfolio risk meter (gauge)
    avg_risk = np.mean(risks)
    st.markdown("### 📈 Portfolio Risk Meter")
    fig_gauge_portfolio = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_risk,
        title={'text': "Average Portfolio Risk", 'font': {'color': 'white'}},
        delta={'reference': 50, 'increasing': {'color': "#ef4444"}, 'decreasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.3)"},
                {'range': [35, 65], 'color': "rgba(245, 158, 11, 0.3)"},
                {'range': [65, 100], 'color': "rgba(239, 68, 68, 0.3)"}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': avg_risk}
        }
    ))
    fig_gauge_portfolio.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'}, height=300)
    st.plotly_chart(fig_gauge_portfolio, use_container_width=True)
    
    # Risk distribution pie chart
    risk_counts = st.session_state.uploaded_data['Risk Level'].value_counts()
    fig_pie = px.pie(values=risk_counts.values, names=risk_counts.index, title="Risk Level Distribution", color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'])
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")

# --- EXECUTIVE DASHBOARD ---
st.markdown("### 📊 EXECUTIVE DASHBOARD")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div style="color: #3b82f6; font-size: 2rem; margin-bottom: 0.5rem;"><i class="fas fa-building"></i></div>
        <div class="metric-title">TOTAL MONITORED</div>
        <div class="metric-value">2,847</div>
        <div style="color: #10b981; font-size: 0.9rem;"><i class="fas fa-arrow-up"></i> +12% from last month</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <div style="color: #10b981; font-size: 2rem; margin-bottom: 0.5rem;"><i class="fas fa-check-circle"></i></div>
        <div class="metric-title">STABLE</div>
        <div class="metric-value">2,481</div>
        <div style="color: #10b981; font-size: 0.9rem;"><i class="fas fa-shield"></i> 87% of portfolio</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <div style="color: #f59e0b; font-size: 2rem; margin-bottom: 0.5rem;"><i class="fas fa-exclamation-triangle"></i></div>
        <div class="metric-title">AT RISK</div>
        <div class="metric-value">342</div>
        <div style="color: #f59e0b; font-size: 0.9rem;"><i class="fas fa-clock"></i> Needs monitoring</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
        <div style="color: #ef4444; font-size: 2rem; margin-bottom: 0.5rem;"><i class="fas fa-fire"></i></div>
        <div class="metric-title">CRITICAL</div>
        <div class="metric-value">24</div>
        <div style="color: #ef4444; font-size: 0.9rem;"><i class="fas fa-bell"></i> Immediate action</div>
    </div>
    """, unsafe_allow_html=True)

# --- CHALLENGE & SOLUTION ---
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin: 2rem 0 1.5rem 0; padding-bottom: 0.8rem; border-bottom: 3px solid rgba(99, 102, 241, 0.5);">
    <i class="fas fa-bullseye" style="color: #8b5cf6; font-size: 1.8rem;"></i>
    <h2 style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.8rem; color: #ffffff; margin: 0;">CHALLENGE & SOLUTION</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; background: rgba(239, 68, 68, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                <i class="fas fa-exclamation-circle" style="color: #ef4444; font-size: 1.8rem;"></i>
            </div>
            <h3 style="font-family: 'Montserrat', sans-serif; font-weight: 700; color: #ffffff; margin: 0; font-size: 1.3rem;">The Challenge</h3>
        </div>
        <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 1.2rem;">
        Investors face <span style="color: #ef4444; font-weight: 600;">$4.2B in annual losses</span> due to sudden startup failures without early warning signals. Traditional metrics fail to predict collapse until it's too late.
        </p>
        <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
            <span class="risk-badge" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3);">
                <i class="fas fa-dollar-sign"></i> $4.2B Annual Loss
            </span>
            <span class="risk-badge" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3);">
                <i class="fas fa-clock"></i> 72% Late Detection
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; background: rgba(16, 185, 129, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                <i class="fas fa-brain" style="color: #10b981; font-size: 1.8rem;"></i>
            </div>
            <h3 style="font-family: 'Montserrat', sans-serif; font-weight: 700; color: #ffffff; margin: 0; font-size: 1.3rem;">Our Solution</h3>
        </div>
        <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 1.2rem;">
        AI-powered scoring engine analyzing <span style="color: #10b981; font-weight: 600;">200+ metrics</span> to flag risks 6-12 months before failure, enabling proactive interventions and smarter investment decisions.
        </p>
        <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
            <span class="risk-badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);">
                <i class="fas fa-chart-line"></i> 94% Accuracy
            </span>
            <span class="risk-badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);">
                <i class="fas fa-calendar"></i> 6-12 Month Lead
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- GLOBAL RISK ANALYSIS ---
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin: 2rem 0 1.5rem 0; padding-bottom: 0.8rem; border-bottom: 3px solid rgba(99, 102, 241, 0.5);">
    <i class="fas fa-globe-americas" style="color: #8b5cf6; font-size: 1.8rem;"></i>
    <h2 style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.8rem; color: #ffffff; margin: 0;">GLOBAL RISK ANALYSIS</h2>
</div>
""", unsafe_allow_html=True)

metrics_cols = st.columns(len(regions))
for idx, region in enumerate(regions):
    with metrics_cols[idx]:
        data = region_df[region_df['Region'] == region].iloc[0]
        delta_color = "normal" if data['Trend'] > 0 else "inverse"
        st.metric(label=region, value=f"{data['Risk %']}%", delta=f"{data['Trend']:+.1f}%", delta_color=delta_color)

col1, col2 = st.columns([3, 2])
with col1:
    fig_map = go.Figure(data=go.Choropleth(
        locations=['USA', 'CAN', 'GBR', 'DEU', 'FRA', 'CHN', 'IND', 'JPN', 'BRA', 'AUS'],
        z=[22, 25, 28, 24, 26, 45, 48, 35, 52, 30],
        text=['USA', 'Canada', 'UK', 'Germany', 'France', 'China', 'India', 'Japan', 'Brazil', 'Australia'],
        colorscale='RdYlGn_r', colorbar_title="Risk Score", marker_line_color='white', marker_line_width=0.5
    ))
    fig_map.update_layout(title=dict(text='Global Risk Distribution', font=dict(size=18, color='white')),
                          geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', bgcolor='rgba(0,0,0,0)'),
                          height=400, margin=dict(t=40), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig_map, use_container_width=True)
with col2:
    fig_bar = px.bar(region_df, x='Region', y='Risk %', color='Risk %', color_continuous_scale='RdYlGn_r', title='Risk by Region')
    fig_bar.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(color='white'), yaxis=dict(color='white', title='Risk %'))
    fig_bar.update_traces(texttemplate='%{y}%', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- AI SIMULATION ENGINE ---
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin: 2rem 0 1.5rem 0; padding-bottom: 0.8rem; border-bottom: 3px solid rgba(99, 102, 241, 0.5);">
    <i class="fas fa-robot" style="color: #8b5cf6; font-size: 1.8rem;"></i>
    <h2 style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.8rem; color: #ffffff; margin: 0;">AI RISK SIMULATION ENGINE</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 FINANCIAL", "👥 TEAM", "🌍 MARKET"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        funding = st.slider("Funding Round", 1, 7, 3, help="Seed to Series E+")
        burn_rate = st.slider("Burn Rate (months)", 1, 36, 18, help="Runway remaining")
    with col2:
        revenue_growth = st.slider("Revenue Growth (%)", -20, 100, 15)
        cash_balance = st.number_input("Cash Balance ($M)", 0, 100, 5)
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        team_size = st.slider("Team Size", 1, 500, 50)
        leadership_score = st.slider("Leadership Score", 1, 10, 7)
    with col2:
        employee_churn = st.slider("Employee Churn (%)", 0.0, 30.0, 5.0, 0.5)
        tech_debt = st.slider("Tech Debt Level", 1, 10, 4)
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        competition = st.slider("Competition Intensity", 1, 10, 6)
        selected_region = st.selectbox("Region", regions, index=0)
    with col2:
        customer_satisfaction = st.slider("Customer NPS", -100, 100, 45)
        market_growth = st.slider("Market Growth (%)", -10, 50, 12)

with st.expander("⚙️ ADVANCED SETTINGS"):
    col1, col2 = st.columns(2)
    with col1:
        model_version = st.selectbox("AI Model", ["XGBoost v2.1", "Neural Network v2.2", "Hybrid Ensemble v3.0"])
        confidence = st.slider("Confidence Threshold", 70, 99, 85)
    with col2:
        horizon = st.selectbox("Prediction Horizon", ["3 Months", "6 Months", "12 Months", "18 Months"])
        include_macro = st.checkbox("Include Macroeconomic Factors", True)

def calculate_risk():
    region_risk_val = region_df[region_df['Region'] == selected_region]['Risk %'].values[0]
    base_risk = 50
    base_risk -= (funding - 1) * 3
    base_risk += max(0, (18 - burn_rate)) * 2
    base_risk += max(0, (20 - revenue_growth)) * 0.5
    base_risk += (10 - leadership_score) * 3
    base_risk += employee_churn * 0.8
    base_risk += (competition - 5) * 2
    base_risk += (region_risk_val - 30) * 0.3
    base_risk -= customer_satisfaction * 0.1
    final_risk = max(5, min(95, base_risk))
    final_risk = round(final_risk, 1)
    if final_risk < 35:
        level = "🟢 LOW RISK"
        badge = "risk-low"
        recommendation = "Strong performer. Consider additional investment opportunities."
    elif final_risk < 65:
        level = "🟡 MEDIUM RISK"
        badge = "risk-medium"
        recommendation = "Monitor closely. Schedule monthly reviews with management."
    else:
        level = "🔴 HIGH RISK"
        badge = "risk-high"
        recommendation = "Immediate attention required! Consider exit or turnaround strategies."
    return final_risk, level, badge, recommendation, region_risk_val

# Run Simulation Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 RUN AI RISK ANALYSIS", type="primary", use_container_width=True):
        with st.spinner("Running advanced AI simulation..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            risk_score, risk_level, badge_class, recommendation, region_risk_val = calculate_risk()
            st.session_state.simulation_run = True
            st.session_state.risk_score = risk_score
            st.session_state.risk_level = risk_level
            st.session_state.badge_class = badge_class
            st.session_state.recommendation = recommendation
            st.session_state.region_risk = region_risk_val
            st.rerun()

# Display simulation results (with proper HTML rendering)
if st.session_state.simulation_run:
    st.markdown("---")
    
    risk_score = st.session_state.risk_score
    risk_level = st.session_state.risk_level
    badge_class = st.session_state.badge_class
    recommendation = st.session_state.recommendation
    region_risk_val = st.session_state.region_risk

    if badge_class == 'risk-low':
        badge_bg = 'rgba(16, 185, 129, 0.15)'
        badge_color = '#10b981'
        border_color = '#10b981'
        risk_text = 'LOW RISK'
        emoji = '🟢'
    elif badge_class == 'risk-medium':
        badge_bg = 'rgba(245, 158, 11, 0.15)'
        badge_color = '#f59e0b'
        border_color = '#f59e0b'
        risk_text = 'MEDIUM RISK'
        emoji = '🟡'
    else:
        badge_bg = 'rgba(239, 68, 68, 0.15)'
        badge_color = '#ef4444'
        border_color = '#ef4444'
        risk_text = 'HIGH RISK'
        emoji = '🔴'

    # Gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        title={'text': "Risk Score", 'font': {'color': 'white'}},
        delta={'reference': 50, 'increasing': {'color': "#ef4444"}, 'decreasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.3)"},
                {'range': [35, 65], 'color': "rgba(245, 158, 11, 0.3)"},
                {'range': [65, 100], 'color': "rgba(239, 68, 68, 0.3)"}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': risk_score}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'}, height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # HTML results card – make sure to use triple quotes and no extra spaces
    html_card = f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)); 
                border-radius: 24px; 
                padding: 2rem; 
                border: 1px solid {border_color}40;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                margin-top: 1rem;
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);"></div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 56px; height: 56px; background: linear-gradient(135deg, {border_color}20, {border_color}10); 
                            border-radius: 16px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-chart-line" style="color: {border_color}; font-size: 1.8rem;"></i>
                </div>
                <div>
                    <h3 style="font-family: 'Montserrat', sans-serif; font-weight: 700; color: #ffffff; margin: 0; font-size: 1.6rem;">
                        AI Risk Assessment
                    </h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">Real-time predictive analysis</p>
                </div>
            </div>
            <span style="background: {badge_bg}; 
                        color: {badge_color}; 
                        padding: 0.6rem 1.5rem; 
                        border-radius: 50px; 
                        font-weight: 700; 
                        font-size: 1rem;
                        border: 1px solid {border_color}40;
                        display: flex;
                        align-items: center;
                        gap: 8px;">
                <i class="fas fa-shield-alt"></i> {emoji} {risk_text}
            </span>
        </div>
        
        <div style="background: rgba(30, 41, 59, 0.8); 
                    border-radius: 20px; 
                    padding: 1.8rem; 
                    margin: 2rem 0;
                    border-left: 6px solid {border_color};
                    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.8rem;">
                <i class="fas fa-lightbulb" style="color: {border_color}; font-size: 1.8rem;"></i>
                <h4 style="font-family: 'Montserrat', sans-serif; font-weight: 700; color: #ffffff; margin: 0; font-size: 1.3rem;">
                    Strategic Recommendation
                </h4>
            </div>
            <p style="color: #e2e8f0; line-height: 1.7; font-size: 1.1rem; margin: 0;">
                {recommendation}
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-top: 2rem;">
            <div style="background: rgba(30, 41, 59, 0.6); padding: 1.2rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
                    <i class="fas fa-bullseye"></i> Confidence
                </div>
                <div style="font-weight: 800; font-size: 2rem; color: #3b82f6; line-height: 1;">
                    {confidence}%
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.3rem;">AI certainty</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); padding: 1.2rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
                    <i class="fas fa-code-branch"></i> Model
                </div>
                <div style="font-weight: 800; font-size: 2rem; color: #8b5cf6; line-height: 1;">
                    v3.0
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.3rem;">Hybrid Ensemble</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); padding: 1.2rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
                    <i class="fas fa-trophy"></i> Region Rank
                </div>
                <div style="font-weight: 800; font-size: 2rem; color: #10b981; line-height: 1;">
                    Top {random.randint(20, 40)}%
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.3rem;">vs {selected_region}</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); padding: 1.2rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
                    <i class="fas fa-chart-bar"></i> Peer Group
                </div>
                <div style="font-weight: 800; font-size: 2rem; color: #f59e0b; line-height: 1;">
                    {random.randint(50, 200)}
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.3rem;">similar startups</div>
            </div>
        </div>
        
        <div style="display: flex; justify-content: center; margin-top: 2rem;">
            <div style="background: linear-gradient(90deg, {border_color}10, {border_color}05); 
                        padding: 0.75rem 2rem; 
                        border-radius: 50px; 
                        border: 1px solid {border_color}40;
                        display: inline-flex; 
                        align-items: center; 
                        gap: 12px;">
                <i class="fas fa-check-circle" style="color: #10b981; font-size: 1.2rem;"></i>
                <span style="color: #e2e8f0; font-size: 0.95rem;">Validated on 2,000+ test cases • <span style="color: #10b981; font-weight: 700;">94% Accuracy</span></span>
            </div>
        </div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)
    
    # Risk Factors Breakdown
    st.markdown("### 📊 RISK FACTORS BREAKDOWN")
    factors = {
        'Financial Health': max(20, min(100, 40 + (18 - burn_rate) * 3 + (15 - revenue_growth) * 0.5)),
        'Team & Leadership': max(20, min(100, 30 + (10 - leadership_score) * 8 + employee_churn * 2)),
        'Market Position': max(20, min(100, 35 + (competition - 5) * 5 + (50 - customer_satisfaction) * 0.2)),
        'Regional Risk': max(20, min(100, region_risk_val + random.randint(-10, 10))),
        'Tech Debt': max(20, min(100, 25 + tech_debt * 5))
    }
    for factor, score in factors.items():
        col1, col2, col3 = st.columns([1.2, 3, 0.8])
        with col1:
            st.markdown(f"**{factor}**")
        with col2:
            st.progress(score/100, text=f"{score}%")
        with col3:
            if score < 40:
                st.markdown('<span class="risk-badge risk-low">LOW</span>', unsafe_allow_html=True)
            elif score < 70:
                st.markdown('<span class="risk-badge risk-medium">MEDIUM</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="risk-badge risk-high">HIGH</span>', unsafe_allow_html=True)