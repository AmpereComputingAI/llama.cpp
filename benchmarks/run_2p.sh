set -e

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches
echo 1 | sudo tee /proc/sys/vm/swappiness
echo 8 | sudo tee /proc/sys/vm/dirty_ratio
echo 1 | sudo tee /proc/sys/vm/zone_reclaim_mode
echo 0 | sudo tee /proc/sys/kernel/numa_balancing

VAR_PAGESIZE=$(getconf PAGESIZE)
if [ $VAR_PAGESIZE = 4096 ]; then
  echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
elif [ $VAR_PAGESIZE = 65536 ]; then
  echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
fi

# Warm up
python3 run.py -m DeepSeek-R1-Distill-Qwen-7B-Q8R16_n0.gguf -t 80 -b 1 -p 512 -r 0-79 -n 0
python3 run.py -m DeepSeek-R1-Distill-Qwen-7B-Q8R16_n1.gguf -t 80 -b 1 -p 512 -r 80-159 -n 1

# Run  
python3 run.py -m DeepSeek-R1-Distill-Qwen-7B-Q8R16_n0.gguf -t 80 64 48 40 32 24 20 16 12 10 8 -b 1 2 4 8 -p 512 -r 0-79 -n 0 &
python3 run.py -m DeepSeek-R1-Distill-Qwen-7B-Q8R16_n1.gguf -t 80 64 48 40 32 24 20 16 12 10 8 -b 1 2 4 8 -p 512 -r 80-159 -n 1 &
wait
