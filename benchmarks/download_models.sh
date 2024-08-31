set -eo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mkdir -p $SCRIPT_DIR/models
#huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False
#huggingface-cli download TheBloke/Llama-2-13B-GGUF llama-2-13b.Q4_K_M.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False
#huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q8_0.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False
#huggingface-cli download TheBloke/Llama-2-13B-GGUF llama-2-13b.Q8_0.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False
#huggingface-cli download TheBloke/Llama-2-70B-GGUF llama-2-70b.Q4_K_M.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False
huggingface-cli download QuantFactory/Meta-Llama-3-8B-Instruct-GGUF Meta-Llama-3-8B-Instruct.Q8_0.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False
huggingface-cli download QuantFactory/Meta-Llama-3-8B-Instruct-GGUF Meta-Llama-3-8B-Instruct.Q4_K_M.gguf --local-dir $SCRIPT_DIR/models --local-dir-use-symlinks False

wget -P models https://ampereaimodelzoo.s3.eu-central-1.amazonaws.com/gguf/Meta-Llama-3-8B-Instruct.Q4_K_4.gguf
wget -P models https://ampereaimodelzoo.s3.eu-central-1.amazonaws.com/gguf/Meta-Llama-3-8B-Instruct.Q8R16.gguf