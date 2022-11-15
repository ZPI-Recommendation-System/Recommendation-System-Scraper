import pandas as pd
import urllib.request

from src.constants import CPU_BENCHMARKS_CSV, GPU_BENCHMARKS_CSV, GPU_BENCHMARKS_URL, CPU_BENCHMARKS_URL


def get():
    urllib.request.urlretrieve(CPU_BENCHMARKS_URL, CPU_BENCHMARKS_CSV)
    cpu_benchmarks = pd.read_csv(CPU_BENCHMARKS_CSV)
    urllib.request.urlretrieve(GPU_BENCHMARKS_URL, GPU_BENCHMARKS_CSV)
    gpu_benchmarks = pd.read_csv(GPU_BENCHMARKS_CSV)
    return cpu_benchmarks, gpu_benchmarks
