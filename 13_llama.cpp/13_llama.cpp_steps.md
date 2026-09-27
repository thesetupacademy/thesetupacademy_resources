# llama.cpp Installation

## 1. Install

### Linux / macOS

```bash
curl -LsSf https://llama.app/install.sh | sh
```

### Windows

Run PowerShell and execute:

```powershell
irm https://llama.app/install.ps1 | iex
```

## 2. Verify Installation

```bash
llama --version
```

## 3. Run Qwen3.5 1B

```bash
llama cli -hf ggml-org/Qwen3.5-0.8B-GGUF
```

## 4. Start Server + Web UI

```bash
llama serve -hf ggml-org/Qwen3.5-0.8B-GGUF

llama serve -hf ggml-org/gemma-3-1b-it-qat-GGUF:Q4_0
```

Open the Web UI:

```text
http://localhost:8080
```

## 5. Test the API

```bash
curl.exe --% http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"gemma-3-1b-it-qat\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello, explain AI in one sentence.\"}]}"
```

llama.cpp provides an **OpenAI-compatible API** for connecting Qwen3.5 1B with Python and other applications.
