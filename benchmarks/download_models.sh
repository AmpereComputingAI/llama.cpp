set -eo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mkdir -p $SCRIPT_DIR/models
hf download AmpereComputing/llama-3.1-8b-instruct-gguf llama-3.1-8b-instruct-Q8R16.gguf --local-dir $SCRIPT_DIR/models
