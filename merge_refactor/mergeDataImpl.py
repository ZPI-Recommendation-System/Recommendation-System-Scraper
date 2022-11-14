from pprint import pprint
import numpy as np
from Interface import MergeDataComponents
from constants import CosineScore


class MergeDataComponentsImpl(MergeDataComponents):
    def create_set_of_tokens(self, laptops_data, benchmark_data, tokens_col):
        # Wypisanie tokenów
        all_tokens_cpu = set()
        [all_tokens_cpu.add(x) for sublist in benchmark_data[tokens_col] for x in sublist]
        [all_tokens_cpu.add(x) for sublist in laptops_data[tokens_col] for x in sublist]
        return all_tokens_cpu

    def create_positions_dict(self, all_tokens):
        positions_dict = dict()
        positions_list = list(all_tokens)

        for i, token in enumerate(positions_list):
            positions_dict[token] = i
        return positions_dict

    def create_vector(self, tokens, positions_dict):
        arr = np.zeros((len(positions_dict),), dtype=int)
        for token in tokens:
            if token in positions_dict:
                arr[positions_dict[token]] = 1
            else:
                raise Exception(f"Token {token} was not found in positions_dict")
        return arr
    #(self, laptops_data, cpu_benchmark_data, tokens_col, component_col, vector_col, vector_ones_col)
    def create_vectors_df(self, df, positions_dict, vector_col, vector_ones_col, tokens_col):
        df[vector_col] = [self.create_vector(i, positions_dict) for i in df[tokens_col]]
        df[vector_ones_col] = [np.count_nonzero(x == 1) for x in df[vector_col]]

    def create_vectors(self, laptops_data, benchmark_data, positions_dict, vector_col, vector_ones_col, tokens_col):
        self.create_vectors_df(benchmark_data, positions_dict, vector_col, vector_ones_col, tokens_col)
        self.create_vectors_df(laptops_data, positions_dict, vector_col, vector_ones_col, tokens_col)

    def cosine_score(self, laptop, benchmark, vector_col, vector_ones_col):
        nominal = np.dot(getattr(laptop, vector_col), getattr(benchmark, vector_col))
        denominal = np.sqrt(getattr(laptop, vector_ones_col)) * np.sqrt(getattr(benchmark, vector_ones_col))
        cos_sim = (nominal / denominal).item()
        return CosineScore(benchmark.Model, cos_sim, benchmark.Benchmark)

    def create_assignment_dict(self, laptops_data, benchmark_data, component_col, token_col, vector_col, vector_ones_col):
        assignments = dict()
        for laptop in laptops_data.itertuples():
            if getattr(laptop, component_col) in assignments:
                continue

            assigned_scores = list()
            duplicates_by_score = list()

            for benchmark in benchmark_data.itertuples():
                assigned_scores.append(self.cosine_score(laptop, benchmark, vector_col, vector_ones_col))
            assigned_scores.sort(key=lambda x: x.Cosine_Score, reverse=True)

            max_benchmark = assigned_scores[0].Cosine_Score
            for score in assigned_scores:
                if not max_benchmark == score.Cosine_Score:
                    break
                duplicates_by_score.append(score)

            min_benchmark = min(duplicates_by_score, key=lambda x: x.Benchmark)

            # print(laptop.Model_procesora)
            # print('assignments ******************************************************************')
            # display(assigned_scores[:10])
            # print('duplicates ******************************************************************')
            # display(duplicates_by_score)

            if min_benchmark.Cosine_Score != 0:
                assignments[getattr(laptop, component_col)] = min_benchmark
            else:
                assignments[getattr(laptop, component_col)] = None
        return assignments
