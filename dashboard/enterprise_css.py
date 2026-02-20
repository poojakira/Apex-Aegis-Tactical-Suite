"""Enterprise-grade CSS theme for Apex-X dashboards."""

ENTERPRISE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #05070e;
    --bg-secondary: #0b0e18;
    --bg-card: rgba(12, 16, 28, 0.85);
    --border-glass: rgba(0, 210, 255, 0.12);
    --accent-cyan: #00d2ff;
    --accent-blue: #3a7bd5;
    --accent-green: #00e676;
    --accent-red: #ff1744;
    --accent-amber: #ffab00;
    --accent-purple: #b388ff;
    --text-primary: #e8eaf6;
    --text-secondary: #8892b0;
    --glow-cyan: 0 0 20px rgba(0, 210, 255, 0.25);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b14 0%, #0d1020 100%) !important;
    border-right: 1px solid var(--border-glass) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem;
}

h1 {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

h2, h3 {
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
}

/* Glassmorphism Metric Cards */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    box-shadow: var(--glow-cyan), inset 0 1px 0 rgba(255,255,255,0.04);
    transition: transform 0.2s ease, box-shadow 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(0, 210, 255, 0.35);
}
[data-testid="stMetric"] label { color: var(--text-secondary) !important; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.2px; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-weight: 700; font-size: 1.8rem; }
[data-testid="stMetric"] [data-testid="stMetricDelta"] svg { display: none; }

/* Premium Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 50%, var(--accent-purple) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 0.8rem !important;
    box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    box-shadow: 0 6px 25px rgba(0, 210, 255, 0.5);
    transform: translateY(-1px);
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-card);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border-glass);
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    font-weight: 500;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,210,255,0.15), rgba(58,123,213,0.15)) !important;
    color: var(--accent-cyan) !important;
}

/* Data Containers */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
}

/* Text Areas & Code Blocks */
.stTextArea textarea, .stCodeBlock {
    background: rgba(5, 7, 14, 0.9) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 8px !important;
    color: var(--accent-cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem;
}

/* Alert Boxes */
.stAlert { border-radius: 12px !important; border: 1px solid var(--border-glass) !important; backdrop-filter: blur(8px); }

/* Progress Bars */
.stProgress > div > div { background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue)) !important; border-radius: 8px; }
.stProgress { background: rgba(255,255,255,0.05) !important; border-radius: 8px; }

/* Plotly Dark Override */
.js-plotly-plot { border-radius: 12px; overflow: hidden; border: 1px solid var(--border-glass); }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent-blue); border-radius: 3px; }

/* Status Badges */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-online { background: rgba(0,230,118,0.15); color: var(--accent-green); border: 1px solid rgba(0,230,118,0.3); }
.badge-alert { background: rgba(255,23,68,0.15); color: var(--accent-red); border: 1px solid rgba(255,23,68,0.3); }
.badge-warning { background: rgba(255,171,0,0.15); color: var(--accent-amber); border: 1px solid rgba(255,171,0,0.3); }

/* Header Bar */
.enterprise-header {
    background: linear-gradient(90deg, rgba(0,210,255,0.08) 0%, rgba(58,123,213,0.08) 50%, rgba(179,136,255,0.08) 100%);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    padding: 16px 24px;
    margin-bottom: 24px;
}

/* Event Log */
.event-log {
    background: rgba(5,7,14,0.9);
    border: 1px solid var(--border-glass);
    border-radius: 12px;
    padding: 16px;
    max-height: 300px;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}
.event-log .ev-info { color: var(--accent-cyan); }
.event-log .ev-warn { color: var(--accent-amber); }
.event-log .ev-crit { color: var(--accent-red); }
.event-log .ev-ok { color: var(--accent-green); }
.event-log .ev-time { color: var(--text-secondary); margin-right: 8px; }

/* AI Chat Bot Styles */
.chat-container {
    background: var(--bg-card);
    border: 1px solid var(--border-glass);
    border-radius: 12px;
    padding: 12px;
    height: 350px;
    overflow-y: auto;
    margin-bottom: 12px;
}
.chat-msg {
    margin-bottom: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.8rem;
}
.msg-bot {
    background: rgba(0, 210, 255, 0.1);
    border: 1px solid rgba(0, 210, 255, 0.2);
    color: var(--text-primary);
}
.msg-user {
    background: rgba(179, 136, 255, 0.1);
    border: 1px solid rgba(179, 136, 255, 0.2);
    color: var(--accent-purple);
    text-align: right;
}

/* Report Styles */
.report-preview {
    background: #fff;
    color: #333;
    padding: 40px;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
}

/* Glowing Animation */
@keyframes pulse-glow {
    0% { box-shadow: 0 0 10px rgba(0, 210, 255, 0.2); }
    50% { box-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    100% { box-shadow: 0 0 10px rgba(0, 210, 255, 0.2); }
}
.glow-box {
    animation: pulse-glow 3s infinite ease-in-out;
}
</style>
"""

PLOTLY_DARK_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor='rgba(5,7,14,0)',
        plot_bgcolor='rgba(12,16,28,0.6)',
        font=dict(family='Inter, sans-serif', color='#8892b0', size=12),  # pyre-ignore[6]
        title_font=dict(color='#e8eaf6', size=16, family='Inter, sans-serif'),  # pyre-ignore[6]
        xaxis=dict(gridcolor='rgba(0,210,255,0.06)', zerolinecolor='rgba(0,210,255,0.1)'),
        yaxis=dict(gridcolor='rgba(0,210,255,0.06)', zerolinecolor='rgba(0,210,255,0.1)'),
        colorway=['#00d2ff','#3a7bd5','#b388ff','#00e676','#ffab00','#ff1744','#76ff03'],
        margin=dict(l=40, r=20, t=50, b=40),
    )
)
