from abc import ABC, abstractmethod
from pprint import pprint


class MergeDataComponents(ABC):
    @abstractmethod
    def create_set_of_tokens(self, laptops_data, benchmark_data, tokens_col):
        pass

    @abstractmethod
    def create_positions_dict(self, all_tokens):
        pass

    @abstractmethod
    def create_vector(self, tokens, positions_dict):
        pass

    @abstractmethod
    def create_vectors_df(self, df, positions_dict):
        pass

    @abstractmethod
    def create_vectors(self, laptops_data, benchmark_data, positions_dict, vector_col, vector_ones_col, tokens_col):
        pass

    @abstractmethod
    def cosine_score(self, laptop, benchmark, vector_col, vector_ones_col):
        pass

    @abstractmethod
    def create_assignment_dict(self, laptops_data, benchmark_data, component_col, token_col, vector_col, vector_ones_col):
        pass


class MergeData:
    def __init__(self, merge_data_impl: MergeDataComponents):
        self.merge_data_impl = merge_data_impl

    @abstractmethod
    def create_laptop_token_column(self, laptops_data):
        pass

    @abstractmethod
    def create_laptops_tokens(self, laptops_data, tokens_col, component_col):
        pass

    @abstractmethod
    def create_benchmark_tokens(self, benchmark_data, tokens_col):
        pass

    @abstractmethod
    def test_tokens(self, laptops_data, benchmark_data):
        pass

    def assign_from_benchmarks(self, laptops_data, benchmark_data, tokens_col, component_col, vector_col, vector_ones_col):
        self.create_laptops_tokens(laptops_data, tokens_col, component_col)
        self.create_benchmark_tokens(benchmark_data, tokens_col)
        self.test_tokens(laptops_data, benchmark_data)
        all_tokens_cpu = self.merge_data_impl.create_set_of_tokens(laptops_data, benchmark_data, tokens_col)
        positions_dict = self.merge_data_impl.create_positions_dict(all_tokens_cpu)
        self.merge_data_impl.create_vectors(laptops_data, benchmark_data, positions_dict, vector_col, vector_ones_col, tokens_col)
        assignments_dict = self.merge_data_impl.create_assignment_dict(laptops_data, benchmark_data, component_col, tokens_col, vector_col, vector_ones_col)
        # pprint(assignments_dict)
        return assignments_dict