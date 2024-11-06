![llama.cpp](https://user-images.githubusercontent.com/1991296/230134379-7181e485-c521-4d23-a0d6-f7b3b61ba524.png "llama.cpp")
# Ampere® optimized llama.cpp
![llama.cpp pull count](https://img.shields.io/docker/pulls/amperecomputingai/llama.cpp?logo=meta&logoColor=black&label=llama.cpp&labelColor=violet&color=purple)

Ampere® optimized build of [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#llamacpp) with full support for rich collection of GGUF models available at HuggingFace: [GGUF models](https://huggingface.co/models?search=gguf)

**For best results we recommend using models in our custom quantization formats available here: [AmpereComputing HF](https://huggingface.co/AmpereComputing)**

This Docker image can be run on bare metal Ampere® CPUs and Ampere® based VMs available in the cloud.

Release notes and binary executables are available on our [GitHub](https://github.com/AmpereComputingAI/llama.cpp/releases)

## Starting container
Default entrypoint runs the server binary of llama.cpp, mimicking behavior of original llama.cpp server image: [docker image](https://github.com/ggerganov/llama.cpp/blob/master/.devops/llama-server.Dockerfile)

To launch shell instead, do this:

```bash
sudo docker run --privileged=true --name llama --entrypoint /bin/bash -it amperecomputingai/llama.cpp:latest
```
Quick start example will be presented at docker container launch:

![quick start](https://ampereaimodelzoo.s3.eu-central-1.amazonaws.com/pictures/Screenshot+2024-04-30+at+22.37.13.png "quick start")

Make sure to visit us at [Ampere Solutions Portal](https://solutions.amperecomputing.com/solutions/ampere-ai)!

## Quantization
Ampere® optimized build of llama.cpp provides support for two new quantization methods, Q4_K_4 and Q8R16, offering model size and perplexity similar to Q4_K and Q8_0, respectively, but performing up to 1.5-2x faster on inference.

First, you'll need to convert the model to the GGUF format using [this script](https://github.com/ggerganov/llama.cpp/blob/master/convert_hf_to_gguf.py):

```bash
python3 convert-hf-to-gguf.py [path to the original model] --outtype [f32, f16, bf16 or q8_0] --outfile [output path]
```

For example:

```bash
python3 convert-hf-to-gguf.py path/to/llama2 --outtype f16 --outfile llama-2-7b-f16.gguf
```

Next, you can quantize the model using the following command:
```bash
./llama-quantize [input file] [output file] [quantization method]
```

For example:
```bash
./llama-quantize llama-2-7b-f16.gguf llama-2-7b-Q8R16.gguf Q8R16
```

## Benchmark Results
Benchmark results conducted by our Team can be found in **benchmarks/example_results**, with data selectable by machine type and software.

## Support

Please contact us at <ai-support@amperecomputing.com>

## LEGAL NOTICE
By accessing, downloading or using this software and any required dependent software (the “Ampere AI Software”), you agree to the terms and conditions of the software license agreements for the Ampere AI Software, which may also include notices, disclaimers, or license terms for third party software included with the Ampere AI Software. Please refer to the [Ampere AI Software EULA v1.6](https://ampereaidevelop.s3.eu-central-1.amazonaws.com/Ampere+AI+Software+EULA+-+v1.6.pdf) or other similarly-named text file for additional details.
