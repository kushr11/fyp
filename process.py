import pandas as pd
import ipdb
import numpy as np
file_path = 'result_60_21-23.csv'

df = pd.read_csv(file_path, header=None)
# Converting each column to a separate list
lists_from_csv = {f'list_{col}': df[col].tolist() for col in df.columns}

# ipdb.set_trace()
return_21_23=np.array(lists_from_csv["list_2"])
name_21_23=np.array(lists_from_csv["list_0"])
sorted_indices = np.argsort(return_21_23)[::-1]
return_21_23=return_21_23[sorted_indices]
indices_gt_zero = np.where(return_21_23 > 0)[0]
name_21_23=name_21_23[indices_gt_zero]
# name_21_23=name_21_23[return_21_23>0]
file_path = 'result_60_20-22.csv'

df = pd.read_csv(file_path, header=None)
# Converting each column to a separate list
lists_from_csv = {f'list_{col}': df[col].tolist() for col in df.columns}

# ipdb.set_trace()
return_=np.array(lists_from_csv["list_2"])
name_=np.array(lists_from_csv["list_0"])
sorted_indices = np.argsort(return_)[::-1]
return_20_22=return_[sorted_indices]
indices_gt_zero = np.where(return_ > 0)[0]
name_20_22=name_[indices_gt_zero]
# ipdb.set_trace()
common_strings = set(name_20_22) & set(name_21_23)
common_with_indices = [(s, return_20_22[np.where(name_20_22==s)], return_21_23[np.where(name_20_22==s)]) for s in common_strings]
print(common_with_indices)