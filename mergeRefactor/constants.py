from collections import namedtuple

CosineScore = namedtuple('CosineScore', ['Model', 'Cosine_Score', 'Benchmark'])
LAPTOPS_FILE_PATH = r'C:\Users\Jakub\Desktop\ZPI\Scapper-System\clear-laptops.csv'
CPU_BENCHMARK_FILE_PATH = r'C:\Users\Jakub\Desktop\ZPI\Scapper-System\CPU_UserBenchmarks.csv'
GPU_BENCHMARK_FILE_PATH = r'C:\Users\Jakub\Desktop\ZPI\Scapper-System\GPU_UserBenchmarks.csv'
key_words = ['LAPTOP', 'MOBILE']
TOKENS_GPU_COL_NAME = 'TokensGPU'
VECTORS_GPU_COLUMN = 'VectorsGPU'
VECTORS_GPU_ONES_COLUMN = 'VectorsGPU_Ones_Count'
TOKENS_CPU_COL_NAME = 'TokensCPU'
VECTORS_CPU_COLUMN = 'VectorsCPU'
VECTORS_CPU_ONES_COLUMN = 'VectorsCPU_Ones_Count'
LAPTOP_GPU_NAME_COLUMN = 'Model_karty_graficznej'
LAPTOP_CPU_NAME_COLUMN = 'Model_procesora'
