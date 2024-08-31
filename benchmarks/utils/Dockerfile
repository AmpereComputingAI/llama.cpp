FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y build-essential cmake vim wget git numactl libopenblas-dev pkg-config python3 python3-pip libnuma-dev clang
RUN mkdir /workspace
RUN mkdir /llm
RUN cd /workspace && git clone -b b3615 https://github.com/ggerganov/llama.cpp.git && cd llama.cpp && make -j && mv /workspace/llama.cpp/llama-batched-bench /llm/
RUN rm -R /workspace