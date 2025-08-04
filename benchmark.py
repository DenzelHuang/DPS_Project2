import pandas as pd
import time
import threading
import multiprocessing as mp
import operator
import os
import re

# Prompt user for filter operation
valid_ops = {
    'lt': operator.lt, '<': operator.lt,
    'le': operator.le, '<=': operator.le,
    'gt': operator.gt, '>': operator.gt,
    'ge': operator.ge, '>=': operator.ge,
}
print("Choose a filter operation:")
print("  lt or <   : less than")
print("  le or <=  : less than or equal to")
print("  gt or >   : greater than")
print("  ge or >=  : greater than or equal to")
user_op = None
while user_op not in valid_ops:
    user_op = input("Enter operation (lt, le, gt, ge or symbol): ").strip()
op_func = valid_ops[user_op]

# Prompt user for numeric threshold
while True:
    try:
        threshold = int(input("Enter integer threshold value: ").strip())
        break
    except ValueError:
        print("Invalid integer, please try again.")

# Configuration
test_fracs = [0.25, 0.50, 0.75, 1.00]
sort_ops = {'asc': False, 'desc': True}

# Environment variables
data_file = os.getenv('DATA_FILE', 'data.csv')
output_dir = os.getenv('OUTPUT_DIR', 'output')

# Load data
df = pd.read_csv(data_file, usecols=['trip_duration'])
data_full = df['trip_duration'].dropna().astype(int).tolist()

# Prepare full filtered dataset
filtered_full = [x for x in data_full if op_func(x, threshold)]
# Prepare full sorted datasets (asc and desc)
sorted_full_asc = sorted(data_full)
sorted_full_desc = sorted(data_full, reverse=True)

# Ensure output dir exists
os.makedirs(output_dir, exist_ok=True)

# Determine next index for output files
existing = os.listdir(output_dir)
nums = [int(re.match(r'output(\d+)\.csv', f).group(1))
        for f in existing if re.match(r'output(\d+)\.csv', f)]
next_idx = max(nums) + 1 if nums else 0

# Paths for outputs
results_path = os.path.join(output_dir, f"timings{next_idx}.csv")
filter_path = os.path.join(output_dir, f"filtered{next_idx}.csv")
sort_path = os.path.join(output_dir, f"sorted{next_idx}.csv")

# Helper functions
def seq_filter(data, op, thresh):
    return [x for x in data if op(x, thresh)]

def seq_sort(data, rev=False):
    return sorted(data, reverse=rev)

def thread_task(func, args, out, idx):
    out[idx] = func(*args)

def mp_task(func, args):
    return func(*args)

# Benchmarking function
def benchmark():
    results = []
    for frac in test_fracs:
        sample = pd.Series(data_full).sample(frac=frac, random_state=42).tolist()
        for method in ['sequential', 'threading', 'multiprocessing']:
            # Filter benchmark
            start = time.perf_counter()
            if method == 'sequential':
                seq_filter(sample, op_func, threshold)
            elif method == 'threading':
                out = [None]
                t = threading.Thread(target=thread_task,
                                        args=(seq_filter, (sample, op_func, threshold), out, 0))
                t.start(); t.join()
            else:
                with mp.Pool(1) as pool:
                    pool.apply(mp_task, args=(seq_filter, (sample, op_func, threshold)))
            elapsed = time.perf_counter() - start
            results.append({
                'fraction': frac,
                'method': method,
                'operation': f'filter_{user_op}',
                'time_s': elapsed
            })
            # Sort benchmark
            for name, rev in sort_ops.items():
                start = time.perf_counter()
                if method == 'sequential':
                    seq_sort(sample, rev)
                elif method == 'threading':
                    out = [None]
                    t = threading.Thread(target=thread_task,
                                            args=(seq_sort, (sample, rev), out, 0))
                    t.start(); t.join()
                else:
                    with mp.Pool(1) as pool:
                        pool.apply(mp_task, args=(seq_sort, (sample, rev)))
                elapsed = time.perf_counter() - start
                results.append({
                    'fraction': frac,
                    'method': method,
                    'operation': f'sort_{name}',
                    'time_s': elapsed
                })
    return pd.DataFrame(results)

if __name__ == '__main__':
    total_start = time.perf_counter()
    # Run benchmark and save timing results
    df_res = benchmark()
    df_res.to_csv(results_path, index=False)
    print(f"Timings written to {results_path}")
    # Print sum of all benchmark times
    total_bench_time = df_res['time_s'].sum()
    print(f"Sum of all filter+sort timings: {total_bench_time:.4f} seconds")
    # Save filtered and sorted data separately
    pd.DataFrame({'trip_duration': filtered_full}).to_csv(filter_path, index=False)
    print(f"Filtered data written to {filter_path}")
    # Save sorted data (both ascending and descending)
    pd.DataFrame({
        'sorted_asc': sorted_full_asc,
        'sorted_desc': sorted_full_desc
    }).to_csv(sort_path, index=False)
    print(f"Sorted data (asc & desc) written to {sort_path}")