import math
import json
import camelot
import io
import numpy
import re
import pandas
from transformer.llama_helper import call_model


def check_extension(filename : str) -> str:
    return filename.rsplit('.', 1)[1].lower()


def process_content(content: str):
    try:
        #strip to turn into a proper JSON string
        res = call_model(content)
        res.strip()
        match = re.search(r'\{.*\}', res, re.DOTALL).group()
        final = json.loads(match)
        for i in range(3): #convert percentage to int
            final['most_transacted_category'][i]['percentage'] = float(str(final['most_transacted_category'][i]['percentage']).strip('%'))
        print(final)
        return final
    except Exception as e:
        raise Exception(f"Error at process_content, {e}")

def extract_table(pdf_file : io.BytesIO) -> str:
    try:
        res_stream, res_lattice = "", ""
        table_stream = camelot.read_pdf(pdf_file, pages='all', flavor='stream')
        table_lattice = camelot.read_pdf(pdf_file, pages='all', flavor='lattice')
        stream_container, lattice_container = [], []
        for table in table_stream:
            # print(table.parsing_report)
            stream_container.append(float(table.parsing_report['accuracy']))
            res_stream += f"{table.df.to_string(index=False, header=False)}\n"
        for table in table_lattice:
            lattice_container.append(float(table.parsing_report['accuracy']))
            res_lattice += f"{table.df.to_string(index=False, header=False)}\n"
        choose_res_stream = not lattice_container or numpy.mean(stream_container) > numpy.mean(lattice_container)
        date_transaction_data = helper_extract_date_transaction(table_stream) if choose_res_stream else  helper_extract_date_transaction(table_lattice)
        income_data = income_analysis(date_transaction_data)
        return (res_stream, date_transaction_data, income_data) if choose_res_stream else (res_lattice, date_transaction_data, income_data)
    except Exception as e:
        raise Exception(f"Error at extract_table, {e}")

def helper_extract_date_transaction(table_arr):
    res_total = [] #{date : string, balance : string }
    for table in table_arr:
        res_total += get_date_trans(table.df)
    return res_total

def income_analysis(transact_arr : list):
    #generate an array of income : {'date', 'balance}
    income_arr = []
    tempSum, tempCount = 0, 0
    for i in range(1, len(transact_arr)):
        diff = transact_arr[i]['balance'] - transact_arr[i-1]['balance']
        if diff > 0:
            tempCount += 1
            tempSum += diff
            income_arr.append({'date' : transact_arr[i]['date'], 'balance' : diff})
    #!income_arr still have type {'date', 'balance'}
    return {'mean' : round(tempSum / tempCount, 3), 'income_data' : income_arr}

def get_date_trans(df : pandas.DataFrame):
    res = []
    column_names = df.columns.values
    first_col, last_col = 0, len(column_names) - 1
    date_pattern = r'(\d{2})[- ]?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[- ]?(\d{2,4})?'
    balance_pattern = r'\$?\d{1,10}(?:,\d{3})*(\.\d+)?'
    prev_first_match = None
    prev_last_match = None
    for index, row in df.iterrows():
        first, last = row[first_col], row[last_col]
        #first will try to match the date, last will try to match the balance
        first_match = re.match(date_pattern, first, re.IGNORECASE)
        last_match = re.match(balance_pattern, last, re.IGNORECASE)
        if first_match and last_match:
            process_and_add(res, first_match, last_match)
        elif first_match:
            if prev_last_match:
                process_and_add(res, first_match, prev_last_match)
                prev_last_match = None
            else: #probably the balance falls out to next row
                prev_first_match = first_match
        elif last_match:
            if prev_first_match:
                process_and_add(res, prev_first_match, last_match)
                prev_first_match = None
            else: #probably the date falls out to next row
                prev_last_match = last_match
    return res

def extract_subset_transaction_data(arr : list):
    subset_size = math.ceil(len(arr) * (2/3))
    step = len(arr) / subset_size
    return [arr[round(i * step)] for i in range(subset_size)]

def process_and_add(res_arr : list, date_match, balance_match):
    #TODO: bhring the date into a format like this 04-Nov
    temp_d, temp_b = date_match.group().strip(), balance_match.group().strip(' $')
    res_b = re.sub(r',', '', temp_b)
    res_d = re.sub(r"(\d{1,2})[ -]([A-Za-z]{3}).*", r"\1-\2", temp_d)
    res_arr.append({"date" : res_d, "balance" : float(res_b)})
    return True
