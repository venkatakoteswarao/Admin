
import os
import json
import streamlit as st

# Define directory paths
VIDEO_DIR = "assets/uploaded_videos"
QUIZ_DIR = "assets/quiz_data"
METADATA_FILE = "assets/video_metadata.json"

# Function to initialize directories and files
def initialize_app():
    try:
        os.makedirs(VIDEO_DIR, exist_ok=True)
        os.makedirs(QUIZ_DIR, exist_ok=True)
        if not os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, "w") as f:
                f.write("{}")  # Initialize with an empty JSON object
    except Exception as e:
        st.error(f"Error initializing directories or files: {e}")

# Call the initialization function
initialize_app()

# Load video metadata
def load_video_metadata():
    try:
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("Metadata file not found. Creating a new one.")
        return {}
    except json.JSONDecodeError as e:
        st.error(f"Error reading metadata file: {e}")
        return {}

# Save video metadata
def save_video_metadata(metadata):
    try:
        with open(METADATA_FILE, "w") as f:
            json.dump(metadata, f)
    except Exception as e:
        st.error(f"Error saving metadata file: {e}")

# Load quizzes
def load_quizzes():
    quizzes = []
    try:
        for file in os.listdir(QUIZ_DIR):
            if file.endswith(".txt"):
                with open(os.path.join(QUIZ_DIR, file), "r") as f:
                    quizzes.append(f.read())
    except Exception as e:
        st.error(f"Error loading quizzes: {e}")
    return quizzes

# Admin View
def admin_view():
    st.title("Admin Dashboard")
    tab1, tab2 = st.tabs(["Manage Quizzes", "Manage Videos"])

    # Manage Quizzes
    with tab1:
        st.subheader("Create and Manage Quizzes")
        quiz_name = st.text_input("Quiz Title")
        quiz_content = st.text_area("Quiz Content")

        if st.button("Create Quiz"):
            if quiz_name and quiz_content:
                try:
                    with open(os.path.join(QUIZ_DIR, f"{quiz_name}.txt"), "w") as f:
                        f.write(quiz_content)
                    st.success("Quiz created successfully!")
                except Exception as e:
                    st.error(f"Error creating quiz: {e}")
            else:
                st.warning("Please enter both a title and content!")

        st.subheader("Existing Quizzes")
        quizzes = load_quizzes()
        for idx, quiz in enumerate(quizzes):
            st.markdown(f"**Quiz {idx + 1}:**")
            st.text(quiz)
            if st.button(f"Delete Quiz {idx + 1}", key=f"delete_quiz_{idx}"):
                try:
                    os.remove(os.path.join(QUIZ_DIR, f"{quiz.splitlines()[0]}.txt"))
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error deleting quiz: {e}")

    # Manage Videos
    with tab2:
        st.subheader("Upload and Manage Videos")
        uploaded_file = st.file_uploader("Upload a Video", type=["mp4", "avi", "mkv"])
        video_description = st.text_area("Video Description")

        if st.button("Upload Video"):
            if uploaded_file and video_description:
                try:
                    video_path = os.path.join(VIDEO_DIR, uploaded_file.name)
                    with open(video_path, "wb") as f:
                        f.write(uploaded_file.read())

                    metadata = load_video_metadata()
                    metadata[uploaded_file.name] = video_description
                    save_video_metadata(metadata)

                    st.success("Video uploaded successfully!")
                except Exception as e:
                    st.error(f"Error uploading video: {e}")
            else:
                st.warning("Please upload a video and provide a description!")

        st.subheader("Uploaded Videos")
        metadata = load_video_metadata()
        for video_name, description in metadata.items():
            st.video(os.path.join(VIDEO_DIR, video_name))
            st.markdown(f"**Description:** {description}")
            if st.button(f"Delete {video_name}", key=f"delete_video_{video_name}"):
                try:
                    os.remove(os.path.join(VIDEO_DIR, video_name))
                    del metadata[video_name]
                    save_video_metadata(metadata)
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error deleting video: {e}")

# User View
def user_view():
    st.title("User Dashboard")
    st.subheader("Available Quizzes")
    quizzes = load_quizzes()
    if quizzes:
        for idx, quiz in enumerate(quizzes):
            st.markdown(f"**Quiz {idx + 1}:**")
            st.text(quiz)
    else:
        st.info("No quizzes available!")

    st.subheader("Available Videos")
    metadata = load_video_metadata()
    if metadata:
        for video_name, description in metadata.items():
            st.video(os.path.join(VIDEO_DIR, video_name))
            st.markdown(f"**Description:** {description}")
    else:
        st.info("No videos available!")

# Main Application Logic
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Choose View", ["Admin Login", "User View"])

    if choice == "Admin Login":
        st.title("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "tysontony" and password == "kotiKoti123":
                st.success("Logged in as Admin")
                admin_view()
            else:
                st.error("Invalid Credentials!")

    elif choice == "User View":
        user_view()

if __name__ == "__main__":
    main()
