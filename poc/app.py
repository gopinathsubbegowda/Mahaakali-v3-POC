import streamlit as st
import pandas as pd
import plotly.express as px
import time
import json
from datetime import datetime
import os

# Set Page Config for "Wow" factor
st.set_page_config(
    page_title="Mahaakali Trust Plane Control Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4451;
    }
    .stSidebar {
        background-color: #0b0e14;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.image("https://img.icons8.com/nolan/128/shield.png", width=80)
st.sidebar.title("Mahaakali V3")
st.sidebar.subheader("Security Trust Plane")

menu = st.sidebar.radio(
    "Modules",
    ["Overview", "Visual Policy Builder", "Compliance Mapping", "Safety & HITL Dashboard", "Supply Chain (AIBOM)", "Sovereign OS Control"]
)

# --- Mock Data Helpers ---
def load_mock_compliance():
    return pd.DataFrame([
        {"Feature": "AIBOM Signing", "NIST AI RMF": "GV-1.1", "ISO 42001": "B.5.2", "Status": "Verified"},
        {"Feature": "Policy-as-Code", "NIST AI RMF": "PR-1.2", "ISO 42001": "B.7.1", "Status": "Active"},
        {"Feature": "Circuit Breaker", "NIST AI RMF": "RS-2.1", "ISO 42001": "B.9.3", "Status": "Standby"},
        {"Feature": "HITL Gateway", "NIST AI RMF": "GV-3.2", "ISO 42001": "B.6.1", "Status": "Configured"},
        {"Feature": "TEE Isolation", "NIST AI RMF": "PR-2.1", "ISO 42001": "B.8.4", "Status": "Simulation Mode"},
    ])

# --- Page: Overview ---
if menu == "Overview":
    st.title("🛡️ Trust Plane Dashboard")
    st.write("Real-time monitoring of Agentic AI Security and Governance.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Agents", "12", "Shared Swarm")
    col2.metric("Violations Prevented", "452", "High Resilience")
    col3.metric("System Trust Score", "98.4%", "Stable")
    col4.metric("Shadow Phase Day", "14/30", "Learning")

    st.subheader("Action Velocity & Safety Interventions")
    chart_data = pd.DataFrame({
        'time': pd.date_range(start='2026-02-12', periods=24, freq='H'),
        'actions': [10, 15, 8, 12, 20, 25, 30, 45, 40, 35, 20, 15, 10, 5, 8, 12, 18, 22, 28, 32, 25, 20, 15, 12],
        'blocks': [0, 0, 1, 0, 0, 2, 5, 8, 2, 1, 0, 0, 0, 0, 0, 0, 1, 3, 2, 0, 0, 0, 0, 0]
    })
    fig = px.line(chart_data, x='time', y=['actions', 'blocks'], title="Agent Swarm Activity vs Trust Plane Interventions")
    st.plotly_chart(fig, use_container_width=True)

# --- Page: Visual Policy Builder ---
elif menu == "Visual Policy Builder":
    st.title("🛠️ Visual Policy Builder")
    st.write("Define governance rules using high-level constraints and Agentic Policy Generation.")

    tab1, tab2 = st.tabs(["Drag & Drop Rules", "Agentic Policy Generator"])

    with tab1:
        st.subheader("Manual Constraint Configuration")
        with st.expander("New Policy: File Access Control", expanded=True):
            policy_name = st.text_input("Policy Name", "Restrict_HR_Access")
            target = st.multiselect("Target Folders", ["/etc/", "/users/hr/", "/logs/", "/config/"], default=["/users/hr/"])
            action_type = st.selectbox("On Violation", ["BLOCK & Record", "BLOCK & Trigger HITL", "OBSERVE Only (Shadow)"])
            severity = st.select_slider("Severity Level", options=["Low", "Medium", "High", "Critical"])
            if st.button("Deploy Policy"):
                st.success(f"Policy '{policy_name}' deployed to Trust Plane via Hot-Reload.")

    with tab2:
        st.subheader("Policy-as-Code Generator Agent")
        st.info("Describe your security requirement in natural language and the Agent will generate the deterministic code blocks.")
        user_input = st.text_area("Example: 'The agent should never call network APIs after 6 PM or access the database without a valid ticket ID.'")
        if st.button("Generate Policy Blocks"):
            st.code("""
# Generated Policy-as-Code (Mahaakali DSL)
def check_time_and_ticket(action):
    if action.type == "network" and current_time() > "18:00":
        return DENY("After-hours network restriction")
    if action.type == "db_access" and not action.meta.get("ticket_id"):
        return DENY("Missing Ticket ID for DB access")
    return ALLOW
            """, language="python")

# --- Page: Compliance Mapping ---
elif menu == "Compliance Mapping":
    st.title("📋 Compliance & Standards Mapping")
    st.write("A visual map of how Mahaakali v3 controls align with global security frameworks.")
    
    compliance_df = load_mock_compliance()
    st.table(compliance_df)
    
    st.subheader("Framework Coverage Index")
    st.progress(0.85, text="EU AI Act - 85% Compliant (Pending TEE finalization)")
    st.progress(0.92, text="NIST AI RMF - 92% Compliant")
    st.progress(0.78, text="ISO/IEC 42001 - 78% Compliant")

# --- Page: Safety & HITL Dashboard ---
elif menu == "Safety & HITL Dashboard":
    st.title("🚨 Safety & HITL Central")
    st.write("Real-time Human-in-the-loop intervention queue.")

    st.warning("High-Risk Decisions require your approval.")
    
    queue_data = [
        {"timestamp": "2026-02-12 17:15", "Agent": "Marketing-Agent-1", "Action": "Send Email Blast", "Confidence": 72, "Reason": "External Domain"},
        {"timestamp": "2026-02-12 17:28", "Agent": "System-Admin-BOT", "Action": "Modify Firewall", "Confidence": 45, "Reason": "Non-standard Port"},
    ]
    
    for item in queue_data:
        with st.container():
            col_a, col_b, col_c = st.columns([1, 3, 1])
            col_a.write(f"**{item['Agent']}**")
            col_b.write(f"Action: `{item['Action']}` | Reason: _{item['Reason']}_")
            if col_c.button("Approve", key=item['timestamp']):
                st.write("Action Propagated.")
            st.divider()

# --- Page: Supply Chain (AIBOM) ---
elif menu == "Supply Chain (AIBOM)":
    st.title("📦 AIBOM Explorer")
    st.write("Signed AI Bill of Materials for every agent in the environment.")
    
    if os.path.exists("simulation_aibom.json"):
        with open("simulation_aibom.json", "r") as f:
            aibom_data = json.load(f)
        st.json(aibom_data)
    else:
        st.info("No AIBOM data found. Run a simulation to generate records.")

# --- Page: Sovereign OS Control ---
elif menu == "Sovereign OS Control":
    st.title("💻 Mahaakali Sovereign OS")
    st.write("Local system health and hardware-rooted trust configuration.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hardware Status (Local)")
        st.metric("GPU Temperature (RTX 4090)", "65°C")
        st.metric("VRAM Usage", "14.2 GB / 24 GB")
    with col2:
        st.subheader("Trust Configuration")
        st.checkbox("Enable TPM Hardware Attestation", value=True)
        st.checkbox("Immutable Log Storage (Sovereign Array)", value=True)
        st.selectbox("OS Variant", ["Mahaakali Debian (Hardened)", "Mahaakali Kali (Offensive Labs)"])

    st.subheader("Scanning Agent Schedule")
    st.slider("Off-Peak Scanning Window (Hours)", 0, 24, (2, 5))
    st.button("Run Full Agentic Swarm Audit (Off-Peak)")
