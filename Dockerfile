FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clone IndexTTS2 repository with Git LFS
RUN git clone https://github.com/index-tts/index-tts.git /app/indextts && \
    cd /app/indextts && \
    git lfs pull && \
    pip install -e .

# Copy checkpoints from the cloned repository
RUN if [ -d "/app/indextts/checkpoints" ]; then \
        echo "Copying checkpoints from IndexTTS2 repository..."; \
        mkdir -p /app/checkpoints && \
        cp -r /app/indextts/checkpoints/* /app/checkpoints/; \
        echo "Checkpoints copied successfully"; \
    else \
        echo "Warning: checkpoints not found in repository. You may need to mount as volume."; \
        mkdir -p /app/checkpoints; \
    fi

# Copy application files
COPY rp_handler.py .
COPY audio_files/ ./audio_files/

# Checkpoints are downloaded via Git LFS from the IndexTTS2 repository above
# If you have local checkpoints you want to use instead, uncomment the line below:
# COPY checkpoints/ ./checkpoints/

# Set environment variables
ENV MODEL_DIR=/app/checkpoints
ENV CONFIG_PATH=/app/checkpoints/config.yaml
ENV AUDIO_FILES_DIR=/app/audio_files
ENV PYTHONUNBUFFERED=1

# Expose port (RunPod uses this)
EXPOSE 8000

# Run the handler
CMD ["python", "-u", "rp_handler.py"]

