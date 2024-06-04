set -eo pipefail

apt update && apt install -y docker.io
apt-get update && apt-get install -y python3 python3-pip
pip3 install huggingface-hub psutil
