import streamlit as st

st.set_page_config(page_title="My First Streamlit App")

st.title("🌟 Hello! I deployed my first Streamlit App")
st.write("If you are seeing this, my deployment worked 😄")

name = st.text_input("Enter your name")

if name:
    st.success(f"Welcome {name} 🎉")

st.button("Click me")
