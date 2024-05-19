import streamlit as st
import pandas as pd

def column_transformer_form(X, select_block):
    if select_block not in st.session_state:
                    st.session_state[select_block] = {}
                    st.session_state[select_block]['cat_num_select_output1'] = 'categorical'
                    st.session_state[select_block]['cat_num_select_output2'] = 'numerical'
                    st.session_state[select_block]['columns_output1'] = []
                    st.session_state[select_block]['columns_output2'] = []
                    st.session_state[select_block]['remainder'] = False
    st.write("Select the target column and predictors:")
    categorical_columns = list(X.select_dtypes(include='object').columns)
    numerical_columns = list(X.select_dtypes(exclude='object').columns)
    type_select = ['categorical', 'numerical', 'list']
    index_output1 = type_select.index(st.session_state[select_block]['cat_num_select_output1'])
    st.session_state[select_block]['cat_num_select_output1'] = st.selectbox('Select for output 1', ['categorical', 'numerical', 'list'], index=index_output1)
    if st.session_state[select_block]['cat_num_select_output1'] == 'list':
        st.session_state[select_block]['columns_output1'] = st.multiselect('Select the columns for output 1:', categorical_columns + numerical_columns, default=st.session_state[select_block]['columns_output1'])

    index_output2 = type_select.index(st.session_state[select_block]['cat_num_select_output2'])
    st.session_state[select_block]['cat_num_select_output2'] = st.selectbox('Select for output 2', ['categorical', 'numerical', 'list'], index=index_output2)
    if st.session_state[select_block]['cat_num_select_output2'] == 'list':
        st.session_state[select_block]['columns_output2'] = st.multiselect('Select the columns for output 2:', categorical_columns + numerical_columns, default=st.session_state[select_block]['columns_output2'])
    st.session_state[select_block]['remainder'] = st.checkbox('Remainder', value=st.session_state[select_block]['remainder'])

def else_form():
    st.write('This functionality is not available yet.')

def show_form(X, barfi, select_block):
    if len(barfi) != 0:
        if select_block is not None:
            type_block = barfi[select_block]['type']
            if type_block == 'Column Transformer':
                column_transformer_form(X, select_block)
            else:
                else_form()
        else:
            st.write('Please select a block')
    else:
         st.write('Please click on "Execute"')