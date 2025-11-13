# IndexTTS2 Demo UI

A simple web-based interface to test your IndexTTS2 RunPod serverless endpoint.

## Features

- 🎤 Text-to-speech generation via RunPod API
- 🎵 In-browser audio playback
- 📥 Download generated audio files
- ⚙️ Easy configuration via sidebar
- 🔄 Real-time status updates

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Enter API Endpoint**: In the sidebar, enter your RunPod serverless endpoint URL
   - Format: `https://api.runpod.io/v2/YOUR_ENDPOINT_ID/run`

2. **Enter API Key**: Add your RunPod API key (stored in session, not saved)

3. **Enter Text**: Type the text you want to convert to speech

4. **Select Voice**: Enter the voice file name (e.g., `scott.wav`)

5. **Generate**: Click "Generate Speech" and wait for the result

6. **Play Audio**: The generated audio will appear as a player in the browser

7. **Download**: Click the download button to save the audio file

## Configuration

### API Endpoint Format

Your RunPod endpoint URL should look like:
```
https://api.runpod.io/v2/YOUR_ENDPOINT_ID/run
```

You can find your endpoint ID in the RunPod dashboard under your serverless endpoint.

### Voice Files

Enter the exact filename of the voice file that exists in your `audio_files/` directory on the serverless worker. For example:
- `scott.wav`
- `voice_01.wav`
- `actor_name.wav`

## Troubleshooting

### "Request timed out"
- The endpoint may be cold-starting (first request takes longer)
- Try again after a few seconds
- Check that your endpoint is running in RunPod dashboard

### "API Error: 401"
- Check that your API key is correct
- Verify the API key has access to the endpoint

### "API Error: 404"
- Verify the endpoint URL is correct
- Check that the endpoint ID matches your RunPod dashboard

### "No audio data in response"
- Check the RunPod logs for errors
- Verify the voice file name exists in `audio_files/` directory
- Ensure the text input is valid

## Example Request

The UI sends requests in this format:

```json
{
  "input": {
    "text": "Hello, this is a test.",
    "voice": "scott.wav"
  }
}
```

## Development

To modify the UI:

1. Edit `app.py` to change the interface
2. Restart Streamlit to see changes
3. Check Streamlit documentation for customization options

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Requests 2.31.0+
- Active RunPod serverless endpoint

