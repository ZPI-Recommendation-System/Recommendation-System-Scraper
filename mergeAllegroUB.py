#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pprint import pprint
import regex as re
import pandas as pd
import numpy as np
from IPython.core.display_functions import display

import constants

laptops_data = pd.read_csv(constants.LAPTOPS_FILE_PATH)
cpu_bechmark_data = pd.read_csv(constants.CPU_BENCHMARK_FILE_PATH)
gpu_benchmark_data = pd.read_csv(constants.GPU_BENCHMARK_FILE_PATH)
laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_')

all_tokens_gpu = set()

# In[2]:


# Tworzenie tokenów z pliku z danymi laptopów
key_words = ['LAPTOP', 'MOBILE']


def create_laptop_token_column(laptops_data):
    token_column = []
    for model_token in laptops_data['Tokens'].str.split():
        sublist = list()  # [re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split() if re.findall(r'[-/]', token, re.IGNORECASE) else [token.upper()]]
        for token in model_token:
            if re.findall('TI$', token, re.IGNORECASE):
                sublist.append(re.sub('TI$', ' TI', token.upper(), flags=re.IGNORECASE).split())
            else:
                sublist.append([token.upper()])
        row_precleaned = []
        for flat in sublist:
            for item in flat:
                # display(item)
                row_precleaned.append(item)
        # print(row)

        row = []
        for token in row_precleaned:
            if re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{4,50})$", token):
                for elem in re.findall('(\d+|[A-Za-z]+)', token):
                    if elem not in row:
                        row.append(elem)
            else:
                row.append(token)

        for keyword in key_words:
            if keyword not in row:
                row.append(keyword)
        token_column.append(row)
    return token_column


laptops_data['Tokens'] = laptops_data['Model_karty_graficznej'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
laptops_data['Tokens'] = laptops_data['Tokens'].str.upper()
laptops_data['Tokens'] = laptops_data['Tokens'].str.replace(r"[-]", ' ', regex=True)
laptops_data['Tokens'] = create_laptop_token_column(laptops_data)
# laptops_data['Tokens'] = [[item for sublist in [re.sub('TI$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in laptops_data['Tokens'].str.split()]
[x for x in laptops_data['Tokens']]


# In[3]:


# Tworzenie tokenów z pliku benchmarkowego
def create_benchmark_token_column(gpu_benchmark_data):
    token_column = []
    for model_token in gpu_benchmark_data['Tokens'].str.split():
        sublist = list()  # [re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split() if re.findall(r'[-/]', token, re.IGNORECASE) else [token.upper()]]
        for token in model_token:
            if re.findall(r'[-/]', token, re.IGNORECASE):
                sublist.append(re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split())
            else:
                sublist.append([token.upper()])
        row_precleaned = []
        for flat in sublist:
            for item in flat:
                # display(item)
                row_precleaned.append(item)
        # print(row)

        row = []
        for token in row_precleaned:
            if re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{4,50})$", token):
                for elem in re.findall('(\d+|[A-Za-z]+)', token):
                    if elem not in row:
                        row.append(elem)
            else:
                row.append(token)
        token_column.append(row)
    return token_column


gpu_benchmark_data['Tokens'] = gpu_benchmark_data[['Brand', 'Model']].apply(
    lambda x: " ".join(x) if (x[0] not in x[1]) else x[1], axis=1)
gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].str.upper()
gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
gpu_benchmark_data['Tokens'] = create_benchmark_token_column(gpu_benchmark_data)

# gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split() if re.findall(r'[-/]', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
# gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub('-Ti$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('-TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
# gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].apply(lambda x: [re.sub('[-/]', ' ', token.upper(), flags=re.IGNORECASE) for token in x])
# gpu_benchmark_data['Tokens'] = [[item for sublist in re.findall('(\d+|[A-Za-z])', token) if re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{2,50})$", token) else token] for token in gpu_benchmark_data['Tokens']]

[x for x in gpu_benchmark_data['Tokens']]
# gpu_benchmark_data[pd.DataFrame(gpu_benchmark_data['Tokens'].tolist()).isin(['-']).any(1).values]


# In[4]:


# Wypisanie tokenów

[all_tokens_gpu.add(x) for sublist in gpu_benchmark_data['Tokens'] for x in sublist]
[all_tokens_gpu.add(x) for sublist in laptops_data['Tokens'] for x in sublist]
all_tokens_gpu

# In[5]:


# Sprawdzenie czy gdzies zostaly jakiekolwiek niepożądane znaki

