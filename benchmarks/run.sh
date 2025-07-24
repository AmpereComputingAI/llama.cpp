set -e

python3 run.py -m Meta-Llama-3-8B-Instruct.Q8_0.gguf -t 10 16 32 40 64 80 -b 1 2 4 8 16 32 64 -p 512 -r 0-79 -fa 1
rm -f /tmp/log_power
