from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
import streamlit as st


def identify_element(block_type):
    if block_type == 'Simple Imputer':
        return SimpleImputer(strategy='most_frequent')
    elif block_type == 'Scaler':
        return StandardScaler()
    elif block_type == 'Encoder':
        return OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    elif block_type == 'Model':
        return DecisionTreeRegressor()
    elif block_type == 'Column Transformer':
        return 'Column Transformer'
    elif block_type == 'Unify':
        return 'Unify'
    else:
        return None

def find_kids(block_name, barfi_result):
    item = barfi_result[block_name]
    kids=[]
    for output in item['interfaces']:
        if item['interfaces'][output]['type'] == 'output':
            kids.append(list(item['interfaces'][output]['to'].keys())[0])
    if kids:
        return kids
    return None

def single_pipe_constructor(barfi_result, X, block_name):
    steps = []
    element = identify_element(barfi_result[block_name]['type'])
    if element != 'Column Transformer' and element != 'Unify' and element is not None:
        steps.append((block_name, element))
    #steps.append((block_name, identify_element(barfi_result[block_name]['type'])))
    kid = find_kids(block_name, barfi_result)
    if (kid is None):
        return steps
    elif barfi_result[kid[0]]['type'] == 'Column Transformer' or barfi_result[kid[0]]['type'] == 'Unify':
        steps.append(kid[0])
        return steps
    else:
        next_step = single_pipe_constructor(barfi_result, X, kid[0])
        steps=steps + next_step
        return steps
    
def transform_to_columns(column, X, block=None, column_output=None):
    if column == 'categorical':
        return list(X.select_dtypes(include='object').columns)
    elif column == 'numerical':
        return list(X.select_dtypes(include=['int64', 'float64']).columns)
    elif column == 'list':
        return st.session_state[block][column_output]


def pipe_recursive(barfi, block, X, steps=[]):
    # Check if block has output, (block is also last step)
    if find_kids(block, barfi) is None:
        return steps
    else:
        # Check Whether It is Column Transformer
        if barfi[block]['type'] == 'Column Transformer':
            print('Column Transformer:', block)
            steps= steps[:-1]
            steps_transformer = []
            kids_transformer = find_kids(block, barfi)
            for line_transf in kids_transformer:
                #print('Kid transformer:', line_transf)
                kid_pipe = pipe_recursive(barfi, line_transf, X)
                #print('Kid pipe:',line_transf, kid_pipe)
                for interface in barfi[line_transf]['interfaces']:
                        if barfi[line_transf]['interfaces'][interface]['type'] == 'intput':
                            input_option = interface
                #print('Block:', block)
                #print('Barfi:', barfi[line_transf]['interfaces'][input_option]['from'])
                #print('Barfi:', barfi[line_transf])
                option = barfi[line_transf]['interfaces'][input_option]['from'][block]
                    
                    # to change with._options
                if option == 'Output 1':
                    columns=st.session_state[block]['cat_num_select_output1']
                    path_transf = transform_to_columns(columns, X, block, 'columns_output1')
                
                if option == 'Output 2':
                    columns=st.session_state[block]['cat_num_select_output2']
                    path_transf = transform_to_columns(columns, X, block, 'columns_output2')
                #columns = barfi[block]['block']._options[option]['value']
                print('Kid pipe:', kid_pipe)
                print('Kid pipe:', type(kid_pipe[-1]))
                if type(kid_pipe[-1]) == tuple:
                    kid_pipe = kid_pipe + ['Unify']
                steps_transformer = steps_transformer + [(line_transf, Pipeline(kid_pipe[:-1]), path_transf)]
                
                relative_unify = kid_pipe[-1]
            if st.session_state[block]['remainder']:
                passthrough = 'passthrough'
            else:
                passthrough = 'drop'
            transformer = ColumnTransformer(steps_transformer, remainder=passthrough)
            steps.append((block,transformer))
            steps = pipe_recursive(barfi, relative_unify, X, steps)
        else:
            next_block = find_kids(block, barfi)[0]
            if barfi[next_block]['type'] == 'Unify' and barfi[block]['type'] == 'Unify':
                return steps
            if barfi[block]['type'] != 'Unify' and barfi[next_block]['type'] == 'Unify':
                steps = steps + single_pipe_constructor(barfi, X, block)
                return steps
            else:
                steps = steps + single_pipe_constructor(barfi, X, block)
                next_block = steps[-1]
                if type(next_block) == tuple:
                    return steps

            
            steps = pipe_recursive(barfi, next_block, X, steps)

    return steps

def create_pipe(barfi, X):
    for key, item in barfi.items():
        if item['type'] == 'Database':
            kids = find_kids(key, barfi)
            pipe = Pipeline(pipe_recursive(barfi, kids[0], X))
            return pipe