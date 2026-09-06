# Ollama Response

### Start Ollama

```bash
ollama serve
```

### List Installed Models

```bash
ollama list
```

# Ollama Status / Speed Issues

Check which models are currently loaded and running:

```bash
ollama ps
```

# Ollama API Not Accessible

### Linux / macOS

Test whether the Ollama API is responding:

```bash
curl http://localhost:11434/api/tags
```

### Windows

Use `curl.exe` to test the Ollama API:

```powershell
curl.exe http://localhost:11434/api/tags
```

# Connection Refused

### Windows

Check whether Ollama is listening on port `11434`:

```powershell
netstat -ano | findstr 11434
```

### Linux / Ubuntu

```bash
ss -lntp | grep 11434
```

# Hosting Ollama Over the Network

To make Ollama accessible over the network:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### Test from Another Machine

Replace `SERVER_IP` with the IP address of the machine running Ollama:

```bash
curl http://SERVER_IP:11434/api/tags
```

On Windows:

```powershell
curl.exe http://SERVER_IP:11434/api/tags
```

# Logs

## Windows

1. Press **`Win + R`**.

2. Type:

```text
explorer %LOCALAPPDATA%\Ollama
```

3. Open the **`logs`** folder.

4. Check the most recent `server-#.log` file.

## Ubuntu / Linux

View Ollama logs:

```bash
journalctl -u ollama --no-pager
```

Follow logs in real time:

```bash
journalctl -u ollama --follow
```

Or combine both:

```bash
journalctl -u ollama --no-pager --follow
```

# Check Model Speed

Run a model with verbose output to see performance information such as tokens per second:

```bash
ollama run <model> --verbose
```

Example:

```bash
ollama run qwen3:4b --verbose
```