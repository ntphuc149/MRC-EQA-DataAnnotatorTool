import pandas as pd
import streamlit as st
import re
import numpy as np

st.set_page_config(page_icon='🍃', page_title='MRC for Legal Document Dataset checker', layout='wide', initial_sidebar_state="collapsed")

st.markdown("<h2 style='text-align: center;'>Investigation Legal Dataset checker for Machine Reading Comprehension</h2>", unsafe_allow_html=True)

df = pd.read_csv(filepath_or_buffer=r'./Datasets/data_unverified.csv')


if 'idx' not in st.session_state:
    st.session_state.idx = 0

st.markdown(f"<h4 style='text-align: center;'>Sample {st.session_state.idx + 1}/{len(df)}</h4>", unsafe_allow_html=True)

col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9, col_10 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

btn_previous = col_1.button(label=':arrow_backward: Previous sample', use_container_width=True)
btn_next = col_2.button(label='Next sample :arrow_forward:', use_container_width=True)
btn_save = col_3.button(label=':heavy_check_mark: Save change', use_container_width=True)
txt_goto = col_5.selectbox(label='Sample', label_visibility='collapsed', options=list(range(1, len(df) + 1)))
btn_goto = col_6.button(label=':fast_forward: Move to', use_container_width=True)

if len(df) != 0:
    col_x1, col_x2 = st.columns([8.5, 1.5])
    txt_context = col_x1.text_area(height=300, label='Your context:', value=df['context'][st.session_state.idx])
    txt_question = st.text_area(height=100, label='Your question:', value=df['question'][st.session_state.idx])
    txt_answer = st.text_area(height=100, label='Your answer:', value=df['answer'][st.session_state.idx])

    if txt_answer.strip() and txt_context.strip():
        highlighted_context = re.sub(re.escape(txt_answer), "<mark>" + txt_answer + "</mark>", txt_context, flags=re.IGNORECASE)
        st.markdown(highlighted_context, unsafe_allow_html=True)

    if btn_previous:
        if st.session_state.idx > 0:
            st.session_state.idx -= 1
            st.rerun()
        else:
            pass

    if btn_next:
        if st.session_state.idx < (len(df) - 1):
            st.session_state.idx += 1
            st.rerun()
        else:
            pass
    
    if btn_save:
        df['context'][st.session_state.idx] = txt_context
        df['question'][st.session_state.idx] = txt_question
        df['answer'][st.session_state.idx] = txt_answer

        btn_download = col_4.download_button(data=df.to_csv(), label=':arrow_down_small: Download file', use_container_width=True, file_name="checked.csv", mime="text/csv")
        df.to_csv(path_or_buf=r'./Datasets/data_unverified.csv', index=None)

    if btn_goto:
        st.session_state.idx = txt_goto - 1
        st.rerun()