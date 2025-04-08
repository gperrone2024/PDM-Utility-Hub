import streamlit as st

def show_page():
    # Page config
    st.set_page_config(
        page_title="Image Renamer",
        page_icon="🖼️",
        layout="centered"
    )
    
    # Back button
    if st.button("← Back to Hub", type="primary"):
        del st.session_state.current_page
        st.rerun()
    
    # Page content
    st.title("🖼️ Repository Image Download & Renaming")
    st.write("Your image renaming tool content goes here...")
