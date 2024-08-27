# Wrapper for multi-process / batched benchmark of llama.cpp


## ARM
Instructions assume you have a debian based OS
```bash
cd benchmarks
sudo bash setup_deb.sh
# vim download_models.sh # uncomment / add models you want to download
bash download_models.sh
# quick run
sudo python3 run.py -m Meta-Llama-3-8B-Instruct.Q4_K_4.gguf Meta-Llama-3-8B-Instruct.Q8R16.gguf -t 128 -b 1 -p 128 -r 0-127 -d amperecomputingai/llama.cpp:latest
```

## x86
Instructions assume you have a debian based OS
```bash
cd benchmarks
sudo bash setup_deb.sh
# vim download_models.sh # uncomment / add models you want to download
bash download_models.sh

cd utils
sudo docker build -t llama_x86 .
cd ..
# quick run
python3 run.py -m Meta-Llama-3-8B-Instruct.Q4_K_M.gguf Meta-Llama-3-8B-Instruct.Q8_0.gguf -t 128 -b 1 -p 128 -r 0-127 -d llama_x86:latest
```

Benchmarks will take a moment in default setting.
After they complete you will find .csv files with results in the benchmarks directory of this repo.

### results on Altra Max
the results were gathered using amperecomputingai/llama.cpp:1.2.6 image with aio optimizations on an Altra Max.

#### Meta-Llama-3-8B-Instruct.Q4_K_4.gguf

| n_proc | n_threads | batch_size | prompt_size | output_tokens | total token generation capability, tps |
|--------|-----------|------------|-------------|---------------|----------------------------------------|
| 16     | 8         | 8          | 128         | 256           | 262.83                                 |


#### Meta-Llama-3-8B-Instruct.Q8R16.gguf

| n_proc | n_threads | batch_size | prompt_size | output_tokens | total token generation capability, tps |
|--------|-----------|------------|-------------|---------------|----------------------------------------|
| 10     | 12        | 16         | 128         | 256           | 294.23                                 |


## run.py options
Provide run.py Python script with following arguments:
- -m, filename(s) of model(s) that should be available under _**llama.cpp/benchmarks/models**_ directory, multiple models can be provided
- -t, threadpool(s) per single process, e.g., if there are 20 threads available on the system, if -t 10 is provided, 2 parallel processes will be spawned, each using 10 threads;
  multiple threadpools can be provided and they will be treated as separate cases to benchmark
- -b, batch size(s) to benchmark, meaning separate token generation streams handled as a single batch; multiple batch sizes can be provided and they will be treated as separate cases to benchmark
- -p, prompt size(s) to benchmark, size of an input prompt; multiple prompt sizes can be provided and they will be treated as separate cases to benchmark
- -r, thread-range, e.g., on an 80-thread system, it should be input as 0-79, unless user wants to use just a subset of available threads, say 16-63 (48 threads indexed 16<>63)
```bash
python3 run.py -m Meta-Llama-3-8B-Instruct.Q8_0.gguf -t 10 16 32 40 64 80 -b 1 2 4 8 16 32 64 -p 512 -r 0-79
```