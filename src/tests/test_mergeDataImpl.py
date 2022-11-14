import re
from collections import namedtuple
from pprint import pprint

import numpy as np
import pandas as pd
import pytest

from src.constants import TOKENS_GPU_COL_NAME, VECTORS_GPU_COLUMN, VECTORS_GPU_ONES_COLUMN, LAPTOP_GPU_NAME_COLUMN, \
    MODEL_BENCHMARK_COLUMN, BRAND_BENCHMARK_COLUMN
from src.merge_benchmarks.mergeDataImpl import MergeDataComponentsImpl
from src.merge_benchmarks.mergeGPUData import MergeAllegroGPU

TestTuple = namedtuple("TestTuple", ['Model', VECTORS_GPU_COLUMN, VECTORS_GPU_ONES_COLUMN, 'Benchmark'])


class TestsMergeDataComponents:

    @pytest.fixture(scope='function')
    def laptops_data(self):
        data = {
                LAPTOP_GPU_NAME_COLUMN: ["['AMD Radeon 540']",
                                         "['AMD Radeon Graphics']",
                                         "['AMD Radeon Pro 5300M']",
                                         "['AMD Radeon Pro 560X']",
                                         "['Intel HD Graphics 4000']",
                                         "['NVIDIA GeForce 940MX']",
                                         "['NVIDIA GeForce GTX 1060 Max-Q']",
                                         "['NVIDIA GeForce MX330']",
                                         "['NVIDIA GeForce RTX 3050Ti']",
                                         "['NVIDIA MX450 2GB']",
                                         "['NVIDIA Quadro K1000M']",
                                         "['RTX3050']"],
                TOKENS_GPU_COL_NAME:
                    [['AMD', 'RADEON', '540', 'LAPTOP', 'MOBILE'],
                     ['AMD', 'RADEON', 'GRAPHICS', 'LAPTOP', 'MOBILE'],
                     ['AMD', 'RADEON', 'PRO', '5300', 'M', 'LAPTOP', 'MOBILE'],
                     ['AMD', 'RADEON', 'PRO', '560', 'X', 'LAPTOP', 'MOBILE'],
                     ['INTEL', 'HD', 'GRAPHICS', '4000', 'LAPTOP', 'MOBILE'],
                     ['NVIDIA', 'GEFORCE', '940', 'MX', 'LAPTOP', 'MOBILE'],
                     ['NVIDIA', 'GEFORCE', 'GTX', '1060', 'MAX', 'Q', 'LAPTOP', 'MOBILE'],
                     ['NVIDIA', 'GEFORCE', 'MX', '330', 'LAPTOP', 'MOBILE'],
                     ['NVIDIA', 'GEFORCE', 'RTX', '3050', 'TI', 'LAPTOP', 'MOBILE'],
                     ['NVIDIA', 'MX', '450', '2GB', 'LAPTOP', 'MOBILE'],
                     ['NVIDIA', 'QUADRO', 'K', '1000', 'M', 'LAPTOP', 'MOBILE'],
                     ['RTX', '3050', 'LAPTOP', 'MOBILE']]}
        return pd.DataFrame(data)

    @pytest.fixture(scope='function')
    def benchmark_data(self):
        data = {
                MODEL_BENCHMARK_COLUMN: ['Radeon 540',
                                         'Radeon R3 Graphics',
                                         'Radeon Pro 5300M',
                                         'HD 7990 (CrossFire Disabled)',
                                         'UHD Graphics 770',
                                         'Sapphire R9 380 4GB NITRO',
                                         'Sapphire R9 380 2GB Dual-X OC',
                                         'PowerColor R9 380 4GB PCS+',
                                         'GTX 750-Ti',
                                         'Quadro K2200',
                                         'Quadro K5000M',
                                         'GTX 675MX',
                                         'MX150-2',
                                         'EAH6770',
                                         'GTX 745 (OEM)',
                                         'RTX 2080S (Super Mobile Max-Q)',
                                         'RX 6600-XT',
                                         'Iris Pro HD 6100 (Mobile)',
                                         'GeForce 9800M-GS',
                                         'HD 5000 (Mobile 1.0/1.1 GHz)'],
                BRAND_BENCHMARK_COLUMN: ['AMD',
                                         'AMD',
                                         'AMD',
                                         'AMD',
                                         'Intel',
                                         'Sapphire',
                                         'Sapphire',
                                         'PowerColor',
                                         'Nvidia',
                                         'Nvidia',
                                         'Nvidia',
                                         'Nvidia',
                                         'Nvidia',
                                         'Asus',
                                         'Nvidia',
                                         'Nvidia',
                                         'AMD',
                                         'Intel',
                                         'Nvidia',
                                         'Intel'],
                TOKENS_GPU_COL_NAME:
                    [['AMD', 'RADEON', '540'],
                     ['AMD', 'RADEON', 'R3', 'GRAPHICS'],
                     ['AMD', 'RADEON', 'PRO', '5300', 'M'],
                     ['AMD', 'HD', '7990', 'CROSSFIRE', 'DISABLED'],
                     ['INTEL', 'UHD', 'GRAPHICS', '770'],
                     ['SAPPHIRE', 'R9', '380', '4GB', 'NITRO'],
                     ['SAPPHIRE', 'R9', '380', '2GB', 'DUAL', 'X', 'OC'],
                     ['POWERCOLOR', 'R9', '380', '4GB', 'PCS+'],
                     ['NVIDIA', 'GTX', '750', 'TI'],
                     ['NVIDIA', 'QUADRO', 'K', '2200'],
                     ['NVIDIA', 'QUADRO', 'K', '5000', 'M'],
                     ['NVIDIA', 'GTX', '675', 'MX'],
                     ['NVIDIA', 'MX', '150', '2'],
                     ['ASUS', 'EAH', '6770'],
                     ['NVIDIA', 'GTX', '745', 'OEM'],
                     ['NVIDIA', 'RTX', '2080', 'S', 'SUPER', 'MOBILE', 'MAX', 'Q'],
                     ['AMD', 'RX', '6600', 'XT'],
                     ['INTEL', 'IRIS', 'PRO', 'HD', '6100', 'MOBILE'],
                     ['NVIDIA', 'GEFORCE', '9800', 'M', 'GS'],
                     ['INTEL', 'HD', '5000', 'MOBILE', '1.0', '1.1', 'GHZ']],
                'Benchmark': [9.84,
                              1.58,
                              35.9,
                              36.0,
                              7.88,
                              34.4,
                              34.4,
                              34.4,
                              18.2,
                              17.3,
                              16.4,
                              16.0,
                              10.9,
                              10.1,
                              9.97,
                              94.2,
                              93.7,
                              6.3,
                              3.3,
                              3.07]}
        return pd.DataFrame(data)

    @pytest.fixture(scope='function')
    def all_tokens(self, laptops_data, benchmark_data):
        obj = MergeDataComponentsImpl()
        return obj.create_set_of_tokens(laptops_data=laptops_data,
                                        benchmark_data=benchmark_data,
                                        tokens_col=TOKENS_GPU_COL_NAME)

    def test_create_set_of_tokens(self, all_tokens):
        assert [x is not None if re.findall(r"[\[\]'!@#$\";()\s]", x) else None for x in all_tokens]
        assert [x is not None if len(x.split()) > 1 else None for x in all_tokens]
        assert len(set(all_tokens)) == len(all_tokens)

    @pytest.fixture(scope='function')
    def positions_dict(self, all_tokens):
        obj = MergeDataComponentsImpl()
        return obj.create_positions_dict(all_tokens)

    def test_create_positions_dict(self, positions_dict, all_tokens):
        assert len(positions_dict) == len(all_tokens)

    @pytest.fixture(scope='function')
    def tokens(self):
        return ['AMD', 'RADEON', '540']

    @pytest.fixture(scope='function')
    def vector(self, tokens, positions_dict):
        obj = MergeDataComponentsImpl()
        vector = obj.create_vector(tokens, positions_dict)
        return vector

    def test_create_vector(self, tokens, vector, positions_dict):
        positions = [positions_dict[token] for token in tokens]
        assert all([vector[i] == 1 for i in positions])

    def test_create_vectors_df(self, laptops_data, positions_dict):
        obj = MergeDataComponentsImpl()
        vector_array = [obj.create_vector(i, positions_dict) for i in laptops_data[TOKENS_GPU_COL_NAME]]
        zero_counter = [np.count_nonzero(x == 1) for x in vector_array]
        obj.create_vectors_df(laptops_data, positions_dict,
                              vector_col=VECTORS_GPU_COLUMN,
                              vector_ones_col=VECTORS_GPU_ONES_COLUMN,
                              tokens_col=TOKENS_GPU_COL_NAME)
        assert all([np.array_equal(i, j) for i, j in zip(vector_array, laptops_data[VECTORS_GPU_COLUMN].tolist())])
        assert all([i == j for i, j in zip(zero_counter, laptops_data[VECTORS_GPU_ONES_COLUMN].tolist())])

    @pytest.fixture(scope='function')
    def vector_ones(self, vector):
        return np.count_nonzero(vector == 1)

    @pytest.fixture(scope='function')
    def laptop(self, vector, vector_ones):
        data = TestTuple(None, vector, vector_ones, None)
        return data

    @pytest.fixture(scope='function')
    def benchmark(self, vector, vector_ones):
        data = TestTuple(None, vector, vector_ones, None)
        return data

    def test_cosine_score(self, laptop, benchmark):
        obj = MergeDataComponentsImpl()
        assert np.isclose(obj.cosine_score(laptop=laptop, benchmark=benchmark, vector_col=VECTORS_GPU_COLUMN,
                                           vector_ones_col=VECTORS_GPU_ONES_COLUMN).Cosine_Score, 1)


    @pytest.fixture(scope='function')
    def dataset(self, laptops_data, benchmark_data, positions_dict):
        obj = MergeDataComponentsImpl()
        obj.create_vectors(laptops_data, benchmark_data, positions_dict, vector_col=VECTORS_GPU_COLUMN, vector_ones_col=VECTORS_GPU_ONES_COLUMN, tokens_col=TOKENS_GPU_COL_NAME)
        return laptops_data, benchmark_data

    def test_create_assignment_dict(self, dataset):
        laptops_data = dataset[0]
        benchmark_data = dataset[1]
        obj = MergeDataComponentsImpl()
        assignment_dict = obj.create_assignment_dict(laptops_data, benchmark_data, LAPTOP_GPU_NAME_COLUMN, TOKENS_GPU_COL_NAME, VECTORS_GPU_COLUMN, VECTORS_GPU_ONES_COLUMN)
        # pprint(assignment_dict)
        assert assignment_dict["['AMD Radeon Pro 5300M']"].Model == 'Radeon Pro 5300M'
