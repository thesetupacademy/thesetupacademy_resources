# vLLM CPU Installation — Linux / WSL

> Based on the official vLLM CPU installation documentation:
> https://docs.vllm.ai/en/latest/getting_started/installation/cpu/

## 1. Requirements

For Intel/AMD x86 CPU:

- OS: Linux
- Python: 3.10–3.13
- CPU flags:
  - `avx512f` — recommended
  - `avx2` — limited features
- Compiler: `gcc/g++ >= 12.3.0` recommended

Check your CPU:

```bash
lscpu
```

Check your compiler:

```bash
gcc --version
g++ --version
```

---

## 2. Install Build Dependencies

### Ubuntu

```bash
sudo apt-get update -y

sudo apt-get install -y \
    gcc-12 \
    g++-12 \
    libnuma-dev
```

Set GCC 12/G++ 12 as the default compiler:

```bash
sudo update-alternatives \
    --install /usr/bin/gcc gcc /usr/bin/gcc-12 10 \
    --slave /usr/bin/g++ g++ /usr/bin/g++-12
```

Verify:

```bash
gcc --version
g++ --version
```

---

## 3. Install `uv`

Install `uv` using the official `uv` installation instructions:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reload the shell:

```bash
source ~/.bashrc
```

Verify:

```bash
uv --version
```

---

## 4. Create a Python 3.12 Environment

Python 3.12 is recommended for this setup.

```bash
uv venv --python 3.12 --seed --managed-python
```

Activate it:

```bash
source .venv/bin/activate
```

Verify:

```bash
python --version
```

Expected:

```text
Python 3.12.x
```

---

## 5. Clone vLLM

For WSL/Linux, keep the source inside the Linux filesystem rather than `/mnt/c` for better build performance.

```bash
cd ~
git clone https://github.com/vllm-project/vllm.git vllm_source
cd vllm_source
```

Verify:

```bash
pwd
```

Recommended:

```text
/home/<username>/vllm_source
```

---

## 6. Install vLLM CPU Build Dependencies

Using `uv`:

```bash
uv pip install \
    -r requirements/build/cpu.txt \
    --torch-backend cpu \
    --index-strategy unsafe-best-match
```

Then:

```bash
uv pip install \
    -r requirements/cpu.txt \
    --torch-backend cpu \
    --index-strategy unsafe-best-match
```

---

## 7. Build and Install vLLM

```bash
VLLM_TARGET_DEVICE=cpu uv pip install . --no-build-isolation
```

This compiles vLLM specifically for the CPU backend.

---

## 8. Verify Installation

Check the installed version:

```bash
python -c "import vllm; print(vllm.__version__)"
```

Check the CLI:

```bash
vllm --help
```

---

## 9. Install TCMalloc

For CPU performance, install TCMalloc:

```bash
sudo apt-get install -y --no-install-recommends \
    libtcmalloc-minimal4
```

Find TCMalloc:

```bash
sudo find / -iname '*libtcmalloc_minimal.so.4'
```

Find Intel OpenMP:

```bash
sudo find / -iname '*libiomp5.so'
```

Set the paths:

```bash
TC_PATH=/path/to/libtcmalloc_minimal.so.4
IOMP_PATH=/path/to/libiomp5.so
```

Add them to `LD_PRELOAD`:

```bash
export LD_PRELOAD="$TC_PATH:$IOMP_PATH:$LD_PRELOAD"
```

---

## 10. Run vLLM on CPU

Example:

```bash
vllm serve <MODEL_NAME> \
    --device cpu
```

Replace `<MODEL_NAME>` with the Hugging Face model you want to serve.

Example:

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
    --device cpu
```

---

# Troubleshooting

## NumPy >= 2.0 Error

If you encounter a NumPy compatibility error:

```bash
pip install "numpy<2.0"
```

---

## CMake Detects CUDA

For a CPU-only build, disable CUDA detection:

```bash
export CMAKE_DISABLE_FIND_PACKAGE_CUDA=ON
```

Then rebuild:

```bash
VLLM_TARGET_DEVICE=cpu uv pip install . --no-build-isolation
```

---

## C++ Compiler Not Found

If you see:

```text
No CMAKE_CXX_COMPILER could be found
```

install the compiler:

```bash
sudo apt-get update -y
sudo apt-get install -y gcc-12 g++-12
```

Verify:

```bash
gcc --version
g++ --version
```

---

## Python Version Error

vLLM CPU currently documents:

```text
Python 3.10–3.13
```

Do not use Python 3.14 for this setup.

Create a clean environment:

```bash
rm -rf .venv
uv venv --python 3.12 --seed --managed-python
source .venv/bin/activate
```

---

## Building from `/mnt/c`

Avoid building vLLM from:

```text
/mnt/c/...
```

Move the source into the WSL filesystem:

```bash
mv /mnt/c/path/to/vllm_source ~/vllm_source
cd ~/vllm_source
```

---

## Clean and Rebuild

If a previous build failed:

```bash
rm -rf build
rm -rf .deps
```

Then reinstall dependencies:

```bash
uv pip install \
    -r requirements/build/cpu.txt \
    --torch-backend cpu \
    --index-strategy unsafe-best-match

uv pip install \
    -r requirements/cpu.txt \
    --torch-backend cpu \
    --index-strategy unsafe-best-match
```

Build again:

```bash
VLLM_TARGET_DEVICE=cpu uv pip install . --no-build-isolation
```

---

# Optional: Build a Wheel

Build a portable wheel:

```bash
VLLM_TARGET_DEVICE=cpu uv build --wheel --no-build-isolation
```

Install it:

```bash
uv pip install dist/*.whl
```

---

# Quick Installation

For a fresh Ubuntu/WSL setup, the essential sequence is:

```bash
sudo apt-get update -y

sudo apt-get install -y \
    gcc-12 \
    g++-12 \
    libnuma-dev \
    git \
    curl

sudo update-alternatives \
    --install /usr/bin/gcc gcc /usr/bin/gcc-12 10 \
    --slave /usr/bin/g++ g++ /usr/bin/g++-12

curl -LsSf https://astral.sh/uv/install.sh | sh

source ~/.bashrc

uv venv --python 3.12 --seed --managed-python
source .venv/bin/activate

git clone https://github.com/vllm-project/vllm.git vllm_source
cd vllm_source

uv pip install \
    -r requirements/build/cpu.txt \
    --torch-backend cpu \
    --index-strategy unsafe-best-match

uv pip install \
    -r requirements/cpu.txt \
    --torch-backend cpu \
    --index-strategy unsafe-best-match

VLLM_TARGET_DEVICE=cpu uv pip install . --no-build-isolation

python -c "import vllm; print(vllm.__version__)"
```

## Official Documentation

https://docs.vllm.ai/en/latest/getting_started/installation/cpu/
