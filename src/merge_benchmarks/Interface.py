from abc import ABC, abstractmethod


class MergeDataComponents(ABC):
    @abstractmethod
    def create_set_of_tokens(self, laptops_data, benchmark_data):
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
    def create_vectors(self, laptops_data, benchmark_data, positions_dict):
        pass

    @abstractmethod
    def cosine_score(self, laptop, benchmark, vector_col, vector_ones_col):
        pass

    @abstractmethod
    def create_assignment_dict(self, laptops_data, benchmark_data, column_to_assign):
        pass

    @abstractmethod
    def assign_from_benchmarks(self, laptops_data, benchmark_data, tokens_col, component_col, vector_col, vector_ones_col):
        pass


class MergeData(MergeDataComponents):
    @abstractmethod
    def create_laptop_token_column(self, laptops_data):
        pass

    @abstractmethod
    def create_laptops_tokens(self, laptops_data, tokens_col, component_col):
        pass

    @abstractmethod
    def create_benchmark_tokens(self, benchmark_data):
        pass

    @abstractmethod
    def test_tokens(self, laptops_data, benchmark_data):
        pass
