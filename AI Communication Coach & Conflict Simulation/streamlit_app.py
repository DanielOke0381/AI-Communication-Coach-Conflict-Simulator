import streamlit as st
import re
from main import AgentFactory

st.set_page_config(page_title="AI Conflict Lab", page_icon="🌍", layout="centered")

# --- HELPER: GIBBERISH FILTER ---
def is_likely_gibberish(text):
    """Checks for keyboard mashing and low-quality input."""
    if not re.search(r'[aeiouAEIOU]', text):
        return True
    if re.search(r'(.)\1{4,}', text):
        return True
    if len(text.strip().split()) < 2:
        return True
    return False

# --- INITIALIZE STATE ---
if "history_storage" not in st.session_state:
    st.session_state.history_storage = {"Communication Coach": [], "Conflict Simulator": []}

if "clear_key" not in st.session_state:
    st.session_state.clear_key = 0

if "agents" not in st.session_state:
    st.session_state.agents = {
        "Communication Coach": AgentFactory.get_agent("Communication Coach"),
        "Conflict Simulator": AgentFactory.get_agent("Conflict Simulator")
    }

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Lab Settings")
    mode = st.radio("Select Mode:", ["Communication Coach", "Conflict Simulator"])
    
    st.divider()
    current_mode_history = st.session_state.history_storage[mode]

    if mode == "Conflict Simulator":
        p_key = f"persona_input_{st.session_state.clear_key}"
        s_key = f"situation_input_{st.session_state.clear_key}"
        
        persona = st.text_area("Target Persona:", placeholder="e.g., An angry landlord...", key=p_key)
        situation = st.text_area("The Situation:", placeholder="e.g., I'm late with rent...", key=s_key)
        
        has_text = persona.strip() != "" or situation.strip() != ""
        has_history = len(current_mode_history) > 0
        
        # --- AFFORDANCE: START BUTTON (PRIMARY) ---
        if not has_history:
            if st.button("🚀 Start Simulation", use_container_width=True, type="primary"):
                if not persona.strip() or not situation.strip():
                    st.warning("⚠️ Please define both the Persona and Situation.")
                elif is_likely_gibberish(persona) or is_likely_gibberish(situation):
                    st.error("⚠️ Please use real words and provide a more detailed description.")
                else:
                    st.session_state.agents[mode] = AgentFactory.get_agent(mode, persona, situation)
                    with st.spinner("Character is entering..."):
                        opening_instruction = "Based on the persona and situation, start the conflict."
                        ai_start = st.session_state.agents[mode].safe_send([], opening_instruction)
                        st.session_state.history_storage[mode].append({"role": "assistant", "content": ai_start})
                    st.rerun()
        
        # --- AFFORDANCE: RESET & CLEAR (HIERARCHY) ---
        else:
            # Primary: Keep the momentum of the current fight
            if st.button("🔄 Reset Simulation", use_container_width=True, type="primary"):
                st.session_state.history_storage[mode] = []
                st.session_state.agents[mode] = AgentFactory.get_agent(mode, persona, situation)
                st.rerun()
            
            # Secondary: Wipe everything and start over
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.history_storage[mode] = []
                st.session_state.clear_key += 1
                st.rerun()

        # Show Clear button even before Start if there is text to wipe
        if not has_history and has_text:
            if st.button("🗑️ Clear Inputs", use_container_width=True):
                st.session_state.clear_key += 1
                st.rerun()
    
    else: # Coach Mode
        if len(current_mode_history) > 0:
            if st.button("🗑️ Clear Chat", use_container_width=True, type="primary"):
                st.session_state.history_storage[mode] = []
                st.rerun()

# --- MAIN CHAT UI ---
st.title(f"🌍 {mode}")

current_messages = st.session_state.history_storage[mode]
current_agent = st.session_state.agents[mode]

for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if mode == "Conflict Simulator" and len(current_messages) == 0:
    st.info("👋 **Ready to practice?** \n\n Define who I should be and the scenario in the sidebar, then click **Start Simulation**.")

if mode == "Communication Coach" or len(current_messages) > 0:
    if prompt := st.chat_input("Type your response..."):
        st.session_state.history_storage[mode].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = current_agent.safe_send(st.session_state.history_storage[mode][:-1], prompt)
                st.markdown(response)
                st.session_state.history_storage[mode].append({"role": "assistant", "content": response})