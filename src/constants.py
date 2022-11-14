from collections import namedtuple

# merge_benchmarks
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
BRAND_BENCHMARK_COLUMN = 'Brand'
MODEL_BENCHMARK_COLUMN = 'Model'

# allegro_api
CLIENT_ID = "57fa927c1f0b426b9419be5de3874bfa"  # wprowadź Client_ID aplikacji
CLIENT_SECRET = "tNlus0WGLDa52dLwSAnkmOgTCuVCp8Bz9Y9DdUjBUyuj5TJKhGqX92Hk3mIK4iyZ"  # wprowadź Client_Secret aplikacji
REDIRECT_URI = "http://localhost:8000"  # wprowadź redirect_uri
AUTH_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize"
TOKEN_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/token"
PRODUCTS_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/products"
CATEGORIES_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/categories/{categoryId}/product-parameters"
PARTICULAR_PRODUCT_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/products/{productId}"
LAPTOP_CATEGORY = "491"
OUTPUT_CSV = "laptops.csv"

# database
CPU_BENCHMARKS_CSV = "CPU_UserBenchmarks.csv"
GPU_BENCHMARKS_CSV = "GPU_UserBenchmarks.csv"
DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

# merge_offers
OUTPUT_CLEAR_LAPTOPS_CSV = "clear-laptops.csv"
OUTPUT_CLEAR_OFFERS_CSV = "clear-laptops.csv"

# pipeline
INPUT_OFFERS_CSV = "offers.csv"

# postfilter

# prefilter
