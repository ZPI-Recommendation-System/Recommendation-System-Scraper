import collections
from pprint import pprint

import pandas as pd
import pytest

from src.constants import TOKENS_CPU_COL_NAME, LAPTOP_CPU_NAME_COLUMN, MODEL_BENCHMARK_COLUMN, BRAND_BENCHMARK_COLUMN
from src.merge_benchmarks.mergeDataImpl import MergeDataComponentsImpl
from src.merge_benchmarks.mergeCPUData import MergeAllegroCPU


class TestMergeAllegroCPU:

    @pytest.fixture(scope='function')
    def laptops_data(self):
        data = {LAPTOP_CPU_NAME_COLUMN: ["['AMD 3020e']",
                                         "['AMD Ryzen 5 PRO 3500U']",
                                         "['AMD A4-9125']",
                                         "['Intel Celeron 4205U']",
                                         "['Intel Core i3-1005G1']",
                                         "['Intel Pentium Silver N5000']",
                                         "['Intel Xeon E3-1505M v5']"]}
        return pd.DataFrame(data)

    def test_create_laptops_tokens(self, laptops_data):
        expected = [['AMD', '3020', 'E'],
                    ['AMD', 'RYZEN', '5', 'PRO', '3500', 'U'],
                    ['AMD', 'A4', '9125'],
                    ['INTEL', 'CELERON', '4205', 'U'],
                    ['INTEL', 'CORE', 'I3', '1005', 'G', '1'],
                    ['INTEL', 'PENTIUM', 'SILVER', 'N', '5000'],
                    ['INTEL', 'XEON', 'E3', '1505', 'M', 'V5']]

        obj = MergeAllegroCPU(MergeDataComponentsImpl())
        obj.create_laptops_tokens(laptops_data=laptops_data,
                                  tokens_col=TOKENS_CPU_COL_NAME,
                                  component_col=LAPTOP_CPU_NAME_COLUMN)
        output = laptops_data[TOKENS_CPU_COL_NAME].values.tolist()
        zipped = zip(output, expected)
        assert all([collections.Counter(x[0]) == collections.Counter(x[1]) for x in zipped])

    @pytest.fixture(scope='function')
    def benchmark_data(self):
        data = {
            MODEL_BENCHMARK_COLUMN: ['Core i9-13900K',
                                     'Core i9-12900KS',
                                     'Ryzen 9 7950X',
                                     'Celeron N4020',
                                     'Xeon E3-1275 v3',
                                     'Xeon W3690',
                                     'Pentium Silver N5000'],

            BRAND_BENCHMARK_COLUMN: ["Intel",
                                     "Intel",
                                     "AMD",
                                     "Intel",
                                     "Intel",
                                     "Intel",
                                     "Intel"]
        }
        return pd.DataFrame(data)

    def test_create_benchmark_tokens(self, benchmark_data):
        expected = [['INTEL', 'CORE', 'I9', '13900', 'K'],
                    ['INTEL', 'CORE', 'I9', '12900', 'K', 'S'],
                    ['AMD', 'RYZEN', '9', '7950', 'X'],
                    ['INTEL', 'CELERON', 'N', '4020'],
                    ['INTEL', 'XEON', 'E3', '1275', 'V3'],
                    ['INTEL', 'XEON', 'W', '3690'],
                    ['INTEL', 'PENTIUM', 'SILVER', 'N', '5000']]

        obj = MergeAllegroCPU(MergeDataComponentsImpl())
        obj.create_benchmark_tokens(benchmark_data=benchmark_data,
                                    tokens_col=TOKENS_CPU_COL_NAME)
        output = benchmark_data[TOKENS_CPU_COL_NAME].values.tolist()
        zipped = zip(output, expected)
        assert all([collections.Counter(x[0]) == collections.Counter(x[1]) for x in zipped])
