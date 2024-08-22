set -e

python3 run.py -m Meta-Llama-3-8B-Instruct.Q8_0.gguf -t 8 12 16 24 48 -b 1 2 4 8 16 32 -p 128 -r 0-47 -d llama.cpp:latest
rm -f /tmp/log_power
