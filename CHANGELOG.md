# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial release of IndexTTS2 RunPod Serverless Worker
- Zero-shot voice cloning functionality using IndexTTS2
- Serverless handler (`rp_handler.py`) with RunPod integration
- Docker configuration with all required dependencies
- RunPod Hub configuration (`.runpod/hub.json`)
- Automated test suite configuration (`.runpod/tests.json`)
- Comprehensive documentation (README.md, SETUP.md)
- Audio file management system with `audio_files/` directory
- Base64-encoded WAV audio output
- Input validation and error handling
- Environment variable configuration support
- Model initialization with lazy loading
- Temporary file cleanup after processing
- Example test input file
- Project structure documentation

### Technical Details
- Python 3.10 with PyTorch 2.1.0
- CUDA 11.8 support
- RunPod SDK integration
- IndexTTS2 model integration
- FFmpeg and libsndfile support
- GPU-accelerated inference

### Documentation
- README with API usage examples
- Setup guide with deployment instructions
- Audio file requirements documentation
- Troubleshooting guide
- Python and cURL client examples

[1.0.0]: https://github.com/Scvtt/index-tts-runpod/releases/tag/v1.0.0

