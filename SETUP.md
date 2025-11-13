# Setup Guide for IndexTTS2 RunPod Worker

## Prerequisites

1. RunPod account with serverless access
2. IndexTTS2 model checkpoints downloaded
3. Reference audio files in WAV format

## Step-by-Step Setup

### 1. Download Model Checkpoints

You need to download the IndexTTS2 model checkpoints. These are large files (several GB) and should NOT be committed to git.

**Option A: Download to Local Machine**
- Follow instructions from [IndexTTS2 repository](https://github.com/index-tts/index-tts)
- Download checkpoints to a local directory

**Option B: Use RunPod Network Volume**
- Create a network volume in RunPod
- Upload checkpoints to the volume
- Mount the volume when creating your endpoint

### 2. Add Reference Audio Files

1. Place your WAV audio files in the `audio_files/` directory
2. Each file should be named to represent a voice/actor (e.g., `voice_01.wav`, `actor_name.wav`)
3. Files should be:
   - WAV format
   - Clear, single-speaker audio
   - Short reference clips (a few seconds work best)
   - 16kHz or higher sample rate recommended

### 3. Configure RunPod Template

#### Using GitHub Integration (Recommended)

1. Push this repository to GitHub
2. In RunPod Serverless dashboard:
   - Go to "Templates"
   - Click "New Template"
   - Connect your GitHub repository
   - Set build configuration:
     - **Dockerfile Path**: `Dockerfile`
     - **Build Context**: `.`
     - **Docker Image**: (auto-generated)
   - Set environment variables (if using network volumes):
     - `MODEL_DIR`: `/runpod-volume/checkpoints` (or your volume path)
     - `CONFIG_PATH`: `/runpod-volume/checkpoints/config.yaml`
     - `AUDIO_FILES_DIR`: `/app/audio_files`

#### Using Docker Registry

1. Build the Docker image:
   ```bash
   docker build -t your-registry/indextts2-runpod:latest .
   ```

2. Push to your registry:
   ```bash
   docker push your-registry/indextts2-runpod:latest
   ```

3. In RunPod:
   - Create new template
   - Select "Docker Image"
   - Enter your image URL
   - Configure environment variables as needed

### 4. Handle Model Checkpoints

Since model checkpoints are large, you have several options:

#### Option A: Network Volume (Recommended for RunPod)

1. Create a network volume in RunPod
2. Upload checkpoints to the volume
3. When creating an endpoint, mount the volume
4. Set `MODEL_DIR` environment variable to the mounted path

#### Option B: Include in Docker Image

**Warning**: This will create a very large Docker image (10GB+)

1. Copy checkpoints into the repository (but add to `.gitignore`)
2. Modify Dockerfile to copy checkpoints:
   ```dockerfile
   COPY checkpoints/ ./checkpoints/
   ```

#### Option C: Download at Runtime

Modify the Dockerfile to download checkpoints during build (if URLs are available).

### 5. Create Endpoint

1. In RunPod Serverless, go to "Endpoints"
2. Click "New Endpoint"
3. Select your template
4. Configure:
   - **GPU Type**: Select based on model requirements (typically A100 or similar)
   - **Max Workers**: Set based on expected load
   - **Idle Timeout**: Adjust as needed
   - **Volumes**: Mount your checkpoints volume if using Option A
   - **Environment Variables**: Set if different from template defaults

### 6. Test the Endpoint

Use the provided `test_input.json` or the Python example in README.md:

```python
import runpod
import base64

runpod.api_key = "your-api-key"

job = runpod.submit_job(
    endpoint_id="your-endpoint-id",
    input={
        "text": "Hello, this is a test.",
        "voice": "voice_01.wav"
    }
)

result = runpod.wait_for_output(job)

if result.get("audio_base64"):
    audio_data = base64.b64decode(result["audio_base64"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    print("Success! Audio saved to output.wav")
else:
    print(f"Error: {result.get('error')}")
```

## Troubleshooting

### Model Loading Errors

- Verify checkpoints path is correct
- Check that `config.yaml` exists in the checkpoints directory
- Ensure all model files are present

### Voice File Not Found

- Verify filename matches exactly (case-sensitive)
- Check file is in `audio_files/` directory
- Ensure file is included in Docker image or mounted volume

### CUDA/GPU Issues

- Verify GPU is available in RunPod
- Check CUDA version compatibility
- Ensure sufficient GPU memory (model may need 8GB+ VRAM)

### Build Errors

- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Ensure IndexTTS2 repository is accessible

## Next Steps

Once basic functionality works, you can:
- Add more voice files to `audio_files/`
- Customize model parameters in the handler
- Add emotion control (see IndexTTS2 documentation)
- Implement batch processing
- Add caching for frequently used voices

