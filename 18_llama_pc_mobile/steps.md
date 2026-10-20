# LlamaNode + llama.cpp RPC Setup (Windows + Android)

Use your Samsung Galaxy A55 as an RPC worker for `llama.cpp` on Windows.

**Project:** https://github.com/adil-adysh/llama-cpp-android-node\
**Windows client:**
https://github.com/ggml-org/llama.cpp/releases/tag/b11429\
**Model:**
https://huggingface.co/tensorblock/SmolLM2-135M-Instruct-GGUF/blob/main/SmolLM2-135M-Instruct-Q2_K.gguf

## 1. Install prerequisites

Install: - Git for Windows - JDK 17 (or the version required by the
current project) - Android Studio, including Android SDK,
Platform-Tools, Build-Tools and command-line tools

Set SDK variables in PowerShell:

``` powershell
$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot"
$env:Path = "$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools;$env:Path"
```

Adjust `JAVA_HOME` if your JDK is elsewhere. Confirm USB debugging is
enabled on the phone and accept the debugging prompt.

## 2. Download and prepare LlamaNode

``` powershell
Set-Location "F:\training_videos"
git clone https://github.com/adil-adysh/llama-cpp-android-node.git
Set-Location "F:\training_videos\llama-cpp-android-node"
```

Fetch the project's prebuilt native binaries:

``` powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\fetch-prebuilt-native.ps1"
```

If the project's current README specifies a different script or
prerequisite, follow that README.

## 3. Build the APK

``` powershell
.\gradlew.bat assembleDebug
```

Expected APK:

``` text
app\build\outputs\apk\debug\app-debug.apk
```

Install it:

``` powershell
& "$env:ANDROID_HOME\platform-tools\adb.exe" devices
& "$env:ANDROID_HOME\platform-tools\adb.exe" install -r ".\app\build\outputs\apk\debug\app-debug.apk"
```

## 4. Download the Windows `llama.cpp` client

Download and extract the **Windows x64 b11429** asset from the official
release page above into:

``` text
F:\training_videos\llama.cpp--b11429
```

Locate `llama-cli.exe` if needed:

``` powershell
Get-ChildItem "F:\training_videos\llama.cpp--b11429" -Filter "llama-cli.exe" -Recurse
```

Verify the version using the actual executable path:

``` powershell
& "F:\training_videos\llama.cpp--b11429\bin\llama-cli.exe" --version
```

The path may differ depending on how the archive extracts.

## 5. Download the GGUF model

``` powershell
New-Item -ItemType Directory -Force "F:\training_videos\models" | Out-Null
hf download tensorblock/SmolLM2-135M-Instruct-GGUF SmolLM2-135M-Instruct-Q2_K.gguf --local-dir "F:\training_videos\models"
```

If `hf` is not recognized:

``` powershell
py -m pip install -U huggingface_hub
```

Verify:

``` powershell
Test-Path "F:\training_videos\models\SmolLM2-135M-Instruct-Q2_K.gguf"
```

## 6. Test the model on the PC first

Replace the executable path if needed:

``` powershell
& "F:\training_videos\llama.cpp--b11429\bin\llama-cli.exe" -m "F:\training_videos\models\SmolLM2-135M-Instruct-Q2_K.gguf" -t 4 -c 1024 -p "Say hello in one sentence." -n 32
```

Continue only after it generates a response.

## 7. Start the Android RPC worker

1.  Open LlamaNode on the phone.
2.  Select **Auto (GPU-first)**. If RPC inference fails, retry with
    **ARM CPU**.
3.  Use port `50052` and **Loopback (`127.0.0.1`)** for USB forwarding.
4.  Tap **START RPC SERVER** and confirm **RUNNING**.

Keep the app running while testing.

## 8. Forward the RPC port over USB

``` powershell
& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" devices
& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" forward tcp:50052 tcp:50052
& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" forward --list
Test-NetConnection 127.0.0.1 -Port 50052
```

ADB should list the phone as `device`; the forward list should show
`tcp:50052 tcp:50052`. TCP success alone does **not** prove RPC
inference works.

If forwarding is stale:

``` powershell
& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" forward --remove tcp:50052
& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" forward tcp:50052 tcp:50052
```

## 9. Run inference with the phone RPC worker

Use the actual path to `llama-cli.exe`:

``` powershell
& "F:\training_videos\llama.cpp-b11429\bin\llama-cli.exe" -m "F:\training_videos\models\SmolLM2-135M-Instruct-Q2_K.gguf" --rpc 127.0.0.1:50052 -ngl 99 -t 4 -c 1024 -p "Say hello in one sentence." -n 32 --verbose
```

Confirm that text is generated and PC logs show RPC/device offloading.
`-ngl 99` requests maximum layer offloading; it does not itself prove
that the phone is doing the work.

## Troubleshooting

  ------------------------------------------------------------------------
  Problem                             First fix
  ----------------------------------- ------------------------------------
  `adb` not recognized                Use the full path to `adb.exe` shown
                                      above.

  Phone says `unauthorized`           Unlock it and accept USB debugging.

  Gradle cannot find SDK              Set
                                      `ANDROID_HOME`/`ANDROID_SDK_ROOT`;
                                      add `sdk.dir` to project
                                      `local.properties` if needed.

  Java/Gradle error                   Check `JAVA_HOME` and use a JDK
                                      supported by the project.

  Native provisioning fails           Read the first download error;
                                      follow the current project README.
                                      Don't create placeholder native
                                      libraries.

  APK missing                         Fix the first Gradle error, then
                                      rerun `assembleDebug`.

  Hugging Face `File not found`       Verify repository and exact filename
                                      `SmolLM2-135M-Instruct-Q2_K.gguf`.

  GGUF fails to open                  Verify the model path and download
                                      completed.

  TCP test fails                      Start the LlamaNode server and
                                      recreate the ADB forward.

  Phone only says                     TCP connected, but RPC
  `Accepted client connection`        handshake/inference isn't confirmed.
                                      Check PC logs and try ARM CPU
                                      backend.

  RPC hangs                           Stop after 15--30 seconds; verify
                                      b11429 client, model path,
                                      forwarding and backend. Capture the
                                      first error.

  Vulkan errors                       Switch LlamaNode to ARM CPU and
                                      retry.

  Missing DLL on Windows              Re-extract the complete official
                                      Windows archive; keep supplied DLLs
                                      beside the executable.
  ------------------------------------------------------------------------

## Quick start (after setup)

1.  Connect/unlock phone; keep USB debugging enabled.
2.  Start LlamaNode RPC server on port `50052`.
3.  Run `adb forward tcp:50052 tcp:50052`.
4.  Run the inference command in section 9.
5.  Check PC logs for actual RPC offloading.

**Security:** Do not expose RPC port `50052` to the public internet.
Keep loopback/USB mode unless you intentionally configure a trusted LAN.
