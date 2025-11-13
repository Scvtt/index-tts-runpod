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
RUN pip install --no-cache-dir -r requirements.txt

# Clone IndexTTS2 repository
RUN git clone https://github.com/index-tts/index-tts.git /app/indextts

# Install IndexTTS2 package
RUN cd /app/indextts && pip install -e .

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

