import pandas as pd
from datetime import datetime, date
from itertools import chain

from django.conf import settings

def model_to_excel(model_data, file_path, file_name, sheet_name, index, header):

    if index:
        index = index
    else:
        index = False

    if header:
        header = header
    else:
        header = False

    item = model_data.values()

    keys = set(chain(*[dic.keys() for dic in item ]))
    final_dict = {key : [str(dic[key]) if isinstance(dic[key], date) else dic[key] for dic in item if key in dic] for key in keys }
    df = pd.DataFrame(final_dict)

    if file_name:
       pass
    else:
        file_name = '\/excel_file'+str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))+'.xlsx'


    if file_path:

        if file_path[-1] == '/' or '\/':
            file_path = file_path[:-1]
        elif file_path[-1] == '//' or '\\':
            file_path = file_path[:-2]
        elif file_path[-1] != '/' or '\/' or '//' or '//':
            file_path = file_path

        if sheet_name:
            df.to_excel(file_path+'\/'+file_name+'.xlsx', sheet_name= sheet_name, index=index, header=header)
        else:
            df.to_excel(file_path+'\/'+file_name+'.xlsx', index=index, header=header)
    else:

        if sheet_name:
            df.to_excel(file_path+'\/'+file_name+'.xlsx', sheet_name= sheet_name, index=index, header=header)
        else:
            df.to_excel(file_path+'\/'+file_name+'.xlsx', index=index, header=header)


    return True



def model_to_csv(model_data, file_path, file_name, sheet_name, index, header):

    item = model_data.values()

    if index:
        index = index
    else:
        index = False

    if header:
        header = header
    else:
        header = False

    keys = set(chain(*[dic.keys() for dic in item ]))
    final_dict = {key : [str(dic[key]) if isinstance(dic[key], date) else dic[key] for dic in item if key in dic] for key in keys }
    df = pd.DataFrame(final_dict)


    if file_name:
        pass
    else:
        file_name = '\/csv_file'+str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))+'.csv'
    
    if file_path:

        if file_path[-1] == '/' or '\/':
            file_path = file_path[:-1]
        elif file_path[-1] == '//' or '\\':
            file_path = file_path[:-2]
        elif file_path[-1] != '/' or '\/' or '//' or '//':
            file_path = file_path

        if sheet_name:
            df.to_csv(file_path+'\/'+file_name+'.xlsx', sheet_name= sheet_name, index=index, header=header)
        else:
            df.to_csv(file_path+'\/'+file_name+'.xlsx', index=index, header=header)
    else:

        if sheet_name:
            df.to_csv(str(settings.BASE_DIR)+'\/'+file_name+'.xlsx', sheet_name= sheet_name, index=index, header=header)
        else:
            df.to_csv(str(settings.BASE_DIR)+'\/'+file_name+'.xlsx', index=index, header=header)


    return True
