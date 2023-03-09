from utils import StreamlitThread
import streamlit as st

# # Set page config
# st.set_page_config(page_title='SL', page_icon=':guardsman:', layout='wide', initial_sidebar_state="auto", menu_items=None)


# st.title('Reconnaissance Faciale et Vocale')
# #adding buttons to start listening (pour pas avoir d'automatisme qui bloque)
# # Create a button with label "Click me"
# button_clicked = st.button("Lancer la reconnaissance vocale")
# # Check if the button was clicked
# if button_clicked:
#     #st.write("Button was clicked!")
StreamlitT = StreamlitThread()
StreamlitT.run()


# from utils import StreamlitThread


# StreamlitT = StreamlitThread()
# StreamlitT.run()