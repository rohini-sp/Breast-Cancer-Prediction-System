import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np


# Load the data
def load_data():
    data = pd.read_csv("C:\\Users\\SHYAM\\OneDrive\\Desktop\\breast cancer prediction\\dataset\\data.csv")
    return data

data = load_data()

# Add the sidebar
def add_sidebar(data):
    st.sidebar.header("Cell Nuclei Measurements")
    
    # Define the labels
    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}

    # Add the sliders
    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label,
            min_value=float(data[key].min()),
            max_value=float(data[key].max()),
            value=float(data[key].mean())
        )
    
    return input_dict


def get_scaled_values_dict(values_dict):
    # Define a Function to Scale the Values based on the Min and Max of the Predictor in the Training Data
    data = load_data()
    X = data.drop(['diagnosis'], axis=1)

    scaled_dict = {}

    for key, value in values_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
 
    return scaled_dict



def add_radar_chart(input_dict):
    # Scale the values
    input_dict = get_scaled_values_dict(input_dict)

    # Create the radar chart
    fig = go.Figure()

    # Add the traces
    fig.add_trace(
        go.Scatterpolar(
            r=[input_dict['radius_mean'], input_dict['texture_mean'], input_dict['perimeter_mean'],
                input_dict['area_mean'], input_dict['smoothness_mean'], input_dict['compactness_mean'],
                input_dict['concavity_mean'], input_dict['concave points_mean'], input_dict['symmetry_mean'],
                input_dict['fractal_dimension_mean']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points',
                   'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Mean'
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[input_dict['radius_se'], input_dict['texture_se'], input_dict['perimeter_se'], input_dict['area_se'],
                input_dict['smoothness_se'], input_dict['compactness_se'], input_dict['concavity_se'],
                input_dict['concave points_se'], input_dict['symmetry_se'], input_dict['fractal_dimension_se']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points',
                   'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Standard Error'
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[input_dict['radius_worst'], input_dict['texture_worst'], input_dict['perimeter_worst'],
                input_dict['area_worst'], input_dict['smoothness_worst'], input_dict['compactness_worst'],
                input_dict['concavity_worst'], input_dict['concave points_worst'], input_dict['symmetry_worst'],
                input_dict['fractal_dimension_worst']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points',
                   'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Worst'
        )
    )

    # Update the layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        autosize=True
    )

    return fig




# Import the scaler and model
scaler = pickle.load(open("C:\\Users\\SHYAM\\OneDrive\\Desktop\\breast cancer prediction\\model\\scaler.pkl", "rb"))
model = pickle.load(open("C:\\Users\\SHYAM\\OneDrive\\Desktop\\breast cancer prediction\\model\\model.pkl", "rb"))


def display_predictions(input_data, model, scaler):
    
    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_data_scaled = scaler.transform(input_array)
    prediction = model.predict(input_data_scaled)

    st.subheader('Cell cluster prediction')
    st.write("The cell cluster is: ")

    if prediction[0] == 0:
        st.write("<span class='diagnosis bright-green'>Benign</span>",
                 unsafe_allow_html=True)
    else:
        st.write("<span class='diagnosis bright-red'>Malignant</span>",
                 unsafe_allow_html=True)

    st.write("Probability of being benign: ",
             model.predict_proba(input_data_scaled)[0][0])
    st.write("Probability of being malignant: ",
             model.predict_proba(input_data_scaled)[0][1])
    



def main():
    """st.set_page_config(
        page_title = "Breast Cancer Predictor",
        page_icon =":female-doctor",
        layout="wide", 
        initial_sidebar_state="expanded"
    )"""

    #importing css file
    with open("C:\\Users\\SHYAM\\OneDrive\\Desktop\\breast cancer prediction\\assets\\style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
 
    # Add the sidebar
    input_dict = add_sidebar(data)


    # Set up the structure
    with st.container():
        st.title("Breast Cancer Diagnosis")
        #st.write("Please connect this app to your cytology lab to help diagnose breast cancer form your tissue sample. This app predicts using a machine learning model whether a breast mass is benign or malignant based on the measurements it receives from your cytosis lab. You can also update the measurements by hand using the sliders in the sidebar. ")
        col1, col2 = st.columns([4,1])
        with col1:
            radar_chart = add_radar_chart(input_dict)
            st.plotly_chart(radar_chart, use_container_width=True)
        with col2:
            display_predictions(input_dict, model, scaler)

if __name__ == "__main__":
    main()