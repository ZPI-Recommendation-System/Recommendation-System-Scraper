import collections

import pandas as pd
import pytest

from src.constants import LAPTOP_GPU_NAME_COLUMN, MODEL_BENCHMARK_COLUMN, BRAND_BENCHMARK_COLUMN, TOKENS_GPU_COL_NAME
from src.merge_benchmarks.mergeDataImpl import MergeDataComponentsImpl
from src.merge_benchmarks.mergeGPUData import MergeAllegroGPU


class TestsMergeAllegroGPU:

    @pytest.fixture(scope='function')
    def laptops_data(self):
        data = {LAPTOP_GPU_NAME_COLUMN: ["['AMD Radeon 540']",
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
                                         "['RTX3050']"]}
        return pd.DataFrame(data)

    def test_create_laptops_tokens(self, laptops_data):
        expected = [['AMD', 'RADEON', '540', 'LAPTOP', 'MOBILE'],
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
                    ['RTX', '3050', 'LAPTOP', 'MOBILE']]

        obj = MergeAllegroGPU(MergeDataComponentsImpl())
        obj.create_laptops_tokens(laptops_data=laptops_data,
                                  tokens_col=TOKENS_GPU_COL_NAME,
                                  component_col=LAPTOP_GPU_NAME_COLUMN)
        output = laptops_data[TOKENS_GPU_COL_NAME].values.tolist()
        zipped = zip(output, expected)
        assert all([collections.Counter(x[0]) == collections.Counter(x[1]) for x in zipped])

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
                                     'Intel']
        }
        return pd.DataFrame(data)

    def test_create_benchmark_tokens(self, benchmark_data):
        expected = [['AMD', 'RADEON', '540'],
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
                    ['INTEL', 'HD', '5000', 'MOBILE', '1.0', '1.1', 'GHZ']]

        obj = MergeAllegroGPU(MergeDataComponentsImpl())
        obj.create_benchmark_tokens(benchmark_data=benchmark_data,
                                    tokens_col=TOKENS_GPU_COL_NAME)
        output = benchmark_data[TOKENS_GPU_COL_NAME].values.tolist()
        zipped = zip(output, expected)
        assert all([collections.Counter(x[0]) == collections.Counter(x[1]) for x in zipped])
