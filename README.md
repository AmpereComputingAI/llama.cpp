![llama.cpp](https://user-images.githubusercontent.com/1991296/230134379-7181e485-c521-4d23-a0d6-f7b3b61ba524.png "llama.cpp")
# Ampere® optimized llama.cpp
![llama.cpp pull count](https://img.shields.io/docker/pulls/amperecomputingai/llama.cpp?logo=meta&logoColor=black&label=llama.cpp&labelColor=violet&color=purple)

Ampere® optimized build of [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#llamacpp) with full support for rich collection of GGUF models available at HuggingFace: [GGUF models](https://huggingface.co/models?search=gguf)

This Docker image can be run on bare metal Ampere® CPUs and Ampere® based VMs available in the cloud.

Release notes and binary executables are available on our [GitHub](https://github.com/AmpereComputingAI/llama.cpp/releases)

## Starting container
Default entrypoint runs the server binary of llama.cpp, mimicking behavior of original llama.cpp server image: [docker image](https://github.com/ggerganov/llama.cpp/blob/master/.devops/server.Dockerfile)

To launch shell instead, do this:

```bash
sudo docker run --privileged=true --name llama --entrypoint /bin/bash -it amperecomputingai/llama.cpp:latest
```
Quick start example will be presented at docker container launch:

![quick start](https://ampereaimodelzoo.s3.eu-central-1.amazonaws.com/pictures/Screenshot+2024-04-30+at+22.37.13.png "quick start")

Make sure to visit us at [Ampere Solutions Portal](https://solutions.amperecomputing.com/solutions/ampere-ai)!

## Support

Please contact us at <ai-support@amperecomputing.com>

## LEGAL NOTICE
By accessing, downloading or using this software and any required dependent software (the “Ampere AI Software”), you agree to the terms and conditions of the software license agreements for the Ampere AI Software, which may also include notices, disclaimers, or license terms for third party software included with the Ampere AI Software. Please refer to the [Ampere AI Software EULA v1.6](https://ampereaidevelop.s3.eu-central-1.amazonaws.com/Ampere+AI+Software+EULA+-+v1.6.pdf) or other similarly-named text file for additional details.
