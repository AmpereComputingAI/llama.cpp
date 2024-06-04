import os
import sys
import time
import psutil
import argparse
import subprocess
from utils.benchmark import parse_threads_range


def get_file_dir():
    return os.path.dirname(os.path.realpath(__file__))


def docker_init():
    tag = "amperecomputingai/llama.cpp:1.2.3"
    if subprocess.run(
            ["docker", "pull", tag]).returncode != 0:
        print("Docker pull process failed!")
        sys.exit(1)
    container_name = "llama_benchmark"
    subprocess.run(["docker", "rm", "-f", container_name])
    memory = (psutil.virtual_memory().total >> 30) - 30  # leave 30GB for OS
    assert memory > 10, "less than 10GB of memory available on the system for llama.cpp"
    if subprocess.run(
            ["docker", "run", "--privileged=true", "--name", container_name, "-d", "-m", f"{str(memory)}g", "-v",
             f"{get_file_dir()}:/runner", "--entrypoint", "/bin/bash", "-it", tag]).returncode != 0:
        print("Docker run process failed!")
        sys.exit(1)
    return container_name


def docker_restart(docker_name):
    break_time = 15

    def docker_stop():
        if subprocess.run(["docker", "stop", docker_name]).returncode != 0:
            print(f"Stopping docker container {docker_name} failed, retrying in {break_time} seconds.")
            time.sleep(break_time)
            docker_stop()

    def docker_start():
        if subprocess.run(["docker", "start", docker_name]).returncode != 0:
            print(f"Starting docker container {docker_name} failed, retrying in {break_time} seconds.")
            time.sleep(break_time)
            docker_start()

    print(f"\nRestarting docker container {docker_name} ...")
    docker_stop()
    docker_start()


def benchmark(docker_container_name, args):
    num_available_threads = len(parse_threads_range(args.threads_range))
    if num_available_threads < max(args.num_threads):
        print(f"Requested number of threads ({max(args.num_threads)}) exceeds threads available ({num_available_threads})")
        sys.exit(1)

    docker_restart(docker_container_name)
    for model in args.model_names:
        for prompt_size in sorted(args.prompt_sizes):
            for batch_size in sorted(args.batch_sizes):
                for num_threads in sorted(args.num_threads):
                    num_processes = int(num_available_threads / num_threads)
                    case = f"{num_processes} x {num_threads} [proc x threads], bs = {batch_size}"
                    print(f"\nRunning {case}")
    
                    cmd = (f"cd /runner; python3 utils/benchmark.py -m models/{model} -n {str(num_processes)} "
                           f"-t {str(num_threads)} -b {str(batch_size)} -p {str(prompt_size)} -r {args.threads_range}")
                    cmd = ["docker", "exec", "-i", docker_container_name, "bash", "-c", cmd]
    
                    print(f"Executing: {' '.join(cmd)}")
                    success = False
                    start = time.time()
                    p = subprocess.Popen(cmd, start_new_session=True)
                    while time.time() - start < args.timeout:
                        time.sleep(1)
                        exit_code = p.poll()
                        if exit_code is not None:
                            success = exit_code == 0
                            break
                    if success:
                        print(f"SUCCESS: {case}")
                    else:
                        print(f"FAIL: {case}")
                        docker_restart(docker_container_name)


def parse_args():
    parser = argparse.ArgumentParser(description="Run set of benchmarks.")
    parser.add_argument("-m", "--model_names",
                        type=str, required=True, nargs="+",
                        help="model names, e.g. 'Meta-Llama-3-8B-Instruct.Q8_0.gguf'")
    parser.add_argument("-t", "--num_threads",
                        type=int, required=True, nargs="+",
                        help="number of threads per process to use")
    parser.add_argument("-b", "--batch_sizes",
                        type=int, required=True, nargs="+",
                        help="batch sizes to cover")
    parser.add_argument("-p", "--prompt_sizes",
                        type=int, required=True, nargs="+",
                        help="prompt sizes to cover")
    parser.add_argument("-r", "--threads_range",
                        type=str, required=True,
                        help="range of threads to use in offline mode, e.g. '0-63,128-191', threads will be divided "
                             "between processes - hint: 'lscpu | grep NUMA'")
    parser.add_argument("--timeout",
                        type=float, default=900,
                        help="timeout to apply per single benchmark case")
    return parser.parse_args()


def main():
    args = parse_args()
    benchmark(docker_init(), args)


if __name__ == "__main__":
    main()
