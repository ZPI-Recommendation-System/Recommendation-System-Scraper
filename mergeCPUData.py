#!/usr/bin/env python
# coding: utf-8

from pprint import pprint
from collections import namedtuple
import regex as re
import pandas as pd
import numpy as np
from IPython.core.display_functions import display
import constants

CosineScore = namedtuple('CosineScore', ['Model', 'Cosine_Score', 'Benchmark'])
laptops_data = pd.read_csv(constants.LAPTOPS_FILE_PATH)
cpu_benchmark_data = pd.read_csv(constants.CPU_BENCHMARK_FILE_PATH)
laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_', regex=True)


def create_laptop_token_column(laptops_data):
    token_column = []
    for model_token in laptops_data['TokensCPU'].str.split():
        row = []
        for token in model_token:
            if re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{4,50})$", token):
                for elem in re.findall('(\d+|[A-Za-z])', token):
                    if elem not in row:
                        row.append(elem)
            else:
                row.append(token)
        token_column.append(row)
    return token_column


def create_laptop_cpu_tokens(laptops_data):
    laptops_data['TokensCPU'] = laptops_data['Model_procesora'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
    laptops_data['TokensCPU'] = laptops_data['TokensCPU'].str.upper()
    laptops_data['TokensCPU'] = laptops_data['TokensCPU'].str.replace(r"[-]", ' ', regex=True)
    laptops_data['TokensCPU'] = create_laptop_token_column(laptops_data)


def create_benchmark_cpu_tokens(cpu_benchmark_data):
    # Tworzenie tokenów z pliku benchmarkowego
    cpu_benchmark_data['TokensCPU'] = cpu_benchmark_data[['Brand', 'Model']].apply(
        lambda x: " ".join(x) if (x[0] not in x[1]) else x[1], axis=1)
    cpu_benchmark_data['TokensCPU'] = cpu_benchmark_data['TokensCPU'].str.upper()
    cpu_benchmark_data['TokensCPU'] = cpu_benchmark_data['TokensCPU'].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
    cpu_benchmark_data['TokensCPU'] = cpu_benchmark_data['TokensCPU'].str.replace(r"[-]", ' ', regex=True)
    cpu_benchmark_data['TokensCPU'] = create_laptop_token_column(cpu_benchmark_data)


def test_cpu_tokens(laptops_data, cpu_benchmark_data):
    # Sprawdzenie czy gdzies zostaly jakiekolwiek niepożądane znaki

    checks = [x if re.findall(r"[\[\]'!@#$\";()\s]", x) else None for sublist in cpu_benchmark_data['TokensCPU'] for x
              in
              sublist]
    checklist = [x for x in checks if x is not None]
    if len(checklist) > 0:
        print("znaleziono blad")
        print(checklist)
    else:
        print("Nie ma żadnych niepożądanych znakow w tokenach")

    # Sprawdzenie czy gdzies jest wiecej niz 1 wyraz w tokenie

    checks = [x if len(x.split()) > 1 else None for sublist in cpu_benchmark_data['TokensCPU'] for x in sublist]
    checklist = [x for x in checks if x is not None]
    if len(checklist) > 0:
        print("znaleziono blad")
        print(checklist)
    else:
        print("Nie ma zadnych wielowyrazowych tokenow")


def create_unique_cpu_tokens(laptops_data, cpu_benchmark_data):
    # Wypisanie tokenów
    all_tokens_cpu = set()
    [all_tokens_cpu.add(x) for sublist in cpu_benchmark_data['TokensCPU'] for x in sublist]
    [all_tokens_cpu.add(x) for sublist in laptops_data['TokensCPU'] for x in sublist]
    return all_tokens_cpu


def create_cpu_positions_dict(all_tokens_cpu):
    positions_dict = dict()
    positions_list = list(all_tokens_cpu)

    for i, token in enumerate(positions_list):
        positions_dict[token] = i
    return positions_dict


def create_cpu_vector(tokens, positions_dict):
    arr = np.zeros((len(positions_dict),), dtype=int)
    for token in tokens:
        if token in positions_dict:
            arr[positions_dict[token]] = 1
        else:
            raise Exception(f"Token {token} was not found in positions_dict")
    return arr


def create_cpu_vectors_df(df, positions_dict):
    df['VectorsCPU'] = [create_cpu_vector(i, positions_dict) for i in df['TokensCPU']]
    df['VectorsCPU_Ones_Count'] = [np.count_nonzero(x == 1) for x in df['VectorsCPU']]


def create_vectors(laptops_data, cpu_benchmark_data, positions_dict):
    create_cpu_vectors_df(cpu_benchmark_data, positions_dict)
    create_cpu_vectors_df(laptops_data, positions_dict)


def cosine_cpu_score(laptop, benchmark):
    nominal = np.dot(laptop.VectorsCPU, benchmark.VectorsCPU)
    denominal = np.sqrt(laptop.VectorsCPU_Ones_Count) * np.sqrt(benchmark.VectorsCPU_Ones_Count)
    output = (nominal / denominal).item()
    return CosineScore(benchmark.Model, output, benchmark.Benchmark)


def create_cpu_assignment_dict(laptops_data, gpu_benchmark_data):
    assignments = dict()
    for laptop in laptops_data.itertuples():
        if laptop.Model_procesora in assignments:
            continue

        assigned_cpu_scores = list()
        duplicates_by_score = list()

        for benchmark in gpu_benchmark_data.itertuples():
            assigned_cpu_scores.append(cosine_cpu_score(laptop, benchmark))
        assigned_cpu_scores.sort(key=lambda x: x.Cosine_Score, reverse=True)

        max_benchmark = assigned_cpu_scores[0].Cosine_Score
        for score in assigned_cpu_scores:
            if not max_benchmark == score.Cosine_Score:
                break
            duplicates_by_score.append(score)

        min_benchmark = min(duplicates_by_score, key=lambda x: x.Benchmark)

        # print(laptop.Model_procesora)
        # print('assignments ******************************************************************')
        # display(assigned_cpu_scores[:10])
        # print('duplicates ******************************************************************')
        # display(duplicates_by_score)

        if min_benchmark.Cosine_Score != 0:
            assignments[laptop.Model_procesora] = min_benchmark
        else:
            assignments[laptop.Model_procesora] = None
    return assignments


def assign_cpus_from_benchmarks(laptops_data, cpu_benchmark_data):
    create_laptop_cpu_tokens(laptops_data)
    create_benchmark_cpu_tokens(cpu_benchmark_data)
    test_cpu_tokens(laptops_data, cpu_benchmark_data)
    all_tokens_cpu = create_unique_cpu_tokens(laptops_data, cpu_benchmark_data)
    positions_dict = create_cpu_positions_dict(all_tokens_cpu)
    create_vectors(laptops_data, cpu_benchmark_data, positions_dict)
    assignments_dict = create_cpu_assignment_dict(laptops_data, cpu_benchmark_data)
    pprint(assignments_dict)


assign_cpus_from_benchmarks(laptops_data, cpu_benchmark_data)