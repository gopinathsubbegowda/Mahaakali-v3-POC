# Mahaakali v3 - Agentic AI Security Trust Plane (POC)

Mahaakali v3 is an autonomous security layer designed to provide a "Trust Plane" for AI Agents. This POC demonstrates core architectural concepts including Signed AIBOMs, Policy-as-Code enforcement, and a safety Circuit Breaker.

## 🚀 Key Features
- **Deterministic Trust Plane**: Central orchestrator for agent safety.
- **Signed AIBOM**: supply chain tracking for AI models and tools.
- **Policy-as-Code**: Human-readable and machine-executable governance rules.
- **Visual Dashboard**: Streamlit-based control center for monitoring and real-time HITL (Human-in-the-loop).

## 🛠️ Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Mahaakali
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements_8gb.txt
   pip install streamlit plotly
   ```
3. **Run the Simulation**:
   ```bash
   python poc/mock_agent.py
   ```
4. **Launch the Trust Plane UI**:
   ```bash
   python -m streamlit run poc/app.py
   ```

## 📂 Structure
- `poc/`: Core Trust Plane implementation.
- `poc/app.py`: Streamlit Dashboard.
- `poc/trust_plane.py`: Central Security Orchestrator.
- `poc/policies.py`: Policy-as-Code Engine.

---
*Developed as part of the Mahaakali Autonomous System initiative.*
