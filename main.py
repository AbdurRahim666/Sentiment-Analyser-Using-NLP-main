import streamlit as st
import matplotlib.pyplot as plt
import string
from collections import Counter

# python -m streamlit run main.py

# CSS for futuristic look
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: #39ff14;
        font-family: 'Courier New', monospace;
    }
    .stTextArea, .stTextInput {
        background-color: #111 !important;
        color: #39ff14 !important;
        border: 1px solid #39ff14 !important;
    }
    .css-1offfwp {
        background-color: #111 !important;
    }
    .stButton>button {
        background-color: #222;
        color: #39ff14;
        border: 1px solid #39ff14;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💡 Emotion Detector")
st.markdown("Enter your text and watch the emotions light up 💥")

user_input = st.text_area("Enter Text Here", height=200)

def clean_text(text):
    lower_cased = text.lower()
    return lower_cased.translate(str.maketrans('', '', string.punctuation))

def remove_stopwords(words):
    stop_words = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
                      "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her",
                      "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
                      "themselves", "what", "which", "who", "whom", "this", "that", "these", "those",
                      "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                      "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
                      "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
                      "against", "between", "into", "through", "during", "before", "after", "above",
                      "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
                      "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                      "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
                      "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
                      "will", "just", "don", "should", "now"])
    return [word for word in words if word not in stop_words]

def extract_emotions(words):
    emotion_list = []
    try:
        with open('emotions.txt', 'r') as file:
            for line in file:
                clean_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clean_line.split(':')
                if word in words:
                    emotion_list.append(emotion)
    except FileNotFoundError:
        st.error("😢 'emotions.txt' not found. Please upload it.")
    return emotion_list

def plot_emotions(emotion_count):
    fig, ax = plt.subplots()
    ax.bar(emotion_count.keys(), emotion_count.values(), color='#39ff14')
    ax.set_title("Detected Emotions", color='white')
    ax.set_facecolor('#111')
    fig.patch.set_facecolor('#111')
    ax.tick_params(colors='white')
    st.pyplot(fig)

if st.button("🧠 Analyze Emotions"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        cleaned = clean_text(user_input)
        words = cleaned.split()
        final_words = remove_stopwords(words)
        emotions_detected = extract_emotions(final_words)
        emotion_count = Counter(emotions_detected)

        if emotion_count:
            st.success("Emotions detected!")
            plot_emotions(emotion_count)
        else:
            st.info("No emotions detected in the text.")