# Wrapper for multi-process / batched benchmark of llama.cpp


## ARM
Instructions assume you have a debian based OS
```bash
cd benchmarks
sudo bash setup_deb.sh
# vim download_models.sh # uncomment / add models you want to download
bash download_models.sh
# vim run.sh # modify run.sh (provide the name of the docker image, threads, batch sizes etc.)
nohup sudo bash run.sh
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
# vim run.sh # modify run.sh (provide the name of the docker image, threads, batch sizes etc.)
nohup sudo bash run.sh
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