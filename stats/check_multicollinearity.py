import pandas as pd
import numpy as np

# Function to calculate VIF
def calculate_vif(data):
    vif_df = pd.DataFrame(columns = ['Var', 'Vif'])
    x_var_names = data.columns
    for i in range(0, x_var_names.shape[0]):
        y = data[x_var_names[i]]
        x = data[x_var_names.drop([x_var_names[i]])]
        r_squared = sm.OLS(y,x).fit().rsquared
        vif = round(1/(1-r_squared),2)
        vif_df.loc[i] = [x_var_names[i], vif]
    return vif_df.sort_values(by = 'Vif', axis = 0, ascending=False, inplace=False)

df = pd.read_csv('sample.csv')
df = df.drop(['Salary'],axis=1)
print(calculate_vif(df))

# now, let us drop one of the dummy variables to solve the multicollinearity issue:
df = df.drop(df.columns[[0]], axis=1)

print(calculate_vif(df)) # Wow! VIF has decreased. We solved the problem of multicollinearity. Now, the dataset is ready for building the model.


