# IndexTTS2 RunPod Serverless Worker

A serverless RunPod worker for IndexTTS2 text-to-speech synthesis. This worker accepts text and a voice filename, then returns base64-encoded WAV audio.

## Features

- Zero-shot voice cloning using IndexTTS2
- Simple API: text in, voice filename in, base64 WAV out
- Reference audio files stored in `audio_files/` directory
- Serverless deployment on RunPod

## Project Structure

```
.
├── handler.py           # Main worker handler
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── audio_files/         # Reference audio files (WAV format)
│   └── .gitkeep
└── README.md
```

## Setup

### 1. Add Reference Audio Files

Place your reference audio files (WAV format) in the `audio_files/` directory. Each file represents a voice/actor that can be used for synthesis.

Example:
```
audio_files/
  ├── voice_01.wav
  ├── voice_02.wav
  └── actor_name.wav
```

### 2. Download Model Checkpoints

You need to download the IndexTTS2 model checkpoints. The model expects:
- `checkpoints/config.yaml`
- Model files in `checkpoints/` directory

**Note:** You'll need to download these separately and either:
- Mount them as a volume in RunPod
- Include them in the Docker image (if size allows)
- Use RunPod's network volumes

### 3. Build and Deploy

#### Option A: GitHub Integration (Recommended)

1. Push this repository to GitHub
2. In RunPod Serverless, create a new template
3. Connect your GitHub repository
4. Configure the build settings:
   - Dockerfile path: `Dockerfile`
   - Build context: `.`
   - Environment variables (if needed):
     - `MODEL_DIR`: Path to model checkpoints (default: `/app/checkpoints`)
     - `CONFIG_PATH`: Path to config file (default: `/app/checkpoints/config.yaml`)
     - `AUDIO_FILES_DIR`: Path to audio files (default: `/app/audio_files`)

#### Option B: Manual Docker Build

```bash
# Build the image
docker build -t indextts2-runpod:latest .

# Tag for your registry
docker tag indextts2-runpod:latest your-registry/indextts2-runpod:latest

# Push to registry
docker push your-registry/indextts2-runpod:latest
```

Then create a template in RunPod pointing to your registry image.

## API Usage

### Input Format

```json
{
  "input": {
    "text": "The text you want to convert to speech",
    "voice": "voice_01.wav"
  }
}
```

### Output Format

```json
{
  "audio_base64": "base64_encoded_wav_string",
  "error": null
}
```

### Error Response

```json
{
  "error": "Error message here",
  "audio_base64": null
}
```

## Example Usage

### Python Client

```python
import runpod
import base64

# Set your API key
runpod.api_key = "your-api-key"

# Create a job
job = runpod.submit_job(
    endpoint_id="your-endpoint-id",
    input={
        "text": "Hello, this is a test of IndexTTS2.",
        "voice": "voice_01.wav"
    }
)

# Wait for result
result = runpod.wait_for_output(job)

# Decode and save audio
if result.get("audio_base64"):
    audio_data = base64.b64decode(result["audio_base64"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    print("Audio saved to output.wav")
else:
    print(f"Error: {result.get('error')}")
```

### cURL

```bash
curl -X POST https://api.runpod.io/v2/your-endpoint-id/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "text": "Hello, this is a test.",
      "voice": "voice_01.wav"
    }
  }'
```

## Model Checkpoints

You need to download the IndexTTS2 model checkpoints separately. Refer to the [IndexTTS2 repository](https://github.com/index-tts/index-tts) for instructions on downloading the model files.

The model files should be placed in the `checkpoints/` directory or mounted as a volume in RunPod.

## Audio File Requirements

- Format: WAV
- Recommended: 16kHz or higher sample rate
- Duration: Short reference clips work best (a few seconds)
- Quality: Clear, single speaker audio

## Environment Variables

- `MODEL_DIR`: Path to model checkpoints (default: `/app/checkpoints`)
- `CONFIG_PATH`: Path to config.yaml (default: `/app/checkpoints/config.yaml`)
- `AUDIO_FILES_DIR`: Path to audio files directory (default: `/app/audio_files`)

## Troubleshooting

### Model Not Found
Ensure model checkpoints are properly mounted or included in the container.

### Voice File Not Found
Check that the voice filename matches exactly (case-sensitive) and is in the `audio_files/` directory.

### CUDA Out of Memory
The model may require significant GPU memory. Consider using a GPU with more VRAM or adjusting batch sizes.

## License

This project uses IndexTTS2. Please refer to the [IndexTTS2 repository](https://github.com/index-tts/index-tts) for license information.

## References

- [IndexTTS2 Repository](https://github.com/index-tts/index-tts)
- [RunPod Serverless Documentation](https://docs.runpod.io/serverless/overview)
- [RunPod Worker Template](https://github.com/runpod-workers/worker-template)

