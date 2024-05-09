import streamlit as st
from dotenv import load_dotenv
import os

from utils.util import loading_llama_model

os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Loading environment variable.
load_dotenv(".env")
model_llama = os.environ.get("model")
checkpoint_dir_llama = os.environ.get("checkpoint_dir")

# Creating Session state variable
if 'Huggingface_Api_Key' not in st.session_state:
    st.session_state['Huggingface_Api_Key']=''

st.title('🦾 AI assistance for Routine fashion brand')

# Sidebar to capture the Api keys
st.sidebar.title("🤓 🆒")
st.session_state['Huggingface_Api_Key'] = st.sidebar.text_input("Please input your Huggingface Api key")

load_button = st.sidebar.button("Loading Huggingface Api key for operation")

if load_button:
    #Proceed only if Api key is provided.
    if st.session_state['Huggingface_Api_Key'] != "":
        # fetch data from site
        model, tokenizer = loading_llama_model(model_llama, st.session_state['Huggingface_Api_Key'], checkpoint_dir_llama)


    prompt = st.text_input('How can I help you bro ?', key="prompt")
    submit = st.button("Asking")

    if submit:
        batch = tokenizer(prompt, return_tensors="pt")
        output = model.generate(batch["input_ids"], max_length=100)[0]
        decode_output = tokenizer.decode(output)

        # Display the output.
        st.write("Please, wait the result for few seconds......")
        st.write(decode_output)
