import streamlit as st
import os
import json
import speech_recognition as sr

ffighters = r'ff_images'
question_json ='questions.json'


def load_quiz_questions(file_path):
    """Load quiz questions from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def capture_speech():
    """Capture and process speech input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak your answer.")
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            spoken_text = recognizer.recognize_google(audio)
            return spoken_text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand your speech. Please try again.")
            return None
        except sr.RequestError as e:
            st.error(f"Speech Recognition service is unavailable: {e}")
            return None

# List of Freedom Fighters
freedom_fighters = [
    {"name": "Mahatma Gandhi", "image": "Mahatma Gandhi.jpg", "info": [
        "Born: 2 October 1869, Porbandar, India.",
        "Played a key role in the Indian independence movement through non-violent civil disobedience.",
        "Led several important movements like the Salt March and Quit India Movement.",
        "Known as the 'Father of the Nation'.",
        "Famous for his philosophy of 'Ahimsa' (non-violence).",
        "Assassinated on 30 January 1948."
    ]},
    {"name": "Jawaharlal Nehru", "image": "Jawaharlal Nehru.jpg", "info": [
        "Born: 14 November 1889, Allahabad, India.",
        "The first Prime Minister of India, serving from 1947 to 1964.",
        "A central figure in the Indian independence movement, closely working with Mahatma Gandhi.",
        "Known for his vision of a secular, socialist India, and played a key role in shaping India's policies post-independence.",
        "Author of several works, including his autobiography and 'Discovery of India'.",
        "Died on 27 May 1964."
    ]},
    {"name": "Bhagat Singh", "image": "Bhagat Singh.jpg", "info": [
        "Born: 28 September 1907, Banga, Punjab (now in Pakistan).",
        "One of the most influential revolutionaries in the Indian independence movement.",
        "Known for his acts of rebellion, including the assassination of John Saunders to avenge Lala Lajpat Rai’s death.",
        "Hanged at the age of 23 on 23 March 1931, along with Rajguru and Sukhdev.",
        "Famous for his courage and his slogan 'Inquilab Zindabad'."
    ]},
    {"name": "Sardar Vallabhbhai Patel", "image": "Sardar Vallabhbhai Patel.jpg", "info": [
        "Born: 31 October 1875, Nadiad, Gujarat, India.",
        "Known as the 'Iron Man of India' for his role in uniting the country post-independence.",
        "Served as the first Deputy Prime Minister and the first Minister of Home Affairs.",
        "Played a key role in integrating over 500 princely states into the Indian Union.",
        "Was a key figure in the freedom struggle and the success of the Salt Satyagraha.",
        "Died on 15 December 1950."
    ]},
    {"name": "Lal Bahadur Shastri", "image": "Lal Bahadur Shastri.jpg", "info": [
        "Born: 2 October 1904, Mughalsarai, India.",
        "Second Prime Minister of India, serving from 1964 to 1966.",
        "Known for promoting the White Revolution and the Green Revolution.",
        "Led India to victory in the 1965 war with Pakistan and advocated for peace with neighbors.",
        "Famous for the slogan 'Jai Jawan Jai Kisan'.",
        "Died suddenly in Tashkent, Uzbekistan, in January 1966, under mysterious circumstances."
    ]},
    {"name": "Rani Lakshmibai", "image": "Rani Lakshmibai.jpg", "info": [
        "Born: 19 November 1828, Varanasi, India.",
        "Queen of the princely state of Jhansi, known for her leadership during the 1857 Indian Rebellion.",
        "Led her army in battles against the British East India Company.",
        "Famous for her bravery and determination, she became a symbol of resistance.",
        "Died on 18 June 1858, in battle, while defending Jhansi."
    ]},
    {"name": "Chandra Sekhar Azad", "image": "Chandra Sekhar Azad.jpg", "info": [
        "Born: 23 July 1906, Bhavra, Madhya Pradesh, India.",
        "One of the most prominent revolutionaries in the Indian independence movement.",
        "Played a significant role in the Hindustan Socialist Republican Association (HSRA).",
        "Famous for his slogan 'Dilsay ki Azadi.'",
        "Committed suicide on 27 February 1931, after being surrounded by the police, maintaining his vow to never be captured alive."
    ]},
    {"name": "Dr. B.R. Ambedkar", "image": "Dr. B.R. Ambedkar.jpg", "info": [
        "Born: 14 April 1891, Mhow, Madhya Pradesh, India.",
        "Principal architect of the Constitution of India, advocating for social justice and equality.",
        "A leading figure in the fight against untouchability and caste-based discrimination.",
        "He converted to Buddhism in 1956 and inspired millions of Dalits to follow the path of Buddhism.",
        "First Law Minister of India, and a member of the first Cabinet of Independent India.",
        "Died on 6 December 1956."
    ]},
    {"name": "Mangal Pandey", "image": "Mangal Pandey.jpg", "info": [
        "Born: 19 July 1827, Nagwa, Ballia, India.",
        "Known for his role in the 1857 Indian Rebellion, also called the First War of Indian Independence.",
        "A sepoy in the British East India Company’s army, he sparked the rebellion by attacking his officers.",
        "Famous for his courage and is regarded as one of the first freedom fighters of India.",
        "Hanged on 21 April 1857, for his role in the rebellion."
    ]},
   

    
]

