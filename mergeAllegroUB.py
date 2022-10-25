#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pprint import pprint
import regex as re
import pandas as pd

import constants

laptops_data = pd.read_csv(constants.LAPTOPS_FILE_PATH)
cpu_bechmark_data = pd.read_csv(constants.CPU_BENCHMARK_FILE_PATH)
gpu_benchmark_data = pd.read_csv(constants.GPU_BENCHMARK_FILE_PATH)
laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_')

all_tokens_gpu = set()


# In[2]:


#Tworzenie tokenów z pliku z danymi laptopów

laptops_data['Tokens'] = laptops_data['Model_karty_graficznej'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
laptops_data['Tokens'] = laptops_data['Tokens'].str.upper()
laptops_data['Tokens'] = laptops_data['Tokens'].str.replace(r"[-]", ' ', regex=True)
laptops_data['Tokens'] = [[item for sublist in [re.sub('TI$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in laptops_data['Tokens'].str.split()]
[x for x in laptops_data['Tokens']]


# In[3]:


#Tworzenie tokenów z pliku benchmarkowego

gpu_benchmark_data['Tokens'] = gpu_benchmark_data[['Brand','Model']].apply(lambda x: " ".join(x) if(x[0] not in x[1]) else x[1], axis=1)
gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].str.upper()
gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split() if re.findall(r'[-/]', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
#gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub('-Ti$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('-TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
#gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].apply(lambda x: [re.sub('[-/]', ' ', token.upper(), flags=re.IGNORECASE) for token in x])


[x for x in gpu_benchmark_data['Tokens']]
# gpu_benchmark_data[pd.DataFrame(gpu_benchmark_data['Tokens'].tolist()).isin(['-']).any(1).values]


# In[4]:


#Wypisanie tokenów

[all_tokens_gpu.add(x) for sublist in gpu_benchmark_data['Tokens'] for x in sublist]
[all_tokens_gpu.add(x) for sublist in laptops_data['Tokens'] for x in sublist]
all_tokens_gpu


# In[5]:


#Sprawdzenie czy gdzies zostaly jakiekolwiek niepożądane znaki

checks = [x if re.findall(r"[\[\]'!@#$\";()\s]", x) else None for sublist in gpu_benchmark_data['Tokens'] for x in sublist]
[x for x in checks if x is not None]


# In[6]:


#Sprawdzenie czy gdzies jest wiecej niz 1 wyraz w tokenie

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
