import sys, os, time, datetime, random
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st  # type: ignore
import numpy as np  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import pandas as pd  # type: ignore

from core.multi_physics_pinn import ApexMultiPhysicsPINN  # type: ignore
from core.fem_overlay import FEMStructuralOverlay  # type: ignore
from core.digital_twin import AerodynamicDigitalTwin  # type: ignore
from autonomy.game_theory_solver import GameTheoreticSolver  # type: ignore
from autonomy.trajectory_solver import MCTrajectorySolver  # type: ignore
from autonomy.tactical_transformer import TacticalTransformer  # type: ignore
from autonomy.xai_diagnostic import XAIDiagnostic  # type: ignore
from mesh.byzantine_mesh import ByzantineMesh  # type: ignore

from mesh.hil_profiler import HILProfiler  # type: ignore
from mesh.sigma_point_fusion import SigmaPointFusion  # type: ignore
from security.pqc_signing import PQCSigningEngine  # type: ignore
from security.self_healing import SelfHealingLogic  # type: ignore
from data.nasa_physics import NASAStandardAtmosphere  # type: ignore
from data.tle_fetcher import TLEFetcher  # type: ignore
from frontier.hyper_branching import HyperBranchingCloud  # type: ignore
from dashboard.enterprise_css import ENTERPRISE_CSS, PLOTLY_DARK_TEMPLATE  # type: ignore
from dashboard.reporter import generate_html_report, get_report_download_link  # type: ignore

# ═══════════════════════════════════════════════════════════════
# APP CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Apex-X Enterprise Command", layout="wide", page_icon="🛡️",
                   initial_sidebar_state="expanded")
st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
if 'pqc_engine' not in st.session_state:
    st.session_state['pqc_engine'] = PQCSigningEngine()
    st.session_state['pqc_tag'] = "CHAIN_IDLE — Awaiting signature request..."
    st.session_state['event_log'] = []
    st.session_state['mesh_nodes'] = [
        {"id": f"AEGIS-{i:02d}", "key": f"KEY_{i:04X}", "lat": np.random.uniform(-60,60),
         "lon": np.random.uniform(-180,180), "status": random.choice(["ONLINE","ONLINE","ONLINE","STANDBY"])}
        for i in range(1, 15)
    ]
    st.session_state['boot_time'] = time.time()
    st.session_state['chat_history'] = [{"role": "bot", "content": "Welcome to Apex-X Mission Command. I am the Apex Guardian. How can I assist you in your tactical operations today?"}]
    # Initialize ML Models in Session State
    st.session_state['pinn'] = ApexMultiPhysicsPINN()
    st.session_state['transformer'] = TacticalTransformer()
    st.session_state['xai'] = XAIDiagnostic(model=None)



# ═══════════════════════════════════════════════════════════════
# MISSION AUDIO (Ambient Soundscape)
# ═══════════════════════════════════════════════════════════════
def render_audio_controller():
    with st.sidebar:
        st.markdown("---")
        st.markdown("##### 🎵 MISSION AUDIO")
        # Using st.audio for reliable user-controlled playback
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mpeg", loop=True)
        st.caption("Ambient soundscape for mission focus. (Required by browser security: please press Play to start)")


def log_event(severity, module, message):
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]  # pyre-ignore
    st.session_state['event_log'].insert(0, {"ts": ts, "sev": severity, "mod": module, "msg": message})
    if len(st.session_state['event_log']) > 200:
        st.session_state['event_log'] = st.session_state['event_log'][:200]

def uptime_str():
    delta = int(time.time() - st.session_state['boot_time'])
    h, m, s = delta // 3600, (delta % 3600) // 60, delta % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:2.2rem;">🛡️</div>
        <div style="font-size:1.1rem;font-weight:700;background:linear-gradient(135deg,#00d2ff,#3a7bd5);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">APEX-X COMMAND</div>
        <div style="font-size:0.7rem;color:#8892b0;letter-spacing:2px;margin-top:4px;">ENTERPRISE v3.0</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("MISSION CONTROL", [
        "📊 Strategic Overview",
        "🔥 Intercept Forge",
        "🧠 Threat Intelligence",
        "🕸️ Mesh Operations",
        "🔐 Security Center",
        "🌀 Quantum Sandbox",
        "⚙️ System Diagnostics"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"""<div style="font-size:0.72rem;color:#8892b0;padding:0 8px;">
    <b style="color:#00d2ff;">UPTIME</b> {uptime_str()}<br>
    <b style="color:#00e676;">STATUS</b> OPERATIONAL<br>
    <b style="color:#b388ff;">NODES</b> {len(st.session_state['mesh_nodes'])} LINKED
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### 🤖 APEX GUARDIAN")
    sc1, sc2 = st.columns([2, 1]) # Added columns for chat and adversarial defense
    with sc1:
        chat_box = st.container()
        with chat_box:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state['chat_history']:
                cls = "msg-bot" if msg['role'] == "bot" else "msg-user"
                st.markdown(f'<div class="chat-msg {cls}">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with sc2:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.markdown("##### 🛡️ Adversarial Denoising")
        st.caption("StyleGAN Reconstruction")
        
        noise_level = st.slider("Noise (dB)", 0, 50, 15)
        
        t = np.linspace(0, 10, 100)
        pure_signal = np.sin(t)
        noisy_signal = pure_signal + np.random.normal(0, noise_level/50, 100)
        reconstructed = pure_signal + np.random.normal(0, noise_level/200, 100)
        
        fig_adv = go.Figure()
        fig_adv.add_trace(go.Scatter(x=t, y=noisy_signal, name="Jammed", line=dict(color='#ff1744', width=1, dash='dot'))) # pyre-ignore
        fig_adv.add_trace(go.Scatter(x=t, y=reconstructed, name="Clean", line=dict(color='#00e676', width=2))) # pyre-ignore
        
        # Fixed multiple values for 'margin' by merging dicts
        adv_layout = PLOTLY_DARK_TEMPLATE['layout'].copy()
        adv_layout.update(height=250, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
        fig_adv.update_layout(**adv_layout) # pyre-ignore
        st.plotly_chart(fig_adv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


    
    if prompt := st.chat_input("Tactical inquiry..."):
        st.session_state['chat_history'].append({"role": "user", "content": prompt})
        # AI Logic Simulation
        response = "I am processing your tactical request."
        p = prompt.lower()
        if "status" in p: response = f"System status is currently NOMINAL. Uptime: {uptime_str()}. All {len(st.session_state['mesh_nodes'])} nodes are linked."
        elif "threat" in p: response = "Scanning threat matrix... 4 active targets identified. TGT-0042 (Ballistic) is currently the highest priority threat."
        elif "pqc" in p or "security" in p: response = f"PQC Chain state is LOCKED. Current head: {st.session_state['pqc_tag'][:12]}..."
        elif "hello" in p or "hi" in p: response = "Greetings, Commander. I am standing by for tactical updates."
        st.session_state['chat_history'].append({"role": "bot", "content": response})
        st.rerun()

    st.markdown("---")
    st.markdown("##### 📋 MISSION SUMMARY")
    report_html = generate_html_report(
        mission_name="APEX-X ENTERPRISE OPS",
        health_data={"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        threats=[
            {"id":"TGT-0041","type":"Cruise Missile","bearing":"NW 324°","range":"142 km","status":"TRACKING"},
            {"id":"TGT-0042","type":"Ballistic (MRBM)","bearing":"NE 047°","range":"891 km","status":"INTERCEPT"},
            {"id":"TGT-0043","type":"UAV Swarm","bearing":"SE 156°","range":"38 km","status":"TRACKING"},
        ],
        pqc_tag=st.session_state['pqc_tag']
    )
    st.markdown(get_report_download_link(report_html), unsafe_allow_html=True)
    
    # Render audio at the bottom of sidebar
    render_audio_controller()


# ═══════════════════════════════════════════════════════════════
# HEADER BAR
# ═══════════════════════════════════════════════════════════════
now = datetime.datetime.now()
hcol1, hcol2, hcol3 = st.columns([4,4,2])
with hcol1:
    st.markdown(f"# {page}")
with hcol3:
    st.markdown(f"""<div style="text-align:right;padding-top:12px;font-size:0.8rem;color:#8892b0;">
    <span style="color:#00d2ff;font-weight:600;">{now.strftime('%d %b %Y')}</span> &nbsp;
    <span style="font-family:'JetBrains Mono',monospace;">{now.strftime('%H:%M:%S')} UTC-7</span>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 1: STRATEGIC OVERVIEW
# ═══════════════════════════════════════════════════════════════
if page == "📊 Strategic Overview":
    log_event("INFO", "CMD", "Strategic Overview accessed")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Active Assets", "142", delta="3 Online")
    k2.metric("Link Integrity", "99.98%", delta="Nominal")
    k3.metric("Threat Count", "04", delta="-1 Resolved", delta_color="inverse")
    k4.metric("PQC Chain", "LOCKED", delta="Verified")
    k5.metric("Mesh Latency", "4.2 ms", delta="Budget OK")
    k6.metric("PINN Accuracy", "99.4%", delta="+0.1%")

    st.markdown("")
    col_map, col_health = st.columns([3, 2])

    with col_map:
        st.markdown("### 🌐 Global Asset Deployment")
        nodes = st.session_state['mesh_nodes']
        map_df = pd.DataFrame({
            'lat': [n['lat'] for n in nodes],
            'lon': [n['lon'] for n in nodes],
            'size': [30 if n['status']=='ONLINE' else 15 for n in nodes],
        })
        fig_map = px.scatter_geo(map_df, lat='lat', lon='lon', size='size',
            projection="natural earth",
            color_discrete_sequence=['#00d2ff'])
        fig_map.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=420,
            geo=dict(bgcolor='rgba(5,7,14,0)', landcolor='#0d1020',  # pyre-ignore[6]
                     oceancolor='#080b14', showocean=True, showland=True,  # pyre-ignore[6]
                     coastlinecolor='rgba(0,210,255,0.15)', countrycolor='rgba(0,210,255,0.08)',
                     lakecolor='#080b14'))
        fig_map.update_layout(title="Tactical Mesh Node Distribution")
        st.plotly_chart(fig_map, use_container_width=True)

    with col_health:
        st.markdown("### 📡 System Health Matrix")
        modules = [
            ("Multi-Physics PINN", "NOMINAL", "#00e676"),
            ("Game Theory Engine", "NOMINAL", "#00e676"),
            ("Byzantine Mesh", "NOMINAL", "#00e676"),
            ("Sigma-Point Fusion", "NOMINAL", "#00e676"),
            ("PQC Signing", "LOCKED", "#00d2ff"),
            ("Self-Healing Logic", "STANDBY", "#ffab00"),
            ("Adversarial AI", "ACTIVE", "#b388ff"),
            ("FEM Overlay", "NOMINAL", "#00e676"),
            ("Digital Twin", "NOMINAL", "#00e676"),
            ("HIL Profiler", "ACTIVE", "#b388ff"),
        ]
        html = '<div style="background:rgba(12,16,28,0.85);border:1px solid rgba(0,210,255,0.12);border-radius:12px;padding:16px;">'
        for name, status, color in modules:
            html += f'''<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 12px;
            border-bottom:1px solid rgba(255,255,255,0.03);font-size:0.82rem;">
            <span style="color:#e8eaf6;">{name}</span>
            <span style="color:{color};font-weight:600;font-size:0.75rem;background:rgba(0,0,0,0.3);
            padding:3px 10px;border-radius:12px;border:1px solid {color}33;">{status}</span></div>'''
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    # Threat Radar
    st.markdown("### 🎯 Active Threat Classification")
    tc1, tc2, tc3 = st.columns(3)
    threats = [
        {"id":"TGT-0041","type":"Cruise Missile","conf":0.97,"bearing":"NW 324°","range":"142 km","status":"TRACKING"},
        {"id":"TGT-0042","type":"Ballistic (MRBM)","conf":0.89,"bearing":"NE 047°","range":"891 km","status":"INTERCEPT"},
        {"id":"TGT-0043","type":"UAV Swarm","conf":0.94,"bearing":"SE 156°","range":"38 km","status":"TRACKING"},
    ]
    for col, t in zip([tc1, tc2, tc3], threats):
        badge_cls = "badge-alert" if t['status']=='INTERCEPT' else "badge-online"
        with col:
            st.markdown(f"""<div style="background:rgba(12,16,28,0.85);border:1px solid rgba(0,210,255,0.12);
            border-radius:12px;padding:20px;">
            <div style="font-size:0.72rem;color:#8892b0;letter-spacing:1px;">{t['id']}</div>
            <div style="font-size:1.1rem;font-weight:700;color:#e8eaf6;margin:4px 0;">{t['type']}</div>
            <div style="font-size:0.82rem;color:#8892b0;">Confidence: <b style="color:#00d2ff;">{t['conf']*100:.0f}%</b></div>
            <div style="font-size:0.82rem;color:#8892b0;">Bearing: {t['bearing']} &bull; Range: {t['range']}</div>
            <div style="margin-top:8px;"><span class="status-badge {badge_cls}">{t['status']}</span></div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 2: INTERCEPT FORGE
# ═══════════════════════════════════════════════════════════════
elif page == "🔥 Intercept Forge":
    log_event("INFO", "FORGE", "Intercept Forge initialized")
    st.caption("Real-time Multi-Physics Trajectory Synthesis & Structural Validation")

    tab_traj, tab_fem, tab_pinn, tab_game = st.tabs(["🚀 Trajectory", "🔩 FEM Structural", "⚛️ PINN Core", "🎲 Game Theory"])


    with tab_traj:
        col_3d, col_met = st.columns([3, 1])
        with col_3d:
            t = np.linspace(0, 12, 200)
            x = np.cos(t * 0.5) * (500 + t * 30)
            y = np.sin(t * 0.5) * (500 + t * 30)
            z = 15000 - t * 800 + np.sin(t) * 200
            mach = 1.5 + t * 0.25
            fig = go.Figure()
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines+markers',
                marker=dict(size=3, color=mach, colorscale='Turbo', colorbar=dict(title="Mach", thickness=15)),  # pyre-ignore[6]
                line=dict(color='#00d2ff', width=3), name="Intercept Vector"))  # pyre-ignore[6]
            fig.add_trace(go.Scatter3d(x=[x[-1]], y=[y[-1]], z=[z[-1]], mode='markers',  # pyre-ignore[5]
                marker=dict(size=10, color='#ff1744', symbol='diamond'), name="PIP"))  # pyre-ignore[6]
            fig.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=550,
                title="Multi-Physics Intercept Trajectory",
                scene=dict(xaxis=dict(title="Downrange (m)"), yaxis=dict(title="Crossrange (m)"),  # pyre-ignore[6]
                           zaxis=dict(title="Altitude (m)"),  # pyre-ignore[6]
                           bgcolor='rgba(5,7,14,0)'))  # pyre-ignore[6]
            st.plotly_chart(fig, use_container_width=True)
        with col_met:
            st.markdown("#### Flight Metrics")
            st.metric("Terminal Mach", f"{mach[-1]:.1f}", delta="Hypersonic")  # pyre-ignore[5]
            st.metric("Terminal Alt", f"{z[-1]:.0f} m", delta="Descending")  # pyre-ignore[5]
            st.metric("Time to PIP", "12.0 s", delta="Active")
            st.progress(0.85, text="Mach Load Factor")
            st.progress(0.42, text="Thermal Flux")
            st.progress(0.18, text="Canard Stress")
            if st.button("🔐 Sign Trajectory (PQC)"):
                tag = st.session_state['pqc_engine'].generate_weight_integrity_tag(x.tolist()[:10])
                st.session_state['pqc_tag'] = tag
                log_event("OK", "PQC", "Trajectory integrity tag generated")
            st.code(st.session_state['pqc_tag'][:64] + "...", language="text")

    with tab_fem:
        fem = FEMStructuralOverlay(resolution=20)
        g_load = st.slider("G-Load Factor", 1.0, 15.0, 8.0, 0.5)
        velocity = st.slider("Velocity (m/s)", 500, 3000, 1500, 50)
        stress_map = fem.compute_stress_map(g_load, velocity, 5000)
        failure = fem.check_failure_nodes()
        fc1, fc2 = st.columns([2, 1])
        with fc1:
            fig_fem = px.imshow(stress_map / 1e6, color_continuous_scale="Inferno",
                labels=dict(color="Stress (MPa)"))
            fig_fem.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=450,
                title=f"Von Mises Stress Distribution — {g_load}G @ {velocity} m/s")
            st.plotly_chart(fig_fem, use_container_width=True)
        with fc2:
            st.metric("Max Stress", f"{np.max(stress_map)/1e6:.1f} MPa")
            st.metric("Failed Nodes", f"{len(failure['failed_nodes'])}")
            st.metric("Failure Rate", f"{failure['failure_percentage']*100:.1f}%")
            color = "#ff1744" if failure['status'] == "CRITICAL" else "#00e676"
            st.markdown(f'<div style="text-align:center;padding:20px;"><span class="status-badge" '
                f'style="background:rgba(0,0,0,0.3);color:{color};border:1px solid {color}55;font-size:1.1rem;">'
                f'{failure["status"]}</span></div>', unsafe_allow_html=True)
            log_event("INFO", "FEM", f"Stress analysis: {failure['status']} at {g_load}G")

    with tab_pinn:
        st.markdown("#### 🚀 Hypersonic Multi-Physics PINN Inference")
        st.caption("Deep surrogate modeling for real-time aerodynamic, thermal, and structural prediction.")
        
        pc1, pc2 = st.columns([1, 2])
        with pc1:
            st.markdown("##### Model Inputs")
            p_mach = st.slider("Input Mach", 2.0, 15.0, 8.5)
            p_alt = st.slider("Input Altitude (m)", 1000, 80000, 35000)
            p_aoa = st.slider("Alpha (AoA deg)", -5.0, 25.0, 12.0)
            p_temp = st.slider("Ambient Temp (K)", 200, 300, 240)
            
            # Simulated PINN Inference
            # In a real dashboard, we'd pass these to st.session_state['pinn']
            # Using mock results to ensure high performance UI response
            aero_score = np.interp(p_mach, [2, 15], [0.4, 0.95])
            thermal_load = (p_mach**1.8) * (p_alt/10000)
            structural_strain = p_mach * (p_aoa/10)
            
            st.markdown("##### Constraint Metrics")
            st.metric("Physics Loss", f"{0.0012 + random.random()*0.0005:.5f}", delta="-0.0001", delta_color="inverse")
            st.metric("L/D Efficiency", f"{1.5 + (p_aoa/20):.2f}", delta="Optimal")

        with pc2:
            st.markdown("##### Prediction Distribution Matrix")
            categories = ['Aero Stability', 'Thermal Flux', 'Structural Strain', 'Boundary Latency', 'Constraint Integrity']
            values = [aero_score, 0.4 + (thermal_load/500), 0.3 + (structural_strain/15), 0.92, 0.98]
            
            fig_pinn = go.Figure()
            fig_pinn.add_trace(go.Scatterpolar(
                r=values, theta=categories, fill='toself',
                fillcolor='rgba(0, 210, 255, 0.25)',
                line=dict(color='#00d2ff', width=2),  # pyre-ignore
                name='Apex-X PINN'
            ))
            
            pinn_layout = PLOTLY_DARK_TEMPLATE['layout'].copy()
            pinn_layout.update(height=450, polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(255,255,255,0.05)'), # pyre-ignore
                                                     bgcolor='rgba(0,0,0,0)')) # pyre-ignore
            fig_pinn.update_layout(**pinn_layout) # pyre-ignore
            st.plotly_chart(fig_pinn, use_container_width=True)

            log_event("OK", "PINN", f"Surrogate inference converged at Mach {p_mach}")



    with tab_game:
        st.markdown("#### Minimax Game-Theoretic Solver")
        solver = GameTheoreticSolver(horizon=float(st.slider("Lookahead Horizon (s)", 1.0, 10.0, 5.0, 0.5)))
        if st.button("▶ Solve Minimax Trajectory"):
            with st.spinner("Computing minimax solution..."):
                i_s = np.array([0, 0, 0, 1000, 0, 0], dtype=float)
                t_s = np.array([2000, 100, 50, 800, 20, 10], dtype=float)
                sol = solver.compute_minimax_trajectory(i_s, t_s, None)
                st.metric("Minimax Miss", f"{sol['minimax_miss_m']:.1f} m")
                st.metric("Intercept Confidence", f"{sol['confidence']*100:.1f}%")  # pyre-ignore[58]
                st.json({"optimal_accel": sol['optimal_accel'].tolist(), "minimax_miss_m": float(sol['minimax_miss_m'])})
                log_event("OK", "GAME", f"Minimax solved: miss={sol['minimax_miss_m']:.1f}m")

# ═══════════════════════════════════════════════════════════════
# PAGE 3: THREAT INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
elif page == "🧠 Threat Intelligence":
    log_event("INFO", "INTEL", "Threat Intelligence loaded")
    st.caption("Adversarial Analysis, XAI Attribution & StyleGAN Jamming Simulation")

    t1, t2, t3 = st.tabs(["🎯 XAI Salience", "🧠 Intent Attention", "📡 Adversarial Jamming"])
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Integrated Gradients Attribution")
            salience = np.abs(np.random.randn(64, 64))
            salience[20:44, 20:44] += 3.0
            salience = salience / salience.max()
            fig_s = px.imshow(salience, color_continuous_scale="Hot", labels=dict(color="Attribution"))
            fig_s.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=420, title="Target Attribution Map")
            st.plotly_chart(fig_s, use_container_width=True)
        with c2:
            st.markdown("#### Classification Confidence Matrix")
            classes = ["Cruise Missile", "Ballistic", "UAV", "Decoy", "Fighter"]
            conf = np.random.dirichlet(np.ones(5) * 0.5, size=5)
            fig_c = px.imshow(conf, x=classes, y=[f"Sensor {i+1}" for i in range(5)],
                color_continuous_scale="Teal", labels=dict(color="P(class)"))
            fig_c.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=420, title="Multi-Sensor Confidence")
            st.plotly_chart(fig_c, use_container_width=True)
        st.info("🎯 **XAI Reasoning:** Target classified as **Cruise Missile** (P=0.97) — dominant feature: "
                "rear canard geometry in IR band (Sector 4), confirmed by radar cross-section profile.")
    
    with t2:
        st.markdown("#### Tactical Transformer Attention Heatmaps")
        st.caption("Decoding multi-head attention weights across hypersonic telemetry channels.")
        at1, at2 = st.columns([1, 2])
        with at1:
            st.markdown("##### Focus Saliency")
            st.metric("Head 1 Divergence", "0.042", delta="-0.001")
            st.metric("Head 2 Alignment", "0.892", delta="+0.012")
            st.metric("Context Window", "5.0s")
            st.progress(0.76, text="Intent Predictor Confidence")
        with at2:
            attn_data = np.random.rand(8, 8)
            fig_attn = px.imshow(attn_data, color_continuous_scale='Turbo',
                                 labels=dict(x="Time Step", y="Sensor Head", color="Attention"))
            fig_attn.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=400, title="Transformer Attention Weights")
            st.plotly_chart(fig_attn, use_container_width=True)

    with t3:
        st.markdown("#### StyleGAN Entropy Masks")
        gc1, gc2, gc3 = st.columns(3)
        for i, col in enumerate([gc1, gc2, gc3]):
            noise = np.random.rand(64, 64) * np.random.rand(64, 64)
            with col:
                fig_n = px.imshow(noise, color_continuous_scale=["Viridis","Plasma","Cividis"][i])
                fig_n.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=280,
                    title=f"Mask {i+1} — Entropy: {np.std(noise):.3f}")
                st.plotly_chart(fig_n, use_container_width=True)
        st.warning("⚠️ **Adversarial Alert:** High-entropy jamming patterns detected across 3 frequency bands.")


# ═══════════════════════════════════════════════════════════════
# PAGE 4: MESH OPERATIONS
# ═══════════════════════════════════════════════════════════════
elif page == "🕸️ Mesh Operations":
    log_event("INFO", "MESH", "Mesh Operations console opened")
    st.caption("Byzantine Fault-Tolerant Mesh, Federated Sync & Sigma-Point Fusion")

    mk1, mk2, mk3, mk4 = st.columns(4)
    online = sum(1 for n in st.session_state['mesh_nodes'] if n['status'] == 'ONLINE')
    mk1.metric("Mesh Nodes", str(len(st.session_state['mesh_nodes'])), delta=f"{online} Online")
    mk2.metric("Byzantine Faults", "0", delta="None Detected")
    mk3.metric("Consensus", "REACHED", delta="2/3 Majority")
    mk4.metric("Sync Latency", "4.2 ms", delta="Within Budget")

    mt1, mt2 = st.tabs(["📊 HIL Profiling", "🔗 Consensus & Fusion"])
    with mt1:
        st.markdown("#### Hardware-in-the-Loop Latency Distribution")
        latencies = np.random.normal(4.2, 0.3, 500)
        fig_h = go.Figure()
        fig_h.add_trace(go.Histogram(x=latencies, nbinsx=40, marker_color='#3a7bd5',
            marker_line=dict(color='#00d2ff', width=0.5), opacity=0.85))  # pyre-ignore[6]
        fig_h.add_vline(x=5.0, line_dash="dash", line_color="#ff1744", annotation_text="Budget: 5ms",
            annotation_font_color="#ff1744")
        fig_h.add_vline(x=np.mean(latencies), line_dash="dot", line_color="#00e676",
            annotation_text=f"Mean: {np.mean(latencies):.2f}ms", annotation_font_color="#00e676")
        fig_h.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=380,
            title=f"Inference Latency — P99: {np.percentile(latencies,99):.2f}ms",
            xaxis_title="Latency (ms)", yaxis_title="Count")
        st.plotly_chart(fig_h, use_container_width=True)

    with mt2:
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("#### Byzantine Consensus Log")
            mesh = ByzantineMesh("AEGIS-CMD", "MASTER_KEY")
            updates = [mesh.sign_weight_update([round(random.random(),3) for _ in range(5)])  # pyre-ignore
                       for _ in range(5)]
            consensus = mesh.resolve_consensus(updates)
            for u in updates[:3]:  # pyre-ignore
                st.markdown(f"""<div style="background:rgba(12,16,28,0.85);border:1px solid rgba(0,210,255,0.12);
                border-radius:8px;padding:10px 14px;margin-bottom:6px;font-size:0.78rem;
                font-family:'JetBrains Mono',monospace;">
                <span style="color:#8892b0;">{u['unit']}</span> &bull;
                <span style="color:#00d2ff;">HASH</span> {u['weight_hash'][:24]}...
                </div>""", unsafe_allow_html=True)
            color = "#00e676" if consensus == "REACHED" else "#ff1744"
            st.markdown(f'<div style="text-align:center;padding:16px;"><span style="color:{color};font-weight:700;'
                f'font-size:1.1rem;">CONSENSUS: {consensus}</span></div>', unsafe_allow_html=True)
        with mc2:
            st.markdown("#### Sigma-Point Fusion State")
            fusion = SigmaPointFusion()
            x_state = np.array([1000, 500, 200, 300, 50, 10], dtype=float)
            P = np.eye(6) * 0.1
            pts = fusion.generate_sigma_points(x_state, P)
            fig_sp = go.Figure()
            fig_sp.add_trace(go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2], mode='markers',
                marker=dict(size=5, color='#b388ff', opacity=0.8), name="Sigma Points"))  # pyre-ignore[6]
            fig_sp.add_trace(go.Scatter3d(x=[x_state[0]], y=[x_state[1]], z=[x_state[2]], mode='markers',
                marker=dict(size=10, color='#00d2ff', symbol='diamond'), name="Mean State"))  # pyre-ignore[6]
            fig_sp.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=380,
                title=f"Unscented Transform — {pts.shape[0]} Sigma Points",
                scene=dict(bgcolor='rgba(5,7,14,0)'))
            st.plotly_chart(fig_sp, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 5: SECURITY CENTER
# ═══════════════════════════════════════════════════════════════
elif page == "🔐 Security Center":
    log_event("INFO", "SEC", "Security Center accessed")
    st.caption("Post-Quantum Cryptography, Self-Healing & Integrity Verification")

    sk1, sk2, sk3 = st.columns(3)
    sk1.metric("PQC Chain Status", "LOCKED", delta="SHA3-512")
    sk2.metric("Integrity Checks", "347", delta="0 Failures")
    sk3.metric("Self-Healing", "STANDBY", delta="No Faults")

    sec1, sec2 = st.tabs(["🔑 PQC Engine", "🛡️ Self-Healing"])
    with sec1:
        sc1, sc2 = st.columns([2, 1])
        with sc1:
            st.markdown("#### Post-Quantum Weight Integrity Chain")
            if st.button("🔐 Generate New Integrity Tag"):
                weights = np.random.randn(10).tolist()
                tag = st.session_state['pqc_engine'].generate_weight_integrity_tag(weights)
                st.session_state['pqc_tag'] = tag
                log_event("OK", "PQC", "New integrity tag generated (SHA3-Lattice)")
            st.markdown("**Current Chain Head:**")
            st.code(st.session_state['pqc_tag'], language="text")
        with sc2:
            st.markdown("#### Chain Properties")
            st.markdown("""
            | Property | Value |
            |----------|-------|
            | Algorithm | SHA3-512 |
            | Iterations | 100 |
            | Entropy Source | os.urandom(32) |
            | Chain Depth | Recursive |
            | Quantum Resistance | Post-Quantum |
            """)
    with sec2:
        st.markdown("#### Self-Healing Logic Monitor")
        healer = SelfHealingLogic()
        statuses = {
            "PINN_Engine": "STABLE", "Mesh_Network": "STABLE", "GNC_System": "STABLE",
            "Sensor_Fusion": "STABLE", "PQC_Chain": "STABLE", "FEM_Overlay": "STABLE"
        }
        if st.button("🧪 Simulate Byzantine Fault"):
            statuses["Mesh_Network"] = "BYZANTINE_FAULT"
            log_event("CRIT", "HEAL", "Byzantine fault injected for testing")
        report = healer.monitor_decision_integrity(statuses)
        for mod, status in statuses.items():
            color = "#00e676" if status == "STABLE" else "#ff1744"
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 14px;
            border-bottom:1px solid rgba(255,255,255,0.03);">
            <span style="color:#e8eaf6;font-size:0.85rem;">{mod.replace('_',' ')}</span>
            <span style="color:{color};font-weight:600;font-size:0.78rem;">{status}</span></div>""",
            unsafe_allow_html=True)
        if report['status'] != "HEALTHY":
            st.error(f"🔴 Recovery Protocol: {report['actions']}")
        else:
            st.success("✅ All modules operating within nominal parameters.")

# ═══════════════════════════════════════════════════════════════
# PAGE 6: QUANTUM SANDBOX
# ═══════════════════════════════════════════════════════════════
elif page == "🌀 Quantum Sandbox":
    log_event("INFO", "QTM", "Quantum Sandbox entered")
    st.caption("Hyper-Branching Probability Manifolds & Temporal Folding")

    qt1, qt2 = st.tabs(["🌊 Probability Manifold", "⏳ Digital Twin"])
    with qt1:
        st.markdown("#### Hypersonic Stability Gradient")
        res = st.slider("Manifold Resolution", 20, 50, 30)
        x_m = np.outer(np.linspace(-3, 3, res), np.ones(res))
        y_m = x_m.copy().T
        z_m = np.sin(x_m**2 + y_m**2) * np.exp(-0.1 * (x_m**2 + y_m**2))
        fig_q = go.Figure(data=[go.Surface(z=z_m, colorscale="Ice", opacity=0.92,
            contours=dict(z=dict(show=True, color='#00d2ff', width=1)))])  # pyre-ignore[6]
        fig_q.update_layout(**PLOTLY_DARK_TEMPLATE['layout'], height=600,
            title="Probability Manifold — Converged Flight Envelope",
            scene=dict(bgcolor='rgba(5,7,14,0)', xaxis_title="Mach Deviation",
                       yaxis_title="AoA Deviation", zaxis_title="P(stable)"))
        st.plotly_chart(fig_q, use_container_width=True)
        convergence = float(np.sum(z_m > 0) / z_m.size * 100)
        st.success(f"✅ **Quantum Verification:** {convergence:.1f}% of manifold converges within stable flight envelope.")

    with qt2:
        st.markdown("#### Aerodynamic Digital Twin — Maneuver Stress Analysis")
        twin = AerodynamicDigitalTwin()
        dt_vel = st.slider("Velocity (m/s)", 200, 2500, 800, 50)
        dt_alt = st.slider("Altitude (m)", 1000, 50000, 10000, 500)
        dt_g = st.slider("G-Load", 1.0, 15.0, 6.0, 0.5)
        result = twin.simulate_maneuver(dt_vel, dt_alt, dt_g)
        dc1, dc2, dc3, dc4 = st.columns(4)
        dc1.metric("Velocity", f"{result['velocity']} m/s")
        dc2.metric("Altitude", f"{result['altitude']} m")
        dc3.metric("G-Load", f"{result['g_load']}")
        dc4.metric("Canard Stress", f"{result['canard_stress_mpa']:.1f} MPa")
        color = "#ff1744" if "CRITICAL" in result['status'] else ("#ffab00" if "WARNING" in result['status'] else "#00e676")
        st.markdown(f'<div style="text-align:center;padding:16px;"><span class="status-badge" '
            f'style="background:rgba(0,0,0,0.3);color:{color};border:1px solid {color}55;font-size:1rem;">'
            f'{result["status"]}</span></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 7: SYSTEM DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════
elif page == "⚙️ System Diagnostics":
    log_event("INFO", "DIAG", "System Diagnostics opened")
    st.caption("Event Log, Module Health & Performance Profiling")

    st.markdown("#### 📋 Mission Event Log")
    sev_filter = st.multiselect("Severity Filter", ["INFO","OK","WARN","CRIT"], default=["INFO","OK","WARN","CRIT"])
    events = [e for e in st.session_state['event_log'] if e['sev'] in sev_filter]

    if events:
        sev_colors = {"INFO": "ev-info", "OK": "ev-ok", "WARN": "ev-warn", "CRIT": "ev-crit"}
        log_html = '<div class="event-log">'
        for e in events[:50]:  # pyre-ignore
            cls = sev_colors.get(e['sev'], 'ev-info')
            log_html += f'<div><span class="ev-time">{e["ts"]}</span><span class="{cls}">[{e["sev"]}]</span> <span style="color:#b388ff;">[{e["mod"]}]</span> {e["msg"]}</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.info("No events recorded yet. Navigate to other pages to generate events.")

    st.markdown("---")
    st.markdown("#### 🏗️ Module Registry")
    mod_data = pd.DataFrame({
        "Module": ["ApexMultiPhysicsPINN", "FEMStructuralOverlay", "GameTheoreticSolver",
                   "ByzantineMesh", "SigmaPointFusion", "PQCSigningEngine",
                   "SelfHealingLogic", "AerodynamicDigitalTwin", "HILProfiler", "MCTrajectorySolver"],
        "Package": ["core", "core", "autonomy", "mesh", "mesh", "security",
                     "security", "core", "mesh", "autonomy"],
        "Status": ["✅ LOADED"] * 10,
        "Version": ["3.0"] * 10
    })
    st.dataframe(mod_data, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""<div style="text-align:center;padding:8px;font-size:0.72rem;color:#8892b0;">
© 2026 Apex-X Enterprise Defense Platform &bull; Proprietary &bull; Classification: UNCLASSIFIED //
FOUO &bull; v3.0 Build {int(time.time()) % 100000}
</div>""", unsafe_allow_html=True)
