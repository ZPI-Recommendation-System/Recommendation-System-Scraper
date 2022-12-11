import os
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()

# merge_benchmarks
CosineScore = namedtuple('CosineScore', ['Model', 'Cosine_Score', 'Benchmark'])
key_words = ['LAPTOP', 'MOBILE']
TOKENS_GPU_COL_NAME = 'TokensGPU'
VECTORS_GPU_COLUMN = 'VectorsGPU'
VECTORS_GPU_ONES_COLUMN = 'VectorsGPU_Ones_Count'
TOKENS_CPU_COL_NAME = 'TokensCPU'
VECTORS_CPU_COLUMN = 'VectorsCPU'
VECTORS_CPU_ONES_COLUMN = 'VectorsCPU_Ones_Count'
LAPTOP_GPU_NAME_COLUMN = 'Model_karty_graficznej'
LAPTOP_CPU_NAME_COLUMN = 'Model_procesora'
BRAND_BENCHMARK_COLUMN = 'Brand'
MODEL_BENCHMARK_COLUMN = 'Model'

# allegro_api
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
CODE_URL = "https://" + os.environ['DATA_API'] + "/auth/oauth/device"
TOKEN_URL = "https://" + os.environ['DATA_API'] + "/auth/oauth/token"
PRODUCTS_URL = "https://api." + os.environ['DATA_API'] + "/sale/products"
CATEGORIES_URL = "https://api." + os.environ['DATA_API'] + "/sale/categories/{categoryId}/product-parameters"
PARTICULAR_PRODUCT_URL = "https://api." + os.environ['DATA_API'] + "/sale/products/{productId}"
LAPTOP_CATEGORY = "491"
OUTPUT_CSV = "resources/laptops.csv"

# benchmarks
CPU_BENCHMARKS_URL = "https://www.userbenchmark.com/resources/download/csv/CPU_UserBenchmarks.csv"
GPU_BENCHMARKS_URL = "https://www.userbenchmark.com/resources/download/csv/GPU_UserBenchmarks.csv"
CPU_BENCHMARKS_CSV = "resources/CPU_UserBenchmarks.csv"
GPU_BENCHMARKS_CSV = "resources/GPU_UserBenchmarks.csv"

# database
DATABASE_URL = 'postgresql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + ':' + os.environ['DB_PORT'] + '/' + os.environ['DB_DB']

# merge_offers
OUTPUT_CLEAR_LAPTOPS_CSV = "resources/clear-laptops.csv"
OUTPUT_CLEAR_OFFERS_CSV = "resources/clear-offers.csv"

# pipeline
INPUT_OFFERS_CSV = "resources/offers.csv"

# postfilter

# prefilter
