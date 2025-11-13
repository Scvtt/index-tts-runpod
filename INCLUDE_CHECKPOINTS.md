# Including Checkpoints in Docker Image

You can include the IndexTTS2 model checkpoints directly in the Docker image. This simplifies deployment but has significant trade-offs.

## ⚠️ Important Warnings

- **Large Image Size**: Including checkpoints will create a Docker image of **10GB+**
- **Slow Builds**: Building and pushing large images takes much longer
- **Storage Costs**: Large images consume more registry storage
- **Slower Pulls**: Downloading the image on each cold start takes longer
- **Not Recommended**: RunPod volumes are the preferred method

## When to Include Checkpoints

Consider including checkpoints in the image if:
- You want the simplest deployment (no volume setup)
- You're okay with large image sizes
- Build time is not a concern
- You have sufficient registry storage

## Setup Instructions

### 1. Download Checkpoints

Download the IndexTTS2 model checkpoints following instructions from the [IndexTTS2 repository](https://github.com/index-tts/index-tts).

### 2. Place Checkpoints in Repository

Create a `checkpoints/` directory in your repository root and place the downloaded files:

```
index-tts-runpod/
├── checkpoints/
│   ├── config.yaml
│   ├── model files...
│   └── other checkpoint files...
├── Dockerfile
├── rp_handler.py
└── ...
```

**Important**: The checkpoints directory is already in `.gitignore` by default. If you want to track it in git (not recommended due to size), you'll need to:

```bash
# Force add checkpoints (not recommended for large files)
git add -f checkpoints/
```

### 3. Build the Image

The Dockerfile will automatically copy checkpoints if they exist:

```bash
docker build -t your-registry/indextts2-runpod:latest .
```

### 4. Verify Checkpoints are Included

Check the image size:

```bash
docker images your-registry/indextts2-runpod:latest
```

You should see a large image (10GB+).

### 5. Push to Registry

```bash
docker push your-registry/indextts2-runpod:latest
```

**Note**: Pushing large images can take a long time depending on your connection speed.

## Alternative: Exclude Checkpoints

If you want to exclude checkpoints from the Docker image (recommended), uncomment this line in `.dockerignore`:

```
checkpoints/
```

Then use RunPod volumes as described in `CHECKPOINTS_SETUP.md`.

## Dockerfile Behavior

The Dockerfile includes this line:

```dockerfile
COPY checkpoints/ ./checkpoints/
```

**Important**: 
- If `checkpoints/` exists in your build context, it will be copied into the image
- If `checkpoints/` doesn't exist, the build will fail with an error
- To exclude checkpoints: Comment out the `COPY checkpoints/` line in the Dockerfile
- Then mount checkpoints as a volume in RunPod instead

## Best Practice Recommendation

**Use RunPod Network Volumes** instead of including checkpoints in the image:
- Faster builds
- Smaller images
- Easier updates (update checkpoints without rebuilding)
- Better for production

See `CHECKPOINTS_SETUP.md` for volume setup instructions.

