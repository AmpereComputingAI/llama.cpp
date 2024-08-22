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

Benchmarks will take few hours in default setting, going over various combinations of n_proc x n_threads x batch_size x prompt_size x model_size 😵‍💫
After they complete you will find .csv files with results in the benchmarks directory of this repo.