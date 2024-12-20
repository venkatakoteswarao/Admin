import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App Title
st.title("Sample Streamlit Application")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Data Visualization", "Upload Data"])

# Home Page
if page == "Home":
    st.header("Welcome to the Sample Streamlit App")
    st.write("This app demonstrates the basic features of Streamlit.")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=300)

# Data Visualization Page
elif page == "Data Visualization":
    st.header("Interactive Data Visualization")

    # Generate sample data
    st.write("Below is a random dataset for demonstration:")
    data = pd.DataFrame(np.random.randn(10, 3), columns=["Column A", "Column B", "Column C"])
    st.dataframe(data)

    # Line chart
    st.line_chart(data)

    # Matplotlib chart
    st.subheader("Histogram")
    fig, ax = plt.subplots()
    ax.hist(data["Column A"], bins=10, color="skyblue", edgecolor="black")
    st.pyplot(fig)

# Upload Data Page
elif page == "Upload Data":
    st.header("Upload Your CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded dataset:")
        st.dataframe(df)

        # Show basic statistics
        st.subheader("Basic Statistics")
        st.write(df.describe())

        # Show a checkbox for plotting
        if st.checkbox("Show Scatter Plot"):
            x_col = st.selectbox("Choose X-axis column:", df.columns)
            y_col = st.selectbox("Choose Y-axis column:", df.columns)
            st.write(f"Scatter plot between {x_col} and {y_col}")
            st.scatter_chart(df[[x_col, y_col]])

# Footer
st.sidebar.info("Developed using Streamlit.")
