"""import streamlit as st

from streamlit_option_menu import option_menu


import home, login1, prediction, correlation
st.set_page_config(
        page_title="BreastCyt Pro",
)



class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():

        def is_user_logged_in():
            return st.session_state.login
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='BreastCyt Pro ',
                options=['Home','Account','Prediction System','Correlation Matrix'],
                icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Home":
            home.app()
        if app == "Account":
            login1.app()    
        if app == "Prediction System":
            prediction.main() 
                  
        if app == 'Correlation Matrix':
            correlation.main()  

              
             
          
             
    run()      

"""
 

import streamlit as st
from streamlit_option_menu import option_menu
import home, login1, prediction, correlation

st.set_page_config(page_title="BreastCyt Pro")


# Define a session state variable for tracking login status
if 'login' not in st.session_state:
    st.session_state.login = False

def login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Call your login function here
        userinfo = login1.sign_in_with_email_and_password(email, password)
        print("Userinfo:", userinfo)  # Debug output
        if userinfo:
            st.session_state.useremail = userinfo['email']
            st.session_state.login = True
            st.success("Login successful")
            st.write("Login status:", st.session_state.login)
        else:
            st.error("Invalid email or password")


def is_user_logged_in():
    return st.session_state.login
#debug
print("Session state login:", st.session_state.login)
print("Session state useremail:", st.session_state.get("useremail", "Not logged in"))



class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Define the sidebar menu
        with st.sidebar:        
            app = option_menu(
                menu_title='BreastCyt Pro',
                options=['Home', 'Account', 'Prediction System', 'Correlation Matrix'],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Check if the user is logged in before displaying certain pages
        if app == "Home":
            home.app()
        elif app == "Account":
            login1.app()
        
        if app == "Prediction System":
            prediction.main() 
        elif app == 'Correlation Matrix':
                correlation.main()
        else:
            st.write("Please log in to access this page.")

# Create an instance of MultiApp
multi_app = MultiApp()

# Add apps to the multi-app instance
multi_app.add_app("Home", home.app)
multi_app.add_app("Account", login1.app)
multi_app.add_app("Prediction System", prediction.main)
multi_app.add_app("Correlation Matrix", correlation.main)

# Run the multi-app
multi_app.run()


