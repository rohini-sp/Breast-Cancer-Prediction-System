import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
    column_names = ['ID', 'Diagnosis', 'Mean Radius', 'Mean Texture', 'Mean Perimeter', 
                    'Mean Area', 'Mean Smoothness', 'Mean Compactness', 'Mean Concavity', 
                    'Mean Concave Points', 'Mean Symmetry', 'Mean Fractal Dimension']
    data = pd.read_csv(url, header=None, names=column_names)
    return data


def main():
    data = load_data()

    # Streamlit app
    st.title('Interactive Correlation Analysis')
    st.write('Select 2 or 3 features to see the correlation:')

    # Multi-select dropdown for selecting features
    selected_features = st.multiselect('Select features for correlation analysis:', data.columns[2:])

    # Check if at least 2 features are selected
    if len(selected_features) >= 2:
        # Filter the data to selected features
        selected_data = data[selected_features]
        
        # Create correlation matrix
        corr = selected_data.corr()

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 8))  # Adjust size of the plot
        cmap = sns.diverging_palette(240, 10, as_cmap=True)  # Define custom colormap
        sns.heatmap(corr, annot=True, cmap=cmap, fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title('Correlation Heatmap', fontsize=20)  # Set title font size
        plt.xticks(rotation=45, ha='right', fontsize=12)  # Rotate x-axis labels and set font size
        plt.yticks(rotation=45, fontsize=12)  # Rotate y-axis labels and set font size
        plt.xlabel('Features', fontsize=14)  # Set x-axis label and font size
        plt.ylabel('Features', fontsize=14)  # Set y-axis label and font size
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=12)  # Set color bar font size
        plt.tight_layout()  # Adjust layout to prevent cutoff of labels
        st.pyplot(fig)
    else:
        st.write('Please select at least 2 features for correlation analysis.')


if __name__ == "__main__":
    main()