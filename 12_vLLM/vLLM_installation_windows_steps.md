# vLLM CPU Setup — Windows Docker

## 1. Clone vLLM

```powershell
cd F:\training_videos\raw_videos\12_vLLM

git clone https://github.com/vllm-project/vllm.git vllm_source

cd .\vllm_source
```

## 2. Build CPU Image

```powershell
docker build -f docker/Dockerfile.cpu --build-arg VLLM_CPU_X86=false --tag vllm-cpu-env --target vllm-openai .
```

### Build Error: `$'\r': command not found`

If you see:

```text
build_rust.sh: line 7: $'\r': command not found
```

Fix the line endings:

```powershell
$content = [System.IO.File]::ReadAllText((Join-Path (Get-Location) "build_rust.sh"))
$content = $content -replace "`r`n", "`n"
[System.IO.File]::WriteAllText((Join-Path (Get-Location) "build_rust.sh"), $content, [System.Text.UTF8Encoding]::new($false))
```

Then rebuild:

```powershell
docker build -f docker/Dockerfile.cpu --build-arg VLLM_CPU_X86=false --tag vllm-cpu-env --target vllm-openai .
```

### Build Error: `invalid toolchain name`

If you see:

```text
invalid toolchain name: '1.95
```

Fix `rust-toolchain.toml`:

```powershell
$content = [System.IO.File]::ReadAllText((Join-Path (Get-Location) "rust-toolchain.toml"))
$content = $content -replace "`r`n", "`n"
[System.IO.File]::WriteAllText((Join-Path (Get-Location) "rust-toolchain.toml"), $content, [System.Text.UTF8Encoding]::new($false))
```

Then rebuild:

```powershell
docker build -f docker/Dockerfile.cpu --build-arg VLLM_CPU_X86=false --tag vllm-cpu-env --target vllm-openai .
```

## 3. Run Qwen3-0.6B

```powershell
docker run --rm --security-opt seccomp=unconfined --cap-add SYS_NICE --shm-size=4g -p 8000:8000 -e VLLM_CPU_OMP_THREADS_BIND=0-3 -v "${env:USERPROFILE}\.cache\huggingface:/root/.cache/huggingface" vllm-cpu-env Qwen/Qwen3-0.6B
```

## 4. Test API

Open another PowerShell:

```powershell
curl http://localhost:8000/v1/models
```

Test generation:

```powershell
curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"Qwen/Qwen3-0.6B","messages":[{"role":"user","content":"What is RAG?"}],"max_tokens":100}'
```

> **Note:** The prebuilt `vllm/vllm-openai-cpu:latest-x86_64` image caused `SIGILL` on the i5-3470S, so use the locally built image above.