checks = [x if re.findall(r"[\[\]'!@#$\";()\s]", x) else None for sublist in gpu_benchmark_data['Tokens'] for x in
          sublist]
[x for x in checks if x is not None]

# In[6]:


# Sprawdzenie czy gdzies jest wiecej niz 1 wyraz w tokenie

checks = [x if len(x.split()) > 1 else None for sublist in gpu_benchmark_data['Tokens'] for x in sublist]
[x for x in checks if x is not None]

# In[7]:


positions_dict = dict()
positions_list = list(all_tokens_gpu)

for i, token in enumerate(positions_list):
    positions_dict[token] = i

positions_dict

# In[8]:


# Tworzenie wektorów z tokenów

np.zeros((len(positions_list),), dtype=int)

# In[9]:


gpu_benchmark_data

# In[10]:


laptops_data


# In[11]:


def create_vector(tokens, positions_dict):
    arr = np.zeros((len(positions_list),), dtype=int)
    for token in tokens:
        if token in positions_dict:
            arr[positions_dict[token]] = 1
        else:
            raise Exception(f"Token {token} was not found in positions_dict")
    return arr


def create_vectors_df(df):
    df['Vectors'] = [create_vector(i, positions_dict) for i in df['Tokens']]
    df['Vectors_Ones_Count'] = [np.count_nonzero(x == 1) for x in df['Vectors']]


# In[12]:


create_vectors_df(gpu_benchmark_data)
create_vectors_df(laptops_data)

# In[13]:


laptops_data[['Model_karty_graficznej', 'Tokens', 'Vectors', 'Vectors_Ones_Count']]

# In[14]:


gpu_benchmark_data[['Model', 'Tokens', 'Vectors', 'Vectors_Ones_Count']]

# In[15]:


gpu_benchmark_data[gpu_benchmark_data['Model'] == 'Quadro K1000M']

# In[16]:


import time

CosineScore = namedtuple('CosineScore', ['Model', 'Cosine_Score', 'Benchmark'])


def cosine_score(laptop, benchmark):
    # if laptop.Model_karty_graficznej == "['NVIDIA Quadro K1000M']":
    #    print(laptop, benchmark)
    nominal = np.dot(laptop.Vectors, benchmark.Vectors)
    denominal = np.sqrt(laptop.Vectors_Ones_Count) * np.sqrt(benchmark.Vectors_Ones_Count)
    output = (nominal / denominal).item()
    return CosineScore(benchmark.Model, output, benchmark.Benchmark)


def create_assignment_dict(laptops_data, gpu_benchmark_data):
    assignments = dict()

    for laptop in laptops_data.itertuples():
        # print(laptop.Model_karty_graficznej)

        if laptop.Model_karty_graficznej in assignments:
            continue

        assigned_gpu_scores = list()
        duplicates_by_score = list()

        for benchmark in gpu_benchmark_data.itertuples():
            assigned_gpu_scores.append(cosine_score(laptop, benchmark))
        assigned_gpu_scores.sort(key=lambda x: x.Cosine_Score, reverse=True)

        # display(assigned_gpu_scores)

        max_benchmark = assigned_gpu_scores[0].Cosine_Score
        for score in assigned_gpu_scores:
            if not max_benchmark == score.Cosine_Score:
                break
            duplicates_by_score.append(score)

        min_benchmark = min(duplicates_by_score, key=lambda x: x.Benchmark)

        print(laptop.Model_karty_graficznej)
        print('assignments ******************************************************************')
        display(assigned_gpu_scores[:10])
        print('duplicates ******************************************************************')
        display(duplicates_by_score)

        if min_benchmark.Cosine_Score != 0:
            assignments[laptop.Model_karty_graficznej] = min_benchmark
        else:
            assignments[laptop.Model_karty_graficznej] = None
    return assignments


assignments_dict = create_assignment_dict(laptops_data, gpu_benchmark_data)

# In[17]:


for laptop in laptops_data.itertuples():
    print(laptop.Model_karty_graficznej)

# In[18]:


assignments_dict["['NVIDIA GeForce MX330']"]

# In[19]:


s = 'MX330'
res = re.findall('(\d+|[A-Za-z])', s)
print(res)

# In[20]:


s = 'RTX3050'
tokens = ['NVIDIA', 'GEFORCE', 'MX330']
for token in tokens:
    print(re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{2,50})$", token))
    print(re.findall('(\d+|[A-Za-z]+)', s))
# re.match("^[A-Za-z0-9_-]*$", s)


# In[ ]:

