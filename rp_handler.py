import runpod
import os
import base64
import tempfile
import subprocess
import shutil
from typing import Dict, Any
from pathlib import Path
from indextts.infer_v2 import IndexTTS2

# Initialize the TTS model (loaded once when worker starts)
MODEL_DIR = os.getenv("MODEL_DIR", "/app/checkpoints")
CONFIG_PATH = os.getenv("CONFIG_PATH", "/app/checkpoints/config.yaml")
AUDIO_FILES_DIR = os.getenv("AUDIO_FILES_DIR", "/app/audio_files")
MODEL_DOWNLOAD_URL = os.getenv("MODEL_DOWNLOAD_URL", "")  # Optional: custom download URL

# Global model instance
tts_model = None
model_downloaded = False


def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a job request to generate speech from text
    
    Expected input:
    {
        "text": "The text to convert to speech",
        "voice": "voice_filename.wav"  # filename in audio_files directory
    }
    
    Returns:
    {
        "audio_base64": "base64_encoded_wav_string",
        "error": null or error message
    }
    """
    try:
        # Get input parameters
        input_data = job.get("input", {})
        text = input_data.get("text")
        voice = input_data.get("voice")
        
        # Validate inputs
        if not text:
            return {"error": "Missing required parameter: text"}
        
        if not voice:
            return {"error": "Missing required parameter: voice"}
        
        # Construct path to voice file
        voice_path = os.path.join(AUDIO_FILES_DIR, voice)
        
        # Check if voice file exists
        if not os.path.exists(voice_path):
            return {"error": f"Voice file not found: {voice_path}"}
        
        # Initialize model if not already loaded
        model = initialize_model()
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            # Generate speech
            print(f"Generating speech for text: {text[:50]}...")
            print(f"Using voice: {voice_path}")
            
            model.infer(
                spk_audio_prompt=voice_path,
                text=text,
                output_path=output_path,
                verbose=False
            )
            
            # Read the generated WAV file and encode to base64
            with open(output_path, "rb") as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            return {
                "audio_base64": audio_base64,
                "error": None
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
    
    except Exception as e:
        error_msg = f"Error processing job: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {
            "error": error_msg,
            "audio_base64": None
        }

def download_model_checkpoints():
    """Download model checkpoints if they don't exist"""
    global model_downloaded
    
    if model_downloaded:
        return True
    
    # Check if model directory exists and has required files
    model_path = Path(MODEL_DIR)
    config_path = Path(CONFIG_PATH)
    
    if config_path.exists() and model_path.exists():
        # Check if directory has model files (not just empty)
        model_files = list(model_path.glob("*.pth")) + list(model_path.glob("*.ckpt"))
        if model_files:
            print(f"Model checkpoints found at {MODEL_DIR}")
            model_downloaded = True
            return True
    
    print(f"Model checkpoints not found. Downloading to {MODEL_DIR}...")
    
    # Create model directory
    model_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Try using git to clone just the checkpoints directory
        # This is the recommended way from IndexTTS2 repository
        print("Attempting to download model checkpoints from IndexTTS2 repository...")
        
        # Use git sparse-checkout to get only checkpoints
        temp_dir = "/tmp/indextts_checkpoints"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        # Clone with sparse checkout
        subprocess.run([
            "git", "clone", "--depth", "1", "--filter=blob:none",
            "--sparse", "https://github.com/index-tts/index-tts.git", temp_dir
        ], check=True, capture_output=True)
        
        subprocess.run([
            "git", "-C", temp_dir, "sparse-checkout", "set", "checkpoints"
        ], check=True, capture_output=True)
        
        # Copy checkpoints to model directory
        source_checkpoints = os.path.join(temp_dir, "checkpoints")
        if os.path.exists(source_checkpoints):
            # Copy all files from source to destination
            for item in os.listdir(source_checkpoints):
                src = os.path.join(source_checkpoints, item)
                dst = os.path.join(MODEL_DIR, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            
            # Clean up temp directory
            shutil.rmtree(temp_dir)
            
            print(f"Model checkpoints downloaded successfully to {MODEL_DIR}")
            model_downloaded = True
            return True
        else:
            print("Warning: checkpoints directory not found in repository")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Git download failed: {e}")
        print("You may need to manually download model checkpoints.")
        print("Please refer to: https://github.com/index-tts/index-tts")
        return False
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("Please ensure model checkpoints are available at:", MODEL_DIR)
        return False


def initialize_model():
    """Initialize the IndexTTS2 model once at worker startup"""
    global tts_model
    
    if tts_model is None:
        # Download model if not present
        if not download_model_checkpoints():
            print("Warning: Model checkpoints may not be available. Continuing anyway...")
            print("If model fails to load, ensure checkpoints are mounted or downloaded.")
        
        print(f"Loading IndexTTS2 model from {MODEL_DIR}...")
        try:
            tts_model = IndexTTS2(
                cfg_path=CONFIG_PATH,
                model_dir=MODEL_DIR,
                use_fp16=False,
                use_cuda_kernel=False,
                use_deepspeed=False
            )
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Please ensure model checkpoints are properly configured.")
            raise
    
    return tts_model


# Initialize model when worker starts
if __name__ == "__main__":
    initialize_model()
    runpod.serverless.start({"handler": handler})

