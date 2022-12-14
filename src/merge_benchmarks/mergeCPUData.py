import regex as re

from src.constants import TOKENS_CPU_COL_NAME, LAPTOP_CPU_NAME_COLUMN, VECTORS_CPU_COLUMN, VECTORS_CPU_ONES_COLUMN, \
    MODEL_BENCHMARK_COLUMN, BRAND_BENCHMARK_COLUMN
from src.merge_benchmarks.Interface import MergeData
from src.merge_benchmarks.mergeDataImpl import MergeDataComponentsImpl


class MergeAllegroCPU(MergeData):
    def create_laptop_token_column(self, laptops_data):
        token_column = []
        for model_token in laptops_data[TOKENS_CPU_COL_NAME].str.split():
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

    def create_laptops_tokens(self, laptops_data, tokens_col, component_col):
        laptops_data[tokens_col] = laptops_data[component_col].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
        laptops_data[tokens_col] = laptops_data[tokens_col].str.upper()
        laptops_data[tokens_col] = laptops_data[tokens_col].str.replace(r"[-]", ' ', regex=True)
        laptops_data[tokens_col] = self.create_laptop_token_column(laptops_data)

    def create_benchmark_tokens(self, benchmark_data, tokens_col):
        # Tworzenie tokenów z pliku benchmarkowego
        benchmark_data[tokens_col] = benchmark_data[[BRAND_BENCHMARK_COLUMN, MODEL_BENCHMARK_COLUMN]].apply(lambda x: " ".join(x) if (x[0] not in x[1]) else x[1], axis=1)
        benchmark_data[tokens_col] = benchmark_data[tokens_col].str.upper()
        benchmark_data[tokens_col] = benchmark_data[tokens_col].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
        benchmark_data[tokens_col] = benchmark_data[tokens_col].str.replace(r"[-]", ' ', regex=True)
        benchmark_data[tokens_col] = self.create_laptop_token_column(benchmark_data)


    @staticmethod
    def print_assigns(laptops_data, cpu_benchmark_data):
        laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_', regex=True)
        obj = MergeAllegroCPU(MergeDataComponentsImpl())
        result = obj.assign_from_benchmarks(laptops_data=laptops_data,
                                   benchmark_data=cpu_benchmark_data,
                                   tokens_col=TOKENS_CPU_COL_NAME,
                                   component_col=LAPTOP_CPU_NAME_COLUMN,
                                   vector_col=VECTORS_CPU_COLUMN,
                                   vector_ones_col=VECTORS_CPU_ONES_COLUMN)
        laptops_data.columns = laptops_data.columns.str.replace('_', ' ')
        return result

