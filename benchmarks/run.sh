set -e

python3 run.py -m llama-3.1-8b-instruct-Q8R16.gguf -t 10 16 32 40 64 80 -b 1 2 4 8 16 32 64 -p 512 -r 0-79 -fa
