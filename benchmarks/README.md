# Running benchmark

This benchmarking tool runs multi-process, throughput-oriented benchmark of Ampere optimized llama.cpp using arbitrary model(s) provided by the user. 
The benchmarking script spawns multiple parallel streams of token generation using llama.cpp and provides user with aggregate metrics of both prompt eval and token generation stages.
Underneath, the _batched-bench_ script from upstream llama.cpp project is being used in an unaltered form.
The script orchestrates the benchmark inside Docker container from the outside environment, **therefore this script should not be run inside Docker container.**

## Setup
Few dependencies need to be installed first. On Debian-based systems you can use the setup script.
```bash
sudo bash setup_deb.sh
```

## Downloading models
Any GGUF model is expected to work, if you experience troubles running your network of choice please raise an [issue](https://github.com/AmpereComputingAI/llama.cpp/issues/new/choose).
Benchmarking script expects models to be placed under _**llama.cpp/benchmarks/models**_ dir.
```bash
mkdir -p models
hf download AmpereComputing/llama-3.1-8b-instruct-gguf llama-3.1-8b-instruct-Q8R16.gguf --local-dir models
```

## Benchmark
Provide run.py Python script with following arguments:
- -m, filename(s) of model(s) that should be available under _**llama.cpp/benchmarks/models**_ directory, multiple models can be provided
- -t, threadpool(s) per single process, e.g., if there are 20 threads available on the system, if -t 10 is provided, 2 parallel processes will be spawned, each using 10 threads;
  multiple threadpools can be provided and they will be treated as separate cases to benchmark
- -b, batch size(s) to benchmark, meaning separate token generation streams handled as a single batch; multiple batch sizes can be provided and they will be treated as separate cases to benchmark
- -p, prompt size(s) to benchmark, size of an input prompt; multiple prompt sizes can be provided and they will be treated as separate cases to benchmark
- -r, thread-range, e.g., on an 80-thread system, it should be input as 0-79, unless user wants to use just a subset of available threads, say 16-63 (48 threads indexed 16<>63)
- -fa, enable flash attention, default: disabled
- -d, docker_image, docker image used for benchmarking, default: amperecomputingai/llama.cpp:latest
```bash
python3 run.py -m llama-3.1-8b-instruct-Q8R16.gguf -t 10 16 32 40 64 80 -b 1 2 4 8 16 32 64 -p 512 -r 0-79 -fa -d amperecomputingai/llama.cpp:3.4.1
```

## Quick run on 80t OCI A1 system
```bash
bash setup_deb.sh  # works on Debian-based systems
bash download_models.sh  # uncomment preferred models in the file, by default llama3 q8_0 will be downloaded
bash run.sh  # modify to adjust number of threads available and other parameters
```

## Speedup Ampere optimized llama.cpp (r1.2.6) vs llama.cpp (b3615)

|                       | Q4_K_M  | Q4_K_4  | Speedup  |
|-----------------------|---|---|---|
|token generation (t/s) |  191.76 | 289.99  | 1.51x  |
|prompt processing (t/s)|  265.64 | 542.87  | 2.04x  |

|                       | Q8_0  | Q8R16  | Speedup  |
|-----------------------|---|---|---|
|token generation (t/s) | 248.17  | 313.78  | 1.26x  |
|prompt processing (t/s)| 410.90  | 950.64  | 2.31x  |
