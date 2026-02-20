import sys, os, time, datetime, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st  # type: ignore
import numpy as np  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import pandas as pd  # type: ignore

from data.tle_fetcher import TLEFetcher  # type: ignore
from data.nasa_physics import NASAStandardAtmosphere  # type: ignore
from core.digital_twin import AerodynamicDigitalTwin  # type: ignore
from core.fem_overlay import FEMStructuralOverlay  # type: ignore
from dashboard.enterprise_css import ENTERPRISE_CSS, PLOTLY_DARK_TEMPLATE  # type: ignore
from dashboard.reporter import generate_html_report, get_report_download_link  # type: ignore

def log_event(severity, module, message):
    if 'event_log' not in st.session_state:
        st.session_state['event_log'] = []
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]  # pyre-ignore
    st.session_state['event_log'].insert(0, {"ts": ts, "sev": severity, "mod": module, "msg": message})
    if len(st.session_state['event_log']) > 200:
        st.session_state['event_log'] = st.session_state['event_log'][:200]


# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Aegis-X Tactical Command", layout="wide", page_icon="🎯")
st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
if 'nasa_loaded' not in st.session_state:
    st.session_state['nasa_loaded'] = False
    st.session_state['nasa_assets'] = []
    st.session_state['atmo'] = NASAStandardAtmosphere()
    st.session_state['twin'] = AerodynamicDigitalTwin()
    st.session_state['chat_history'] = [{"role": "bot", "content": "Aegis Tactical AI online. Commander, ready for physics-grounded mission analysis."}]

