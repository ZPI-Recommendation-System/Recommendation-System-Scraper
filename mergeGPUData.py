#!/usr/bin/env python
# coding: utf-8

from pprint import pprint
from collections import namedtuple
import regex as re
import pandas as pd
import numpy as np
from IPython.core.display_functions import display
from constants import CosineScore

# laptops_data = pd.read_csv(constants.LAPTOPS_FILE_PATH)
# cpu_bechmark_data = pd.read_csv(constants.CPU_BENCHMARK_FILE_PATH)
# gpu_benchmark_data = pd.read_csv(constants.GPU_BENCHMARK_FILE_PATH)
# laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_', regex=True)
key_words = ['LAPTOP', 'MOBILE']
TOKENS_GPU_COL_NAME = 'TokensGPU'

# Tworzenie tokenów z pliku z danymi laptopów
def create_laptop_gpu_tokens_column(laptops_data):
    token_column = []
    for model_token in laptops_data[TOKENS_GPU_COL_NAME].str.split():
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


def create_laptop_gpu_tokens(laptops_data):
    laptops_data[TOKENS_GPU_COL_NAME] = laptops_data['Model_karty_graficznej'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
    laptops_data[TOKENS_GPU_COL_NAME] = laptops_data[TOKENS_GPU_COL_NAME].str.upper()
    laptops_data[TOKENS_GPU_COL_NAME] = laptops_data[TOKENS_GPU_COL_NAME].str.replace(r"[-]", ' ', regex=True)
    laptops_data[TOKENS_GPU_COL_NAME] = create_laptop_gpu_tokens_column(laptops_data)
    # laptops_data[TOKENS_COL_NAME] = [[item for sublist in [re.sub('TI$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in laptops_data[TOKENS_COL_NAME].str.split()]
    # [x for x in laptops_data[TOKENS_COL_NAME]]


# Tworzenie tokenów z pliku benchmarkowego
def create_benchmark_gpu_tokens_column(gpu_benchmark_data):
    token_column = []
    for model_token in gpu_benchmark_data[TOKENS_GPU_COL_NAME].str.split():
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


def create_benchmark_gpu_tokens(gpu_benchmark_data):
    gpu_benchmark_data[TOKENS_GPU_COL_NAME] = gpu_benchmark_data[['Brand', 'Model']].apply(
        lambda x: " ".join(x) if (x[0] not in x[1]) else x[1], axis=1)
    gpu_benchmark_data[TOKENS_GPU_COL_NAME] = gpu_benchmark_data[TOKENS_GPU_COL_NAME].str.upper()
    gpu_benchmark_data[TOKENS_GPU_COL_NAME] = gpu_benchmark_data[TOKENS_GPU_COL_NAME].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
    gpu_benchmark_data[TOKENS_GPU_COL_NAME] = create_benchmark_gpu_tokens_column(gpu_benchmark_data)
    # gpu_benchmark_data[TOKENS_COL_NAME] = [[item for sublist in [re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split() if re.findall(r'[-/]', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data[TOKENS_COL_NAME].str.split()]
    # gpu_benchmark_data[TOKENS_COL_NAME] = [[item for sublist in [re.sub('-Ti$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('-TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data[TOKENS_COL_NAME].str.split()]
    # gpu_benchmark_data[TOKENS_COL_NAME] = gpu_benchmark_data[TOKENS_COL_NAME].apply(lambda x: [re.sub('[-/]', ' ', token.upper(), flags=re.IGNORECASE) for token in x])
    # gpu_benchmark_data[TOKENS_COL_NAME] = [[item for sublist in re.findall('(\d+|[A-Za-z])', token) if re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{2,50})$", token) else token] for token in gpu_benchmark_data[TOKENS_COL_NAME]]
    # [x for x in gpu_benchmark_data[TOKENS_COL_NAME]]
    # gpu_benchmark_data[pd.DataFrame(gpu_benchmark_data[TOKENS_COL_NAME].tolist()).isin(['-']).any(1).values]


def test_gpu_tokens(laptops_data, gpu_benchmark_data):
    # Sprawdzenie czy gdzies zostaly jakiekolwiek niepożądane znaki

    checks = [x if re.findall(r"[\[\]'!@#$\";()\s]", x) else None for sublist in gpu_benchmark_data[TOKENS_GPU_COL_NAME] for x in
              sublist]
    checklist = [x for x in checks if x is not None]
    if len(checklist) > 0:
        print("znaleziono blad")
        print(checklist)
    else:
        print("Nie ma żadnych niepożądanych znakow w tokenach")

    # Sprawdzenie czy gdzies jest wiecej niz 1 wyraz w tokenie

    checks = [x if len(x.split()) > 1 else None for sublist in gpu_benchmark_data[TOKENS_GPU_COL_NAME] for x in sublist]
    checklist = [x for x in checks if x is not None]
    if len(checklist) > 0:
        print("znaleziono blad")
        print(checklist)
    else:
        print("Nie ma zadnych wielowyrazowych tokenow")


def create_unique_gpu_tokens(laptops_data, gpu_benchmark_data):
    # Wypisanie tokenów
    all_tokens_gpu = set()
    [all_tokens_gpu.add(x) for sublist in gpu_benchmark_data[TOKENS_GPU_COL_NAME] for x in sublist]
    [all_tokens_gpu.add(x) for sublist in laptops_data[TOKENS_GPU_COL_NAME] for x in sublist]
    return all_tokens_gpu


def create_gpu_positions_dict(all_tokens_gpu):
    positions_dict = dict()
    positions_list = list(all_tokens_gpu)

    for i, token in enumerate(positions_list):
        positions_dict[token] = i
    return positions_dict


def create_gpu_vector(tokens, positions_dict):
    arr = np.zeros((len(positions_dict),), dtype=int)
    for token in tokens:
        if token in positions_dict:
            arr[positions_dict[token]] = 1
        else:
            raise Exception(f"Token {token} was not found in positions_dict")
    return arr


def create_gpu_vectors_df(df, positions_dict):
    df['Vectors'] = [create_gpu_vector(i, positions_dict) for i in df[TOKENS_GPU_COL_NAME]]
    df['Vectors_Ones_Count'] = [np.count_nonzero(x == 1) for x in df['Vectors']]


def create_vectors(laptops_data, gpu_benchmark_data, positions_dict):
    create_gpu_vectors_df(gpu_benchmark_data, positions_dict)
    create_gpu_vectors_df(laptops_data, positions_dict)


def cosine_gpu_score(laptop, benchmark):
    # if laptop.Model_karty_graficznej == "['NVIDIA Quadro K1000M']":
    #    print(laptop, benchmark)
    nominal = np.dot(laptop.Vectors, benchmark.Vectors)
    denominal = np.sqrt(laptop.Vectors_Ones_Count) * np.sqrt(benchmark.Vectors_Ones_Count)
    output = (nominal / denominal).item()
    return CosineScore(benchmark.Model, output, benchmark)


def create_gpu_assignment_dict(laptops_data, gpu_benchmark_data):
    assignments = dict()

    for laptop in laptops_data.itertuples():
        if laptop.Model_karty_graficznej in assignments:
            continue

        assigned_gpu_scores = list()
        duplicates_by_score = list()

        for benchmark in gpu_benchmark_data.itertuples():
            assigned_gpu_scores.append(cosine_gpu_score(laptop, benchmark))
        assigned_gpu_scores.sort(key=lambda x: x.Cosine_Score, reverse=True)

        # display(assigned_gpu_scores)

        max_benchmark = assigned_gpu_scores[0].Cosine_Score
        for score in assigned_gpu_scores:
            if not max_benchmark == score.Cosine_Score:
                break
            duplicates_by_score.append(score)

        min_benchmark = min(duplicates_by_score, key=lambda x: x.Benchmark.Benchmark)

        # print(laptop.Model_karty_graficznej)
        # print('assignments ******************************************************************')
        # display(assigned_gpu_scores[:10])
        # print('duplicates ******************************************************************')
        # display(duplicates_by_score)

        if min_benchmark.Cosine_Score != 0:
            assignments[laptop.Model_karty_graficznej] = min_benchmark
        else:
            assignments[laptop.Model_karty_graficznej] = None
    return assignments


def assign_gpus_from_benchmarks(laptops_data, gpu_benchmark_data):
    laptops_data = laptops_data.copy(deep=False)
    laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_', regex=True)
    create_laptop_gpu_tokens(laptops_data)
    create_benchmark_gpu_tokens(gpu_benchmark_data)
    test_gpu_tokens(laptops_data, gpu_benchmark_data)
    all_tokens_gpu = create_unique_gpu_tokens(laptops_data, gpu_benchmark_data)
    positions_dict = create_gpu_positions_dict(all_tokens_gpu)
    create_vectors(laptops_data, gpu_benchmark_data, positions_dict)
    assignments_dict = create_gpu_assignment_dict(laptops_data, gpu_benchmark_data)
    # pprint(assignments_dict)
    return assignments_dict

# assign_gpus_from_benchmarks(laptops_data, gpu_benchmark_data)
