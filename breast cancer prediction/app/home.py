import streamlit as st

def app():
    
    st.title('Welcome to BreastCyt Pro')

    st.write("""
    This web app provides a platform for breast cancer prediction using cytology data.
    Please choose an option from the sidebar to get started.
    """)


    st.header('About the Project')
    st.write("""
    Breast cancer is one of the most common cancers among women worldwide. Early detection 
    and prediction of breast cancer can significantly improve treatment outcomes. This project 
    aims to provide a predictive model for breast cancer risk assessment along with correlation between different factors.
    """)

app()