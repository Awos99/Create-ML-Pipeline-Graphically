from barfi import Block

Database = Block(name='Database')
Database.add_output()

Simputer = Block(name='Simple Imputer')
Simputer.add_input()
Simputer.add_output()

Scaler = Block(name='Scaler')
Scaler.add_input()
Scaler.add_output()

Encoder = Block(name='Encoder')
Encoder.add_input()
Encoder.add_output()

ColumnTransformer = Block(name='Column Transformer')
ColumnTransformer.add_input()
ColumnTransformer.add_output()
ColumnTransformer.add_output()
#ColumnTransformer.add_option(name='Output 1', type='select', items=['categorical', 'numerical'])
#ColumnTransformer.add_option(name='Output 2', type='select', items=['categorical', 'numerical'])

Unify = Block(name='Unify')
Unify.add_input()
Unify.add_input()
Unify.add_output()

Model = Block(name='Model')
Model.add_input()


base_blocks = [Database, Simputer, Scaler, Encoder, ColumnTransformer, Unify, Model]
#base_blocks_category = {'process': [feed, result, mixer, splitter], 'options':[checkbox, input, integer, number, selecto, slider]}