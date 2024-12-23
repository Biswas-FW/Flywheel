
import streamlit as st
import pandas as pd
from collections import Counter
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator

# Function to process titles and generate top 1000 words
def process_titles(titles):
    word_counter = Counter()
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)

    for title in titles:
        words = word_tokenize(title)
        words = [word.lower() for word in words if word.lower() not in stop_words and word not in punctuation]
        word_counter.update(words)

    top_1000_words = word_counter.most_common(1000)
    return top_1000_words

# Streamlit App
st.title("Top 1000 Words with Translation")
st.write("Upload a text file or paste your data below:")

# File Upload
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
input_data = st.text_area("Or paste your column data here:")

if uploaded_file:
    titles = uploaded_file.read().decode("utf-8").splitlines()
elif input_data:
    titles = input_data.splitlines()
else:
    titles = []

if st.button("Process Data"):
    if not titles:
        st.error("Please upload a file or enter data!")
    else:
        st.info("Processing data...")
        top_1000 = process_titles(titles)

        # Translate words
        translator = GoogleTranslator(source='auto', target='en')
        translations = [(word, translator.translate(word), freq) for word, freq in top_1000]

        # Convert to DataFrame
        df = pd.DataFrame(translations, columns=["Word", "Translation", "Frequency"])
        st.success("Processing complete!")

        # Show results
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "Top1000.csv", "text/csv", key='download-csv')

st.write("Built with ❤️ using Streamlit!")
