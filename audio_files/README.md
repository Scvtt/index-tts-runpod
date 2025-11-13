# Audio Files Directory

This directory contains reference audio files used for voice cloning with IndexTTS2.

## File Requirements

- **Format**: WAV (`.wav` extension)
- **Sample Rate**: 16kHz or higher (recommended: 22kHz or 44.1kHz)
- **Channels**: Mono or Stereo (mono recommended)
- **Duration**: Short clips work best (3-10 seconds)
- **Quality**: Clear, single-speaker audio with minimal background noise

## Naming Convention

Name your files to represent the voice/actor. Examples:
- `voice_01.wav`
- `voice_02.wav`
- `actor_name.wav`
- `female_voice.wav`
- `male_voice.wav`

## Usage

When calling the API, reference the file by its filename (including extension):

```json
{
  "input": {
    "text": "Your text here",
    "voice": "voice_01.wav"
  }
}
```

## Adding Files

1. Place your WAV files directly in this directory
2. Ensure files are properly formatted (WAV, correct sample rate)
3. Test with a short text sample to verify quality

## Notes

- Files in this directory will be included in the Docker image
- Keep file sizes reasonable (under 5MB per file recommended)
- Each file represents a unique voice that can be cloned
- The model will use these files as reference for voice characteristics

