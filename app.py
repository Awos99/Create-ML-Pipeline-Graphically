import streamlit as st
import barfi
from blocks.preprocessing import base_blocks
from calc.transform_pipe import create_pipe
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn import set_config
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from hyperparameters_forms.hyper_forms import show_form
from joblib import dump

set_config(transform_output='pandas')

st.set_page_config(layout="wide")

st.title("Machine Learning!!")

file = st.file_uploader("Upload a file", type=["csv"])

if file:
    if st.session_state['demo_123456']:
        print("Deleting session state uploaded file")
        key = 'demo_123456'
        st.session_state = {k: v for k, v in st.session_state.items() if k == key}
        st.session_state['demo_123456'] = False

if not file:
    demo_button = st.button("Use Demo Data")

    if demo_button:
        st.session_state['demo_123456'] = True
        file = "75.csv"
        key = 'demo_123456'
        print("Deleting session state demo button")
        st.session_state = {k: v for k, v in st.session_state.items() if k == key}

try:
    if st.session_state['demo_123456']:
        file = "75.csv"
except:
    pass

print(file)
if file:
    df = pd.read_csv(file, low_memory=False)
    # dropping columns with no observed values
    df = df.dropna(axis=1, how='all')

    with st.form(key='target_column_form'):
        st.write("Select the target column and predictors:")
        target_column = st.selectbox('Select the target column', df.columns)
        predictors = st.multiselect('Select the predictors', df.columns)
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        st.session_state['target_column'] = target_column
        st.session_state['predictors']= predictors
    
    if 'target_column' in st.session_state:
        target_column = st.session_state['target_column']
        df = df.dropna(subset=[target_column])
        X = df[predictors]
        y = df[target_column]


        barfi_schema_name = st.selectbox(
            'Select a saved schema to load:', barfi.barfi_schemas())


        col1, col2 = st.columns([8, 4])
        with col1:
        
            barfi_results = barfi.st_barfi(base_blocks=base_blocks, compute_engine=True, load_schema=barfi_schema_name)
        
        with col2:
            st.title("Change Hyperparameters")
            select_block = st.selectbox('Select the block', barfi_results.keys())
            with st.container(border=True):
                show_form(X, barfi_results, select_block)
                #column_transformer_form(X, select_block)

        try:
            st.write(create_pipe(barfi_results, X))
            if 'fit_model' not in st.session_state:
                st.session_state['fit_model'] = False
            if barfi_results:
                fit_model = st.button("Fit Model")

                if fit_model:
                    st.session_state['fit_model'] = True
                    with st.spinner("Fitting model..."):
                        pipe = create_pipe(barfi_results, X)
                        

                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                        
                        pipe.fit(X_train, y_train)
                        st.write("Model fitted successfully!")
                        st.write("Mean Absolute Error: ", mean_absolute_error(y_test, pipe.predict(X_test)))
                        dump(pipe, "pipeline.pkl")
                if st.session_state['fit_model']:
                    
                    with open("pipeline.pkl", "rb") as f:
                        
                        st.download_button(
                            label="Download Pipeline",
                            data=f,
                            file_name="pipeline.joblib",
                            mime="application/octet-stream"
                        )
        except KeyError as e:
            print(e)
            st.write("Please finish initializing the blocks' hyperparameters.")
            st.warning(str(e))

        

        
