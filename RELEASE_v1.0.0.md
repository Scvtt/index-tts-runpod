# 🎉 IndexTTS2 RunPod Serverless Worker v1.0.0

## Initial Release

The first stable release of IndexTTS2 RunPod Serverless Worker - a production-ready serverless implementation for zero-shot text-to-speech synthesis.

## ✨ What's New

### Core Features
- ✅ Zero-shot voice cloning with IndexTTS2
- ✅ Simple API: text + voice filename → base64 WAV audio
- ✅ Serverless deployment on RunPod
- ✅ Automatic scaling and GPU acceleration
- ✅ Comprehensive error handling

### Technical Highlights
- 🐳 Production-ready Docker configuration
- 🔧 Configurable environment variables
- 📝 Full documentation and setup guides
- 🧪 Automated test suite
- 🎯 RunPod Hub integration

## 🚀 Quick Start

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
```

## 📦 What's Included

- **Handler Script**: `rp_handler.py` - Main serverless worker
- **Docker Configuration**: Production-ready container setup
- **Hub Configuration**: RunPod Hub listing ready
- **Test Suite**: Automated validation tests
- **Documentation**: Complete setup and usage guides

## 📋 Requirements

- RunPod account with serverless access
- IndexTTS2 model checkpoints (download separately)
- Reference audio files (WAV format)
- GPU with 8GB+ VRAM recommended

## 🔗 Links

- [RunPod Hub Listing](https://console.runpod.io/hub/Scvtt/index-tts-runpod)
- [IndexTTS2 Repository](https://github.com/index-tts/index-tts)
- [Documentation](README.md)

## 📄 Full Release Notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for complete details.

---

**Installation**: Deploy via RunPod Hub or GitHub integration  
**Support**: Check README.md for troubleshooting  
**License**: See IndexTTS2 repository for license information

