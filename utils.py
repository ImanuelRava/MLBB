import streamlit as st

def display_icon_50px(hero_name):
    """Helper to display a consistent 50px icon or a placeholder."""
    try:
        # Updated path to include the 'hero_icon' folder
        st.image(f"hero_icon/{hero_name}.png", width=50)
    except:
        # Fallback if image is missing
        st.markdown(f"""
            <div style='width: 50px; height: 50px; background-color: #f0f2f6; 
                        display: flex; align-items: center; justify-content: center; 
                        border-radius: 5px; font-size: 10px; color: #555; margin: 0 auto;'>
                {hero_name[:2]}
            </div>
        """, unsafe_allow_html=True)