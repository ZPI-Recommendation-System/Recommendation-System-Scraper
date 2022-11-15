import regex as re


from src.constants import TOKENS_GPU_COL_NAME, key_words, LAPTOP_GPU_NAME_COLUMN, VECTORS_GPU_COLUMN, \
    VECTORS_GPU_ONES_COLUMN
from src.merge_benchmarks.Interface import MergeData
from src.merge_benchmarks.mergeDataImpl import MergeDataComponentsImpl


# Tworzenie tokenów z pliku z danymi laptopów
class MergeAllegroGPU(MergeData):
    def create_laptop_token_column(self, laptops_data):
        token_column = []
        for model_token in laptops_data[TOKENS_GPU_COL_NAME].str.split():
            sublist = list()
            for token in model_token:
                if re.findall('TI$', token, re.IGNORECASE):
                    sublist.append(re.sub('TI$', ' TI', token.upper(), flags=re.IGNORECASE).split())
                else:
                    sublist.append([token.upper()])
            row_before_clean = []
            for flat in sublist:
                for item in flat:
                    # display(item)
                    row_before_clean.append(item)
            # print(row)

            row = []
            for token in row_before_clean:
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

    def create_laptops_tokens(self, laptops_data, tokens_col, component_col):
        laptops_data[tokens_col] = laptops_data[component_col].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
        laptops_data[tokens_col] = laptops_data[tokens_col].str.upper()
        laptops_data[tokens_col] = laptops_data[tokens_col].str.replace(r"[-]", ' ', regex=True)
        laptops_data[tokens_col] = self.create_laptop_token_column(laptops_data)

    # Tworzenie tokenów z pliku benchmarkowego
    def __create_benchmark_tokens(self, benchmark_data, tokens_col):
        token_column = []
        for model_token in benchmark_data[tokens_col].str.split():
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

    def create_benchmark_tokens(self, benchmark_data, tokens_col):
        benchmark_data[tokens_col] = benchmark_data[['Brand', 'Model']].apply(lambda x: " ".join(x) if (x[0] not in x[1]) else x[1], axis=1)
        benchmark_data[tokens_col] = benchmark_data[tokens_col].str.upper()
        benchmark_data[tokens_col] = benchmark_data[tokens_col].str.replace(r"[\[\]'!@#$\";()]", '', regex=True)
        benchmark_data[tokens_col] = self.__create_benchmark_tokens(benchmark_data, tokens_col)
        # gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub(r'[-/]', ' ', token.upper(), flags=re.IGNORECASE).split() if re.findall(r'[-/]', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
        # gpu_benchmark_data['Tokens'] = [[item for sublist in [re.sub('-Ti$', ' TI', token.upper(), flags=re.IGNORECASE).split() if re.findall('-TI$', token, re.IGNORECASE) else [token.upper()] for token in model_token] for item in sublist] for model_token in gpu_benchmark_data['Tokens'].str.split()]
        # gpu_benchmark_data['Tokens'] = gpu_benchmark_data['Tokens'].apply(lambda x: [re.sub('[-/]', ' ', token.upper(), flags=re.IGNORECASE) for token in x])
        # gpu_benchmark_data['Tokens'] = [[item for sublist in re.findall('(\d+|[A-Za-z])', token) if re.match("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{2,50})$", token) else token] for token in gpu_benchmark_data['Tokens']]
        # [x for x in gpu_benchmark_data['Tokens']]
        # gpu_benchmark_data[pd.DataFrame(gpu_benchmark_data['Tokens'].tolist()).isin(['-']).any(1).values]

    def test_tokens(self, laptops_data, benchmark_data):
        # Sprawdzenie czy gdzies zostaly jakiekolwiek niepożądane znaki

        checks = [x if re.findall(r"[\[\]'!@#$\";()\s]", x) else None for sublist in benchmark_data[TOKENS_GPU_COL_NAME] for x in sublist]
        checklist = [x for x in checks if x is not None]
        if len(checklist) > 0:
            print("znaleziono blad")
            print(checklist)
        else:
            print("Nie ma żadnych niepożądanych znakow w tokenach")

        # Sprawdzenie czy gdzies jest wiecej niz 1 wyraz w tokenie

        checks = [x if len(x.split()) > 1 else None for sublist in benchmark_data[TOKENS_GPU_COL_NAME] for x in sublist]
        checklist = [x for x in checks if x is not None]
        if len(checklist) > 0:
            print("znaleziono blad")
            print(checklist)
        else:
            print("Nie ma zadnych wielowyrazowych tokenow")

    @staticmethod
    def print_assigns(laptops_data, gpu_benchmark_data):
        laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_', regex=True)
        obj = MergeAllegroGPU(MergeDataComponentsImpl())
        result = obj.assign_from_benchmarks(laptops_data=laptops_data,
                                   benchmark_data=gpu_benchmark_data,
                                   tokens_col=TOKENS_GPU_COL_NAME,
                                   component_col=LAPTOP_GPU_NAME_COLUMN,
                                   vector_col=VECTORS_GPU_COLUMN,
                                   vector_ones_col=VECTORS_GPU_ONES_COLUMN)
        laptops_data.columns = laptops_data.columns.str.replace('_', ' ')
        return result
