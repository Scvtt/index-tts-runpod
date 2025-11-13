# Model Checkpoints Setup Guide

The IndexTTS2 model checkpoints are **required** but not included in this repository due to their large size. You need to set them up separately.

## Quick Setup Options

### Option 1: RunPod Network Volume (Recommended)

This is the easiest and most efficient method for RunPod serverless.

1. **Create a Network Volume in RunPod**
   - Go to RunPod Dashboard → Volumes
   - Click "Create Volume"
   - Give it a name (e.g., `indextts2-checkpoints`)
   - Choose appropriate size (checkpoints are ~5-10GB)

2. **Upload Checkpoints to Volume**
   - Download IndexTTS2 checkpoints from the [official repository](https://github.com/index-tts/index-tts)
   - Upload to your RunPod volume
   - Ensure structure is:
     ```
     checkpoints/
       ├── config.yaml
       ├── model files...
       └── other checkpoint files...
     ```

3. **Mount Volume in Endpoint**
   - When creating/editing your serverless endpoint
   - Add your volume as a mount
   - Set mount path to `/app/checkpoints`
   - Or update `MODEL_DIR` environment variable to match your mount path

### Option 2: Download During Container Startup

You can modify the Dockerfile to download checkpoints at build/startup time if download URLs are available.

**Note**: This will significantly increase build time and image size.

### Option 3: Include in Docker Image (Not Recommended)

You can copy checkpoints into the Docker image, but this creates a very large image (10GB+).

## Environment Variables

You can configure checkpoint paths using environment variables:

- `MODEL_DIR`: Path to checkpoints directory (default: `/app/checkpoints`)
- `CONFIG_PATH`: Path to config.yaml (default: `/app/checkpoints/config.yaml`)

## Verifying Setup

Once checkpoints are mounted, the worker will:
1. Check for `config.yaml` at startup
2. Verify model directory exists
3. Load the model automatically

If checkpoints are missing, you'll see a clear error message with instructions.

## Downloading Checkpoints

Refer to the [IndexTTS2 repository](https://github.com/index-tts/index-tts) for:
- Checkpoint download instructions
- Required files list
- Model structure

## Troubleshooting

### "Model checkpoints not found"
- Verify volume is mounted correctly
- Check mount path matches `MODEL_DIR` environment variable
- Ensure `config.yaml` exists in the mounted directory
- Check volume contents in RunPod dashboard

### "Model directory not found"
- Verify the volume mount path
- Check that the directory structure is correct
- Ensure all model files are present

### Model loads but fails during inference
- Check GPU memory (may need more VRAM)
- Verify all checkpoint files are present
- Check RunPod logs for detailed error messages

## Example Volume Mount Configuration

In RunPod endpoint settings:
- **Volume**: `indextts2-checkpoints` (your volume name)
- **Mount Path**: `/app/checkpoints`
- **Environment Variables**:
  - `MODEL_DIR=/app/checkpoints`
  - `CONFIG_PATH=/app/checkpoints/config.yaml`

This matches the default configuration, so no environment variable changes needed if you mount at `/app/checkpoints`.

