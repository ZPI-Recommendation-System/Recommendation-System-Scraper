from collections import namedtuple

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
CLIENT_ID = "473bd2ed049f4d4d815fe720b98ddc2d"
CLIENT_SECRET = "IOogn5eBhxmSSu8pnKDnwhXIkKIq8iBKngqkoOciMMgYTHs3qWRQi4vBir168ysd"
CODE_URL = "https://allegro.pl/auth/oauth/device"
TOKEN_URL = "https://allegro.pl/auth/oauth/token"
PRODUCTS_URL = "https://api.allegro.pl/sale/products"
CATEGORIES_URL = "https://api.allegro.pl/sale/categories/{categoryId}/product-parameters"
PARTICULAR_PRODUCT_URL = "https://api.allegro.pl/sale/products/{productId}"
LAPTOP_CATEGORY = "491"
OUTPUT_CSV = "resources/laptops.csv"

# benchmarks
CPU_BENCHMARKS_URL = "https://www.userbenchmark.com/resources/download/csv/CPU_UserBenchmarks.csv"
GPU_BENCHMARKS_URL = "https://www.userbenchmark.com/resources/download/csv/GPU_UserBenchmarks.csv"
CPU_BENCHMARKS_CSV = "resources/CPU_UserBenchmarks.csv"
GPU_BENCHMARKS_CSV = "resources/GPU_UserBenchmarks.csv"

# database
DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

# merge_offers
OUTPUT_CLEAR_LAPTOPS_CSV = "resources/clear-laptops.csv"
OUTPUT_CLEAR_OFFERS_CSV = "resources/clear-offers.csv"

# pipeline
INPUT_OFFERS_CSV = "resources/offers.csv"

# postfilter

# prefilter
