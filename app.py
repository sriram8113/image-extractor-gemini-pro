from dotenv import load_dotenv


load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_pro_vision_output(input, image, prompt):
    response1 = model.generate_content([input, image[0], prompt])
    return response1.text



def input_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data" : bytes_data
            }
        ] 
        return image_parts
    
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Gemini Invoice Extractor", page_icon="🔮", layout="wide")

st.header("Extractor data from image - GEMINI PRO")
input  = st.text_input("Enter the input Prompt", key = "input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", 'jpeg'])

image  = ''



if uploaded_file is not None:
      image = Image.open(uploaded_file)
      st.image(image, caption='Uploaded Image.', use_column_width=True)   

submit = st.button('Tell me about invoice')

input_prompt = """
you are an expert in reading tax documents. we will upload an tax document image and you will answer questions about the invoice."""

if submit:
    image_data = input_image(uploaded_file)
    response = get_gemini_pro_vision_output(input_prompt, image_data, input)
    st.subheader("Response is ")
    st.write(response)
