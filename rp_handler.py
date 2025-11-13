import runpod
import os
import base64
import tempfile
from typing import Dict, Any
from indextts.infer_v2 import IndexTTS2

# Initialize the TTS model (loaded once when worker starts)
MODEL_DIR = os.getenv("MODEL_DIR", "checkpoints")
CONFIG_PATH = os.getenv("CONFIG_PATH", "checkpoints/config.yaml")
AUDIO_FILES_DIR = os.getenv("AUDIO_FILES_DIR", "audio_files")

# Global model instance
tts_model = None


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

def initialize_model():
    """Initialize the IndexTTS2 model once at worker startup"""
    global tts_model
    if tts_model is None:
        print(f"Loading IndexTTS2 model from {MODEL_DIR}...")
        tts_model = IndexTTS2(
            cfg_path=CONFIG_PATH,
            model_dir=MODEL_DIR,
            use_fp16=False,
            use_cuda_kernel=False,
            use_deepspeed=False
        )
        print("Model loaded successfully!")
    return tts_model


# Initialize model when worker starts
if __name__ == "__main__":
    initialize_model()
    runpod.serverless.start({"handler": handler})

