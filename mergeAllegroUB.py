#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pprint import pprint
import regex as re
import pandas as pd

laptops_data = pd.read_csv('clear-laptops.csv')
cpu_bechmark_data = pd.read_csv('CPU_UserBenchmarks.csv')
gpu_benchmark_data = pd.read_csv('GPU_UserBenchmarks.csv')
laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_')

all_tokens_gpu = dict()


# In[2]:


stop_words = ['NVIDIA','INTEL','AMD', 'APPLE']


# In[3]:


laptops_data['Tokens'] = laptops_data['Model_karty_graficznej'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
laptops_data['Tokens'] = laptops_data['Tokens'].str.upper()
laptops_data['Tokens'] = laptops_data['Tokens'].str.replace(r"[-]", ' ', regex=True)
laptops_data['Tokens'] = [[item for sublist in [re.sub('TI$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in laptops_data['Tokens'].str.split()]
[x for x in laptops_data['Tokens']]


# In[7]:


gpu_benchmark_data['Tokens'] = gpu_benchmark_data[['Brand','Model']].apply(lambda x: " ".join(x) if(x[0] not in x[1]) else x[1], axis =1)
gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].str.upper()
gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub('-Ti$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('-TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
[x for x in gpu_benchmark_data['Tokens']]


# In[5]:





# In[6]:


print(re.search('-TI$', '3090-Ti', re.IGNORECASE))

