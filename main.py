import box
import timeit
import yaml
import argparse
from dotenv import find_dotenv, load_dotenv
from src.utils import setup_dbqa
import streamlit as st
from PIL import Image

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

def main():
    st.title("DocQnA ChatBot")
    image = Image.open('assets/diagram_flow.png')
    st.image(image, '')
    st.write("Enter your message below and press Enter to get the response from the chatbot.")

    user_input = st.text_input("User Input:", "")

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a message.")
        else:
            with st.spinner("Getting response..."):
                dbqa = setup_dbqa()
                response = dbqa({'query': user_input})
                st.write("Chatbot:", response["result"])
                st.write("="*60)
                source_docs = response['source_documents']
                for i, doc in enumerate(source_docs):
                    st.write(f'\nSource Document {i+1}\n')
                    st.write(f'Source Text: {doc.page_content}')
                    st.write(f'Document Name: {doc.metadata["source"]}')
                    st.write(f'Page Number: {doc.metadata["page"]}\n')
                    st.write('='* 60)

if __name__ == "__main__":
    main()