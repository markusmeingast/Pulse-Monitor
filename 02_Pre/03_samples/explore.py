import pandas as pd

data = pd.read_excel('measurement_codes.xlsx',index_col=0,usecols=[0,2])

print(data['CODE'].value_counts())
