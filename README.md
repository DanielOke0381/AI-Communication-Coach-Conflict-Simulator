# AI Conflict Simulation & Communication Coach

An engineered AI communication coach and conflict simulator prototype built in Python using the Streamlit framework and the Google GenAI SDK. This application simulates high-stakes interpersonal conflicts, allowing users to practice conflict resolution skills using structured frameworks like Non-Violent Communication (NVC).

## 🚀 Key Features & Engineering Pillars

### 1. Architectural Scalability (Factory Method Pattern)
The application utilizes a **Factory Method design pattern** to decouple the core user interface from the underlying LLM configurations. This ensures an open/closed architecture where new agent personas (e.g., negotiation coaches, customer relations simulators) can be dynamically instantiated without modifying the core UI rendering logic or introducing code duplication.

### 2. Defensive Programming & Token Optimization
To guarantee system stability and prevent model hallucinations, a custom regex-driven **input validation layer** handles data sanitization at the edge. 
* Catches low-quality inputs and keyboard mashing before hitting the API.
* Drastically optimizes token utilization and mitigates API runtime overhead.
* Safeguards the model from losing its behavioral persona boundaries.

### 3. Context & State Management
* **State-Driven UI/UX:** Leverages persistent runtime session state to manage dynamic visual affordance. Components and action items automatically alter their visibility and visual priority based on the application's immediate lifecycle state.
* **Context Anchoring:** Implements layered system instructions and conversational memory buffers to prevent model drift during extended interactions.

---

## 🛠️ Tech Stack & Architecture

* **Backend Logic:** Python 3
* **AI Engine:** Google GenAI SDK (Gemini API)
* **Frontend UI:** Streamlit (State-managed)
* **Framework Metrics:** Non-Violent Communication (NVC) logic layers

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DanielOke0381/AI-Communication-Coach-Conflict-Simulator.git](https://github.com/DanielOke0381/AI-Communication-Coach-Conflict-Simulator.git)
   cd AI-Communication-Coach-Conflict-Simulator