folder_path = ffighters


# Streamlit App
st.title('Freedom Fighters of India')
st.write('Click on any freedom fighter name to see their image and more information.')

if os.path.isdir(folder_path):
    st.write(f"Folder found: {folder_path}")
    quiz_file_path = question_json  
    quiz_questions = load_quiz_questions(quiz_file_path)

    if 'current_fighter' not in st.session_state:
        st.session_state.current_fighter = None

    for fighter in freedom_fighters:
        image_path = os.path.join(folder_path, fighter['image'])

        if st.button(fighter['name']):
            st.session_state.current_fighter = fighter['name']

        if st.session_state.current_fighter == fighter['name']:
            if os.path.exists(image_path):
                st.image(image_path, caption=fighter['name'], width=300)

                if st.button(f"Show Info about {fighter['name']}"):
                    st.write(f"**Details about {fighter['name']}:**")
                    for point in fighter['info']:
                        st.markdown(f"- {point}")
            else:
                st.write("Image not available in the folder.")

            st.write('---')

    # Quiz Section
    with st.expander("Start Quiz"):
        st.subheader("Freedom Fighters Quiz")

        if 'question_index' not in st.session_state:
            st.session_state.question_index = 0

        current_question = quiz_questions[st.session_state.question_index]
        st.subheader(f"{st.session_state.question_index + 1}. {current_question['question']}")

        # Display options
        answer = st.radio(f"Choose your answer for Q{st.session_state.question_index + 1}", options=current_question["options"], key=f"q{st.session_state.question_index}")

        if 'answered' not in st.session_state:
            st.session_state.answered = False
        
        if st.button(f"Submit Answer for Q{st.session_state.question_index + 1}", key=f"submit{st.session_state.question_index}"):
            if answer == current_question["answer"]:
                st.success("Correct!")
            else:
                st.error(f"Wrong! The correct answer is: {current_question['answer']}")
            
           
            st.session_state.answered = True
        
        if st.button(f"Speak Answer for Q{st.session_state.question_index + 1}", key=f"speak{st.session_state.question_index}"):
            spoken_answer = capture_speech()
            if spoken_answer:
                st.write(f"You said: {spoken_answer}")
                if spoken_answer.lower() == current_question["answer"].lower():
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! The correct answer is: {current_question['answer']}")
                   
                st.session_state.answered = True
        
        if st.session_state.answered:
            if st.session_state.question_index + 1 < len(quiz_questions):
                next_question_button = st.button("Next Question")
                if next_question_button:
                    st.session_state.question_index += 1  
                    st.session_state.answered = False  
                    st.rerun()  # Trigger a rerun to refresh the state
            else:
                st.success("Congratulations! You've completed the quiz.")

