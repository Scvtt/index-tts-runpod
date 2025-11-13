# Release Notes - v1.0.0

## 🎉 Initial Release

We're excited to announce the first release of **IndexTTS2 RunPod Serverless Worker** - a production-ready serverless implementation of IndexTTS2 text-to-speech synthesis on RunPod's infrastructure.

## ✨ Features

### Core Functionality
- **Zero-Shot Voice Cloning**: Generate natural speech using IndexTTS2 with any reference audio file
- **Simple API**: Clean, straightforward interface - text in, voice filename in, base64 WAV out
- **Serverless Architecture**: Fully serverless deployment on RunPod with automatic scaling
- **Base64 Audio Output**: Audio returned as base64-encoded WAV for easy client-side decoding

### Technical Features
- **Model Initialization**: Efficient single-load model initialization at worker startup
- **Error Handling**: Comprehensive error handling with descriptive error messages
- **Input Validation**: Validates required parameters and file existence before processing
- **Temporary File Management**: Automatic cleanup of temporary files after processing
- **GPU Support**: Optimized for GPU acceleration with CUDA support

## 📦 Components

### Core Files
- **`rp_handler.py`**: Main serverless worker handler implementing the RunPod interface
- **`Dockerfile`**: Production-ready Docker configuration with all dependencies
- **`requirements.txt`**: Python dependencies including RunPod SDK and IndexTTS2
- **`.runpod/hub.json`**: RunPod Hub listing configuration
- **`.runpod/tests.json`**: Automated test configuration for validation

### Configuration
- **Environment Variables**: Configurable paths for model, config, and audio files
- **Standard Preset**: Pre-configured environment settings for easy deployment
- **Test Suite**: Two test cases (basic and long text) for validation

### Documentation
- **README.md**: Comprehensive documentation with API examples
- **SETUP.md**: Detailed setup guide for deployment
- **audio_files/README.md**: Audio file requirements and usage guide

## 🚀 Getting Started

### Prerequisites
- RunPod account with serverless access
- IndexTTS2 model checkpoints (download separately)
- Reference audio files in WAV format

### Quick Start
1. Add reference audio files to `audio_files/` directory
2. Configure model checkpoints (mount volume or include in image)
3. Deploy to RunPod Serverless via GitHub integration or Docker registry
4. Use the API with text and voice filename parameters

## 📡 API Specification

### Input Format
```json
{
  "input": {
    "text": "The text you want to convert to speech",
    "voice": "voice_filename.wav"
  }
}
```

### Success Response
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

## 🔧 Technical Details

### Environment Variables
- `MODEL_DIR`: Path to IndexTTS2 model checkpoints (default: `/app/checkpoints`)
- `CONFIG_PATH`: Path to config.yaml file (default: `/app/checkpoints/config.yaml`)
- `AUDIO_FILES_DIR`: Path to reference audio files (default: `/app/audio_files`)

### Docker Configuration
- **Base Image**: `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel`
- **Container Disk**: 20GB
- **System Dependencies**: ffmpeg, libsndfile1
- **Python Dependencies**: RunPod SDK, PyTorch, IndexTTS2, and supporting libraries

### GPU Requirements
- **Recommended**: NVIDIA RTX A5000, RTX A6000, A100, or A40
- **Minimum VRAM**: 8GB
- **CUDA Versions**: 11.8, 12.0, 12.1

## 📝 Audio File Requirements

- **Format**: WAV (`.wav` extension)
- **Sample Rate**: 16kHz or higher (22kHz or 44.1kHz recommended)
- **Channels**: Mono or Stereo (mono recommended)
- **Duration**: Short clips work best (3-10 seconds)
- **Quality**: Clear, single-speaker audio with minimal background noise

## 🎯 Use Cases

- Voice cloning for content creation
- Text-to-speech for applications and services
- Multi-voice TTS systems
- Audio content generation
- Accessibility applications

## ⚠️ Known Limitations

- Model checkpoints must be provided separately (not included in repository)
- Requires GPU with sufficient VRAM (8GB+ recommended)
- Reference audio files must be in WAV format
- Model initialization happens at worker startup (cold start latency)

## 🔗 Links

- **RunPod Hub**: [View on RunPod Hub](https://console.runpod.io/hub/Scvtt/index-tts-runpod)
- **IndexTTS2 Repository**: [GitHub](https://github.com/index-tts/index-tts)
- **RunPod Documentation**: [Serverless Overview](https://docs.runpod.io/serverless/overview)

## 📄 License

This project uses IndexTTS2. Please refer to the [IndexTTS2 repository](https://github.com/index-tts/index-tts) for license information.

## 🙏 Acknowledgments

Built on top of:
- [IndexTTS2](https://github.com/index-tts/index-tts) by the IndexTTS team
- [RunPod](https://www.runpod.io/) serverless infrastructure
- Open source TTS community

---

**Release Date**: 2025-01-XX  
**Version**: 1.0.0  
**Status**: Stable