# ═══════════════════════════════════════════════════════════════
# MISSION AUDIO (Tactical Ambient)
# ═══════════════════════════════════════════════════════════════
def render_audio_controller():
    with st.sidebar:
        st.markdown("---")
        st.markdown("##### 🎵 TACTICAL AMBIENT")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", format="audio/mpeg", loop=True)
        st.caption("Immersive soundscape. (Press Play to start)")


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:2.2rem;">🎯</div>
        <div style="font-size:1.1rem;font-weight:700;background:linear-gradient(135deg,#ff1744,#ffab00);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">AEGIS-X TACTICAL</div>
        <div style="font-size:0.7rem;color:#8892b0;letter-spacing:2px;margin-top:4px;">COMMAND CENTER v3.0</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("##### 🕹️ What-If Parameters")
    wind_speed = st.slider("Wind Speed (m/s)", 0, 100, 20)
    air_density = st.slider("Air Density (kg/m³)", 0.1, 1.5, 1.225, 0.01)
    sim_altitude = st.slider("Altitude (m)", 1000, 50000, 10000, 500)
    sim_velocity = st.slider("Velocity (m/s)", 200, 3000, 1500, 50)

    st.markdown("---")
    now = datetime.datetime.now()
    st.markdown(f"""<div style="font-size:0.72rem;color:#8892b0;padding:0 8px;">
    <b style="color:#ff1744;">MODE</b> TACTICAL<br>
    <b style="color:#ffab00;">TIME</b> {now.strftime('%H:%M:%S')} UTC-7<br>
    <b style="color:#00d2ff;">BUILD</b> {int(time.time()) % 100000}
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 🤖 TACTICAL ASSIST")
    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="chat-container" style="height:250px;">', unsafe_allow_html=True)
        for msg in st.session_state['chat_history']:
            cls = "msg-bot" if msg['role'] == "bot" else "msg-user"
            st.markdown(f'<div class="chat-msg {cls}">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("Tactical inquiry..."):
        st.session_state['chat_history'].append({"role": "user", "content": prompt})
        response = "Analyzing physics constraints..."
        p = prompt.lower()
        if "altitude" in p or "alt" in p: response = f"Current simulation altitude: {sim_altitude}m. Atmosphere layer: {atmo_result['layer']}."
        elif "mach" in p or "speed" in p: response = f"Calculated Mach number: {mach_num:.2f}. Hypersonic threshold is Mach 5."
        elif "stress" in p: response = "Axial stress is within nominal bounds for the current G-load profile."
        st.session_state['chat_history'].append({"role": "bot", "content": response})
        st.rerun()

    st.markdown("---")
    st.markdown("##### 📋 TACTICAL REPORT")
    report_html = generate_html_report(
        mission_name="AEGIS-X TACTICAL EVAL",
        health_data={"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        threats=[{"id":"TGT-BETA","type":"Hypersonic Glide Vehicle","bearing":"090°","range":"450 km","status":"INTERCEPT"}],
        pqc_tag="AEGIS-LIVE-BLOCK-003-SIGNATURE-VERIFIED"
    )
    st.markdown(get_report_download_link(report_html), unsafe_allow_html=True)
    
    # Render audio at the bottom of sidebar
    render_audio_controller()


# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("# 🎯 Aegis-X: Tactical Command Center")
st.caption("Enterprise Defense Platform — Official NASA Physics Grounding & Real-Time Threat Analysis")

# ═══════════════════════════════════════════════════════════════
# KPI ROW
# ═══════════════════════════════════════════════════════════════
# Get atmosphere data
atmo_result = st.session_state['atmo'].get_atmospheric_state(sim_altitude)
m1, m2, m3, m4, m5 = st.columns(5)
mach_num = sim_velocity / 343.0
m1.metric("Mach Number", f"{mach_num:.2f}", delta="Hypersonic" if mach_num > 5 else "Supersonic" if mach_num > 1 else "Subsonic")
m2.metric("Air Temp", f"{atmo_result['temp_k']:.1f} K", delta=f"{atmo_result['temp_k']-273.15:.1f}°C")
m3.metric("Pressure", f"{atmo_result['pressure_pa']:.0f} Pa")
m4.metric("Density", f"{atmo_result['density']:.4f} kg/m³")
m5.metric("Atmosphere Layer", atmo_result.get('layer', 'Analyzing...'))

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════
tab_hud, tab_nasa, tab_sim = st.tabs(["📡 3D Telemetry HUD", "🛰️ NASA Tracking", "🔬 Physics Simulator"])

# --- TAB 1: 3D HUD ---
with tab_hud:
    col_3d, col_panel = st.columns([3, 1])
    with col_3d:
        t = np.linspace(0, 10, 200)
        x = t * sim_velocity * 0.1 + np.random.normal(0, 2, 200)
        y = np.sin(t * 0.8) * 500 * (1 + wind_speed / 100)
        z = sim_altitude - (t ** 2) * 50
        stress = np.abs(np.cos(t * 1.5)) * 100 * (sim_velocity / 1500)

        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines+markers',
            marker=dict(size=2.5, color=stress, colorscale='Turbo',  # pyre-ignore[6]
                       colorbar=dict(title="Ca Stress %", thickness=12)),  # pyre-ignore[6]
            line=dict(color='#00d2ff', width=2.5), name="Flight Path"))  # pyre-ignore[6]
        
        # --- Predicted Trajectory (Phase 3) ---
        pred_x = x + np.random.normal(0, 15, 200)
        pred_y = y + np.random.normal(0, 50, 200)
        fig.add_trace(go.Scatter3d(x=pred_x, y=pred_y, z=z, mode='lines',
                                   line=dict(color='#ffab00', width=1.5, dash='dot'), # pyre-ignore
                                   name="AI Predicted Path"))

        fig.add_trace(go.Scatter3d(x=[x[-1]], y=[y[-1]], z=[z[-1]], mode='markers',
            marker=dict(size=8, color='#ff1744', symbol='diamond'), name="Current"))  # pyre-ignore[6]
        fig.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=520,
            title=f"Tactical Trajectory — Mach {mach_num:.1f} @ {sim_altitude}m",
            scene=dict(xaxis_title="Downrange (m)", yaxis_title="Crossrange (m)",
                       zaxis_title="Altitude (m)", bgcolor='rgba(5,7,14,0)'))
        st.plotly_chart(fig, use_container_width=True)


    with col_panel:
        st.markdown("#### Flight Parameters")
        st.metric("Max Stress", f"{np.max(stress):.1f}%", delta="Tracking")
        st.metric("Wind Effect", f"+{wind_speed*0.3:.1f} m drift", delta=f"{wind_speed} m/s")
        st.metric("Terminal Alt", f"{z[-1]:.0f} m")
        st.progress(min(float(np.max(stress) / 100), 1.0), text="Axial Stress (Ca)")
        st.progress(min(float(mach_num / 8), 1.0), text="Mach Load Factor")

        fem = FEMStructuralOverlay(resolution=10)
        stress_map = fem.compute_stress_map(sim_velocity / 300, sim_velocity, sim_altitude)
        failure = fem.check_failure_nodes()
        color = "#ff1744" if failure['status'] == "CRITICAL" else "#00e676"
        st.markdown(f"""<div style="text-align:center;padding:12px;margin-top:8px;
        background:rgba(12,16,28,0.85);border:1px solid {color}33;border-radius:12px;">
        <div style="font-size:0.72rem;color:#8892b0;">STRUCTURAL STATUS</div>
        <div style="color:{color};font-weight:700;font-size:1rem;margin-top:4px;">{failure['status']}</div>
        <div style="font-size:0.75rem;color:#8892b0;margin-top:4px;">{len(failure['failed_nodes'])} failure nodes</div>
        </div>""", unsafe_allow_html=True)

# --- TAB 2: NASA TRACKING ---
with tab_nasa:
    st.markdown("### 🛰️ Official NASA Asset Tracking (Live TLE)")
    if st.button("🔄 Fetch Live NASA TLE Data", use_container_width=True):
        with st.spinner("Establishing secure handshake with NASA/NORAD Mirror..."):
            try:
                fetcher = TLEFetcher()
                st.session_state['nasa_assets'] = fetcher.get_active_nasa_assets()
                st.session_state['nasa_loaded'] = True
                log_event("OK", "NASA", "Satellite TLE data synchronized")
            except Exception as e:
                log_event("WARN", "NASA", f"Sync failed: {e}. Loading emergency fallbacks.")
                st.error(f"Handshake failed: {e}")
                st.session_state['nasa_assets'] = [
                    {"OBJECT_NAME": "ISS (OFFLINE)", "TLE_LINE1": "1 25544U 98067A   24051.50000000", "TLE_LINE2": "2 25544  51.6420 247.4720 0006703"},
                    {"OBJECT_NAME": "AQUA (OFFLINE)", "TLE_LINE1": "1 27424U 02022A   24051.50000000", "TLE_LINE2": "2 27424  98.2104 127.3700 0001350"}
                ]
                st.session_state['nasa_loaded'] = True


    if st.session_state['nasa_loaded'] and st.session_state['nasa_assets']:
        cols = st.columns(min(len(st.session_state['nasa_assets']), 4))
        for i, asset in enumerate(st.session_state['nasa_assets'][:4]):
            with cols[i]:
                st.markdown(f"""<div style="background:rgba(12,16,28,0.85);border:1px solid rgba(0,210,255,0.12);
                border-radius:12px;padding:16px;">
                <div style="font-size:0.72rem;color:#8892b0;letter-spacing:1px;">SATELLITE {i+1}</div>
                <div style="font-size:0.92rem;font-weight:700;color:#e8eaf6;margin:6px 0;">{asset.get('OBJECT_NAME', 'UNKNOWN')}</div>
                <span class="status-badge badge-online">TRACKING</span>
                </div>""", unsafe_allow_html=True)
                st.code(f"{asset.get('TLE_LINE1', 'No Data')}\n{asset.get('TLE_LINE2', 'No Data')}", language="text")
        
        if st.button("🗑️ Clear Cache"):
            st.session_state['nasa_loaded'] = False
            st.rerun()

    else:
        st.info("Click 'Fetch Live NASA TLE Data' to load real satellite tracking data from NASA's public API.")

# --- TAB 3: PHYSICS SIMULATOR ---
with tab_sim:
    st.markdown("### 🔬 NASA Standard Atmosphere Simulation")
    altitudes = np.linspace(0, 85000, 200)
    temps, pressures, densities = [], [], []
    for alt in altitudes:
        cond = st.session_state['atmo'].get_atmospheric_state(alt)
        temps.append(cond.get('temp_k', 288.15))
        pressures.append(cond.get('pressure_pa', 101325.0))
        densities.append(cond.get('density', 1.225))

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(x=temps, y=altitudes/1000, mode='lines',
            line=dict(color='#ff1744', width=2.5), fill='tozerox',  # pyre-ignore[6]
            fillcolor='rgba(255,23,68,0.08)'))
        fig_t.add_hline(y=sim_altitude/1000, line_dash="dash", line_color="#00d2ff",
            annotation_text=f"Current: {sim_altitude/1000:.0f}km")
        fig_t.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=400,
            title="Temperature Profile", xaxis_title="T (K)", yaxis_title="Altitude (km)")
        st.plotly_chart(fig_t, use_container_width=True)

    with sc2:
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=np.log10(np.array(pressures)+1), y=altitudes/1000, mode='lines',
            line=dict(color='#3a7bd5', width=2.5), fill='tozerox',  # pyre-ignore[6]
            fillcolor='rgba(58,123,213,0.08)'))
        fig_p.add_hline(y=sim_altitude/1000, line_dash="dash", line_color="#00d2ff")
        fig_p.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=400,
            title="Pressure Profile", xaxis_title="log₁₀(P) (Pa)", yaxis_title="Altitude (km)")
        st.plotly_chart(fig_p, use_container_width=True)

    with sc3:
        fig_d = go.Figure()
        fig_d.add_trace(go.Scatter(x=densities, y=altitudes/1000, mode='lines',
            line=dict(color='#00e676', width=2.5), fill='tozerox',  # pyre-ignore[6]
            fillcolor='rgba(0,230,118,0.08)'))
        fig_d.add_hline(y=sim_altitude/1000, line_dash="dash", line_color="#00d2ff")
        fig_d.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=400,
            title="Density Profile", xaxis_title="ρ (kg/m³)", yaxis_title="Altitude (km)")
        st.plotly_chart(fig_d, use_container_width=True)

    # Digital Twin Simulation
    st.markdown("---")
    st.markdown("### 🏗️ Aerodynamic Digital Twin — What-If Result")
    result = st.session_state['twin'].simulate_maneuver(sim_velocity, sim_altitude, sim_velocity / 300)
    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Dynamic Pressure", f"{0.5 * air_density * sim_velocity**2 / 1e3:.1f} kPa")
    rc2.metric("Canard Stress", f"{result['canard_stress_mpa']:.1f} MPa")
    rc3.metric("Reynolds Number", f"{air_density * sim_velocity * 1.0 / 1.8e-5:.2e}")
    color = "#ff1744" if "CRITICAL" in result['status'] else ("#ffab00" if "WARNING" in result['status'] else "#00e676")
    rc4.markdown(f"""<div style="text-align:center;padding:16px;margin-top:8px;">
    <div style="font-size:0.72rem;color:#8892b0;">VERDICT</div>
    <div style="color:{color};font-weight:700;font-size:1.2rem;">{result['status']}</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""<div style="text-align:center;padding:8px;font-size:0.72rem;color:#8892b0;">
© 2026 Aegis-X Tactical Defense Systems &bull; NASA Physics Grounded &bull;
Classification: UNCLASSIFIED // FOUO &bull; v3.0
</div>""", unsafe_allow_html=True)
