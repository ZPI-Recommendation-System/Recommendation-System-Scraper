from pprint import pprint
from collections import namedtuple
import regex as re
import pandas as pd
import numpy as np
from constants import *
from mergeCPUData import MergeAllegroCPU
from mergeGPUData import MergeAllegroGPU

laptops_data = pd.read_csv(LAPTOPS_FILE_PATH)
gpu_benchmark_data = pd.read_csv(GPU_BENCHMARK_FILE_PATH)
cpu_benchmark_data = pd.read_csv(CPU_BENCHMARK_FILE_PATH)
laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_', regex=True)

MergeAllegroCPU.print_assigns(laptops_data, cpu_benchmark_data)
print("\n")
MergeAllegroGPU.print_assigns(laptops_data, gpu_benchmark_data)
