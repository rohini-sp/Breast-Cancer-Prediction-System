import streamlit as st
import firebase_admin
from firebase_admin import credentials
import json
import requests

cred = credentials.Certificate("C://Users//SHYAM//OneDrive//Desktop//breast cancer prediction//app//breastcyt-pro-firebase-adminsdk-t4qrz-ece1683c46.json")
try:
    default_app = firebase_admin.get_app()
except ValueError:
    default_app = firebase_admin.initialize_app(cred)

def sign_up_with_email_and_password(email, password, return_secure_token=True):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        }
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyAlUv79xeDuaU2ng8SMZFGmVvYQGhwqhH4"}, data=payload)
        try:
            return r.json()['email']
        except:
            st.warning(r.json())
    except Exception as e:
        st.warning(f'Signup failed: {e}')

def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    try:
        payload = {
            "returnSecureToken": return_secure_token
        }
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyAlUv79xeDuaU2ng8SMZFGmVvYQGhwqhH4"}, data=payload)
        try:
            data = r.json()
            user_info = {
                'email': data['email']
            }
            return user_info
        except:
            st.warning(data)
    except Exception as e:
        st.warning(f'Signin failed: {e}')

def reset_password(email):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
        payload = {
            "email": email,
            "requestType": "PASSWORD_RESET"
        }
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyAlUv79xeDuaU2ng8SMZFGmVvYQGhwqhH4"}, data=payload)
        if r.status_code == 200:
            return True, "Reset email Sent"
        else:
            error_message = r.json().get('error', {}).get('message')
            return False, error_message
    except Exception as e:
        return False, str(e)

def app():
    st.title('Welcome to BreastCyt Pro')

    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f(): 
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.useremail = userinfo['email']
            st.session_state.signedout = True
            st.session_state.signout = True    
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.useremail = ''

    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]:
        choice = st.sidebar.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            if st.button('Create my account'):
                sign_up_with_email_and_password(email=email, password=password)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
        else:
            st.button('Login', on_click=f)
            forget()

    if st.session_state.signout:
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

app()
