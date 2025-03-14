import os
import csv
import sys
import uuid
import time
import argparse
import subprocess

TOKENS = 256

online_threads = None


def parse_args():
    parser = argparse.ArgumentParser(description="Run offline benchmark.")
    parser.add_argument("-m", "--model",
                        type=str, required=True,
                        help="name of the model")
    parser.add_argument("-b", "--batch_size",
                        type=int, required=True,
                        help="batch size to feed the model with")
    parser.add_argument("-p", "--prompt_size",
                        type=int, required=True,
                        help="prompt size to feed the model with")
    parser.add_argument("-r", "--threads_range",
                        type=str, required=True,
                        help="range of threads to use, e.g. '0-63,128-191', threads will be divided between processes "
                             "- hint: 'lscpu | grep NUMA'")
    parser.add_argument("--kv_cache",
                        type=int, default=65536,
                        help="kv cache size")
    parser.add_argument("-n", "--num_processes",
                        type=int, default=1,
                        help="number of processes to spawn")
    parser.add_argument("-t", "--num_threads",
                        type=int, default=1,
                        help="number of threads to use per process")
    parser.add_argument("--mp",
                        type=str, default="local",
                        help="memory placement policy, 'local','interleave' or 'none'")
    return parser.parse_args()


def parse_threads_range(threads_range: str) -> list[int]:
    threads_range = [s.split("-") for s in threads_range.split(",")]
    if not all([len(s) == 2 for s in threads_range]):
        print("Format of --threads_range argument must be '{idx}-{idx},{idx}-{idx},...', "
              "e.g. '88-88' to use just thread idx 88")
        sys.exit(1)
    designated_threads = []
    for s in threads_range:
        s_0, s_1 = int(s[0]), int(s[1])
        if s_1 < s_0:
            print(f"Range {s_0}-{s_1} is not valid, second value has to be equal to or greater than the first value")
            sys.exit(1)
        designated_threads += [i for i in range(s_0, s_1 + 1)]
    return designated_threads


def gen_threads_config(num_threads, process_id):
    threads_to_use = [str(t) for t in online_threads[num_threads * process_id:num_threads * (process_id + 1)]]
    assert len(threads_to_use) == num_threads
    return ",".join(threads_to_use)


def summarize_results(logs_dir, args, start, finish):
    ttfts = []
    tg_lats = []
    for n in range(args.num_processes):
        results = open(f"{logs_dir}/log_{n}", "r").readlines()[-9].split("|")
        prompt_size = int(results[1])
        assert prompt_size == args.prompt_size
        tokens_generated = int(results[2])
        assert tokens_generated == TOKENS
        batch_size = int(results[3])
        assert batch_size == args.batch_size
        ttfts.append(float(results[5]))
        tg_lats.append(float(results[7]))

    pp_throughput = sum([args.batch_size * args.prompt_size / ttft for ttft in ttfts])
    avg_pp_latency = sum(ttfts) / len(ttfts)
    tg_throughput = sum([args.batch_size * TOKENS / lat for lat in tg_lats])
    tg_per_token_lats = [lat / TOKENS for lat in tg_lats]
    avg_tg_latency = sum(tg_per_token_lats) / len(tg_per_token_lats)
    avg_total_speed = args.num_processes * args.batch_size * (args.prompt_size + TOKENS) / max([ttft + tg_lat for ttft, tg_lat in zip(ttfts, tg_lats)])

    results_filename = f"{args.model.split('/')[-1]}@PP{str(args.prompt_size)}@TG{str(TOKENS)}.csv"
    if os.path.exists(results_filename):
        first_write = False
    else:
        first_write = True
    with open(results_filename, "a") as f:
        writer = csv.writer(f)
        if first_write:
            writer.writerow(
                ["n_proc", "n_threads", "batch_size", "prompt_size", "output_tokens", "pp_throughput_tps",
                 "pp_avg_latency_sec", "tg_throughput_tps", "tg_avg_latency_sec", "pp+tg_throughput_tps", "concurrency", "start", "finish"])
        writer.writerow(
            [args.num_processes, args.num_threads, args.batch_size, args.prompt_size, TOKENS, f"{pp_throughput:.3f}",
             f"{avg_pp_latency:.3f}", f"{tg_throughput:.3f}", f"{avg_tg_latency:.3f}", f"{avg_total_speed:.3f}", args.batch_size * args.num_processes, f"{start:.3f}", f"{finish:.3f}"])

    print(f"Result saved in {results_filename}")


