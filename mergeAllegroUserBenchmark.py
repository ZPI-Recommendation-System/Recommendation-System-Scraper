
import regex as re
import pandas as pd

import constants

# rejected version
def mergeAllegroUserBenchmark():
    laptops_data = pd.read_csv(constants.LAPTOPS_FILE_PATH)
    cpu_bechmark_data = pd.read_csv(constants.CPU_BENCHMARK_FILE_PATH)
    gpu_benchmark_data = pd.read_csv(constants.GPU_BENCHMARK_FILE_PATH)

    # print(laptops_data.to_string(max_rows=10))
    laptops_data.columns = laptops_data.columns.str.replace(r'\s+', '_')
    # print(cpu_bechmark_data)
    # print(gpu_benchmark_data.to_string(max_rows=10))

    cache = dict()
    assigned_graphics_cards = []

    for row in laptops_data.itertuples():
        gpu_from_laptops = row.Model_karty_graficznej  # printparam = re.sub(r"[\[\]'!@#$\";]", '', str(product_parameter['valuesLabels']))
        gpu_from_laptops = re.sub(r"[\[\]'!@#$\";]", '', gpu_from_laptops)

        splitted_gpu_name = gpu_from_laptops.split(' ')
        splitted_gpu_name.reverse()

        last_filtered_data_by_token = None
        new_filtered_data_by_token = None
        was_assigned = False

        if gpu_from_laptops not in cache:
            for token in splitted_gpu_name:
                if last_filtered_data_by_token is None:
                    last_filtered_data_by_token = gpu_benchmark_data[gpu_benchmark_data['Model'].str.match(token)]
                    new_filtered_data_by_token = last_filtered_data_by_token
                else:
                    new_filtered_data_by_token = last_filtered_data_by_token[
                        last_filtered_data_by_token['Model'].str.match(token)]
                if len(new_filtered_data_by_token) == 0:
                    break
            if len(last_filtered_data_by_token) != 0:
                item = last_filtered_data_by_token.iloc[0]['Model']
                assigned_graphics_cards.append(item)
                cache[gpu_from_laptops] = item
                last_filtered_data_by_token = None
                was_assigned = True
                # break
        else:
            assigned_graphics_cards.append(cache[gpu_from_laptops])
            was_assigned = True

        if not was_assigned:
            assigned_graphics_cards.append('')
    laptops_data['assigned_gpu'] = assigned_graphics_cards
    laptops_data.to_csv('merged.csv')


if __name__ == "__main__":
    mergeAllegroUserBenchmark()
