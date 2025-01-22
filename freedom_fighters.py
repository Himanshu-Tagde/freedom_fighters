import streamlit as st
import pandas as pd
import wikipedia
from PIL import Image
import requests
from io import BytesIO
import random

# Function to fetch detailed information about the freedom fighter from Wikipedia
def fetch_wikipedia_info(person_name):
    try:
        
        summary = wikipedia.summary(person_name, sentences=5) 
        
       
        page_url = wikipedia.page(person_name).url
        
       
        img_url = None
        try:
            img_url = wikipedia.page(person_name).images[0]  
        except Exception as e:
            img_url = None  
        
        return summary, img_url, page_url
    except wikipedia.exceptions.DisambiguationError as e:
        return "Sorry, too many results. Please be more specific.", None, None
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Request timed out. Please try again.", None, None
    except wikipedia.exceptions.RedirectError:
        return "This page redirects to another one. Try again later.", None, None
    except wikipedia.exceptions.PageError:
        return "Sorry, no page found for this freedom fighter.", None, None

# Function to resize the image to 255x255 pixels
def resize_image(image_url):
    try:
        
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Resize the image to 255x255 pixels
        img_resized = img.resize((255, 255))
        
        return img_resized
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None

# Function to fetch answers to predefined questions and create random options
def generate_question_options(fighter_name, question):
    # Answer based on CSV file details
    fighter_details = fighters_data[fighters_data['Name'] == fighter_name]
    
    if not fighter_details.empty:
        if 'major contribution' in question.lower():
            correct_answer = fighter_details['Major Contributions'].values[0]
        elif 'role in freedom movement' in question.lower():
            correct_answer = fighter_details['Role in Freedom Movement'].values[0]
        elif 'legacy' in question.lower():
            correct_answer = fighter_details['Legacy'].values[0]
        else:
            return [], None  
        
       
        other_fighters = fighters_data[fighters_data['Name'] != fighter_name]
        random_incorrect_answers = other_fighters.sample(n=3)  
        
        if 'major contribution' in question.lower():
            incorrect_answers = random_incorrect_answers['Major Contributions'].tolist()
        elif 'role in freedom movement' in question.lower():
            incorrect_answers = random_incorrect_answers['Role in Freedom Movement'].tolist()
        elif 'legacy' in question.lower():
            incorrect_answers = random_incorrect_answers['Legacy'].tolist()
        
        # Mix correct answer with random incorrect answers
        all_options = incorrect_answers + [correct_answer]
        random.shuffle(all_options)  # Shuffle the options
        
        return all_options, correct_answer
    else:
        return [], None

# Title of the app
st.title("Learn About Indian Freedom Fighters")

# Load the CSV file with freedom fighters' names
csv_file_path = 'freedom_fighters.csv'
try:
    fighters_data = pd.read_csv(csv_file_path)
    st.success("CSV file loaded successfully.")
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    fighters_data = None

if fighters_data is not None:
    
    st.write(f"Columns in the CSV file: {fighters_data.columns.tolist()}")
    
    fighters_list = fighters_data['Name'].tolist()

    
    selected_fighter = st.selectbox("Select an Indian Freedom Fighter", fighters_list)

   
    if selected_fighter:
        st.header(f"About {selected_fighter}")
        
        # Fetch data from Wikipedia
        info, img_url, page_url = fetch_wikipedia_info(selected_fighter)
        
        # Display the information in a presentable way
        if info:
            st.subheader("Biography:")
            st.write(info)
        
        # Display the image if available
        if img_url:
            st.subheader(f"Image of {selected_fighter}")
            img_resized = resize_image(img_url)
            if img_resized:
                st.image(img_resized, caption=f"{selected_fighter} Image")
            else:
                st.write("No image found.")
        
        # Display the link to the full Wikipedia page
        if page_url:
            st.subheader("Learn More:")
            st.write(f"[Read more on Wikipedia]({page_url})")
        
        # Fetch other details from CSV
        fighter_details = fighters_data[fighters_data['Name'] == selected_fighter]
        
        if not fighter_details.empty:
            # Ensure all details are displayed
            st.subheader("Major Contributions:")
            st.write(fighter_details['Major Contributions'].values[0])
            
            st.subheader("Role in Freedom Movement:")
            st.write(fighter_details['Role in Freedom Movement'].values[0])
            
            st.subheader("Legacy:")
            st.write(fighter_details['Legacy'].values[0])
        
            # Check if there are any other relevant columns
            other_columns = fighter_details.drop(columns=['Name', 'Major Contributions', 'Role in Freedom Movement', 'Legacy'])
            if not other_columns.empty:
                st.subheader("Other Details:")
                for col in other_columns.columns:
                    st.write(f"{col}: {other_columns[col].values[0]}")
    
    # Predefined Questions Section
    st.subheader("Ask a Question About the Selected Freedom Fighter")
    
    # Define predefined questions
    question_options = [
        "What were the major contributions of this freedom fighter?",
        "What was the role of this freedom fighter in the freedom movement?",
        "What is the legacy of this freedom fighter?"
    ]
    
    # Let user select a question
    selected_question = st.selectbox("Choose a question:", question_options)
    
    # Generate random options for the selected question
    if selected_question:
        options, correct_answer = generate_question_options(selected_fighter, selected_question)
        
        if options:
            # Show the question and options using radio buttons
            user_answer = st.radio(f"Select the correct answer to: {selected_question}", options)
            
            # Add Submit Button to check the answer
            submit_button = st.button("Submit Answer")
            
            # Check the answer after user clicks submit
            if submit_button:
                if user_answer == correct_answer:
                    st.success("Correct! Well done.")
                else:
                    st.error("Oops! That's incorrect. Try again.")
