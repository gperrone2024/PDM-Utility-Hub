import streamlit as st

def show_page():
    # Page config
    st.set_page_config(
        page_title="Bundle Creator",
        page_icon="📦",
        layout="centered"
    )
    
    # Back button
    if st.button("← Back to Hub", type="primary"):
        del st.session_state.current_page
        st.rerun()
    
    # Page content
    st.title("📦 Bundle & Set Images Creator")
    st.write("Your bundle creator content goes here...")