def main():
    global online_threads

    args = parse_args()

    designated_threads = parse_threads_range(args.threads_range)
    numa_config = subprocess.run(["numactl", "--show"], capture_output=True, text=True, check=True)
    online_threads = [int(t) for t in numa_config.stdout.split("physcpubind: ")[1].split(" \ncpubind:")[0].split()
                      if int(t) in designated_threads]
    if len(online_threads) < args.num_processes * args.num_threads:
        print(f"Requested config requires {args.num_processes * args.num_threads} threads, while only {len(online_threads)} threads are both online and designated")
        sys.exit(1)

    logs_dir = os.path.join("/tmp", str(uuid.uuid4()))
    os.mkdir(logs_dir)
    current_subprocesses = list()
    if args.mp == "local":
        mem_place = "--localalloc"
    elif args.mp == "interleave":
        mem_place = "--interleave=all"
    else:
        mem_place = "none"

    for n in range(args.num_processes):
        logfile = f"{logs_dir}/log_{n}"
        if os.path.exists("/llm/batched-bench"):
            # command-line for v1
            if mem_place == "none":
                cmd = ["numactl", f"--physcpubind={gen_threads_config(args.num_threads, n)}",
                       "/llm/batched-bench", args.model, str(args.kv_cache), "2048", "512", "0", "0", "0", str(args.prompt_size), str(TOKENS),
                       str(args.batch_size), str(args.num_threads)]
            else:
                 cmd = ["numactl", f"--physcpubind={gen_threads_config(args.num_threads, n)}", str(mem_place),
                       "/llm/batched-bench", args.model, str(args.kv_cache), "2048", "512", "0", "0", "0", str(args.prompt_size), str(TOKENS),
                       str(args.batch_size), str(args.num_threads)]
        elif os.path.exists("/llm/llama-batched-bench"):
            # command-line for v2
            if mem_place == "none":
                cmd = ["numactl", f"--physcpubind={gen_threads_config(args.num_threads, n)}",
                       "/llm/llama-batched-bench", "-m", args.model, "-c", str(args.kv_cache), "-b", "2048", "-ub", "512", "-npp", str(args.prompt_size), "-ntg", str(TOKENS),
                       "-npl", str(args.batch_size), "-t", str(args.num_threads), "-tb", str(args.num_threads), "-td", str(args.num_threads)]
            else:
                cmd = ["numactl", f"--physcpubind={gen_threads_config(args.num_threads, n)}",str(mem_place),
                       "/llm/llama-batched-bench", "-m", args.model, "-c", str(args.kv_cache), "-b", "2048", "-ub", "512", "-npp", str(args.prompt_size), "-ntg", str(TOKENS),
                       "-npl", str(args.batch_size), "-t", str(args.num_threads), "-tb", str(args.num_threads), "-td", str(args.num_threads)]

        else:
            print("FAIL: batched-bench not found!")
            sys.exit(1)

        current_subprocesses.append(
            subprocess.Popen(cmd, stdout=open(logfile, 'wb'), stderr=open(logfile, 'wb')))
    start = time.time()
    if any(p.wait() != 0 for p in current_subprocesses):
        print("FAIL: At least one process returned exit code other than 0 or died!")
        sys.exit(1)
    finish = time.time()
    summarize_results(logs_dir, args, start, finish)


if __name__ == "__main__":
    main()
