![Ampere AI](https://ampereaimodelzoo.s3.eu-central-1.amazonaws.com/ampere_logo_®_primary_stacked_rgb.png "Ampere AI")
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

### results on Altra Max with 128 threads on 1 process:

#### Meta-Llama-3-8B-Instruct.Q4_K_4.gguf

| Batch Size | total token generation capability, tps |
|------------|----------------------------------------|
| 1          | 26.13                                  |
| 32         | 102.85                                 |

#### Meta-Llama-3-8B-Instruct.Q8R16.gguf

| Batch Size | total token generation capability, tps |
|------------|----------------------------------------|
| 1          | 18.37                                  |
| 32         | 121.19                                 |