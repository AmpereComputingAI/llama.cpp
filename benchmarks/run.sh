set -e

python3 run.py -m Meta-Llama-3-8B-Instruct.Q4_K_4.gguf Meta-Llama-3-8B-Instruct.Q8R16.gguf -t 128 -b 1 32 -p 128 -r 0-127 -d amperecomputingai/llama.cpp:latest
