## Change log

### Release v2.0.0

- Based on ggerganov/llama.cpp b3485 (https://github.com/ggerganov/llama.cpp/releases/tag/b3485)
- Upgraded upstream tag enables Llama 3.1 in ollama
- Native support for AmpereOne platform
- Breaking change: due to changed weight type IDs it is now required to re-quantize models to Q8R16 and Q4_K_4 formats with current llama-quantize tool.

### Release v1.2.7

- Based on ggerganov/llama.cpp b3340 (https://github.com/ggerganov/llama.cpp/releases/tag/b3340)

### Release v1.2.6

- Based on ggerganov/llama.cpp b3171 (https://github.com/ggerganov/llama.cpp/releases/tag/b3171)

### Release v1.2.5

- Based on ggerganov/llama.cpp b3074 (https://github.com/ggerganov/llama.cpp/releases/tag/b3074)
- Ampere optimizations can now be optionally disabled via CMake option LLAMA_AIO

### Release v1.2.4

- Rebase to ggerganov/llama.cpp b3074 (https://github.com/ggerganov/llama.cpp/releases/tag/b3074)
- Introducing Q4_K_4 quantized format as a 1.5x faster replacement for Q4_K.
- Q8R16 and Q4_K_4 are now natively supported by bin/quantize and other tools (see README)

### Release v1.2.3

- Rebase to ggerganov/llama.cpp b2953 (https://github.com/ggerganov/llama.cpp/releases/tag/b2953)
- The rebase is to allow llama-cpp-python to pick up upstream CVE fix (https://github.com/abetlen/llama-cpp-python/security/advisories/GHSA-56xg-wfcc-g829)
- Experimental support for Q8R16 quantized format with optimized matrix multiplication kernels
- CMake files updated to build llama.aio on Ampere Altra