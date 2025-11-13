FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge || true

# Clone IndexTTS2 repository (shallow clone to save space)
RUN git clone --depth 1 --single-branch https://github.com/index-tts/index-tts.git /app/indextts

# Install IndexTTS2 package and clean up unnecessary files
RUN cd /app/indextts && \
    pip install --no-cache-dir -e . && \
    pip cache purge || true && \
    rm -rf /app/indextts/.git && \
    rm -rf /app/indextts/tests /app/indextts/examples /app/indextts/docs /app/indextts/.github /app/indextts/archive 2>/dev/null || true

# Create checkpoints directory (models will be downloaded at runtime)
RUN mkdir -p /app/checkpoints

# Copy application files
COPY rp_handler.py .
COPY audio_files/ ./audio_files/

# Set environment variables
ENV MODEL_DIR=/app/checkpoints
ENV CONFIG_PATH=/app/checkpoints/config.yaml
ENV AUDIO_FILES_DIR=/app/audio_files
ENV PYTHONUNBUFFERED=1

# Expose port (RunPod uses this)
EXPOSE 8000

# Run the handler
CMD ["python", "-u", "rp_handler.py"]

