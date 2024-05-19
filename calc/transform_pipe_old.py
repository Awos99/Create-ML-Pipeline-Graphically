from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

def identify_element(block_type):
    if block_type == 'Simple Imputer':
        return SimpleImputer(strategy='most_frequent')
    elif block_type == 'Scaler':
        return StandardScaler()
    elif block_type == 'Encoder':
        return OrdinalEncoder()
    elif block_type == 'Model':
        return DecisionTreeClassifier()
    elif block_type == 'Column Transformer':
        return 'Column Transformer'
    else:
        return None

def transform_pipe(json_data):
    # supports only 1 column transformer and 1 step per block
    steps = []
    transformer_open=False
    for key, block in json_data.items():
        block_type = block['type']
        if not transformer_open:
            if block_type != 'Column Transformer' and not None:
                element = identify_element(block_type)
                if element != None:
                    steps.append((block_type, element))
        
            elif block_type == 'Column Transformer':
                column1=block['block']._options['Output 1']['value']
                column2=block['block']._options['Output 2']['value']
                transformer_open=True
                transformer = []
        elif transformer_open:
            if block_type != 'Unify':
                if len(transformer) == 0:
                    transformer.append((block_type,identify_element(block_type),[column1]))
                else:
                    transformer.append((block_type,identify_element(block_type),[column2]))
            else:
                transformer_open=False
                steps.append(('Column Transformer', ColumnTransformer(transformers=transformer)))
    return steps