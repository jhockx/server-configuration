import streamlit as st

from pages.page1 import main as page1_main
from pages.page2 import main as page2_main

page = st.sidebar.selectbox('Page:', ['Page 1', 'Page 2'])
if page == 'Page 1':
    page1_main()
elif page == 'Page 2':
    page2_main()
else:
    raise ValueError('Unknown page!')
