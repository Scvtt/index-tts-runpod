"""
Simple Web UI for IndexTTS2 RunPod Serverless Worker
A Streamlit-based interface to test the TTS API and play generated audio
"""

import streamlit as st
import requests
import base64
import io
import time

# Page configuration
st.set_page_config(
    page_title="IndexTTS2 Demo",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 IndexTTS2 Text-to-Speech Demo")
st.markdown("Test your RunPod serverless endpoint and generate speech from text")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Endpoint input
    api_endpoint = st.text_input(
        "RunPod API Endpoint",
        placeholder="https://api.runpod.io/v2/YOUR_ENDPOINT_ID/run",
        help="Your RunPod serverless endpoint URL"
    )
    
    api_key = st.text_input(
        "API Key",
        type="password",
        help="Your RunPod API key"
    )
    
    st.divider()
    st.markdown("### 📝 Instructions")
    st.markdown("""
    1. Enter your RunPod endpoint URL
    2. Enter your API key
    3. Type the text you want to convert
    4. Select a voice file
    5. Click 'Generate Speech'
    6. Play the audio in the browser
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Input")
    
    # Text input
    text_input = st.text_area(
        "Text to Convert",
        height=150,
        placeholder="Enter the text you want to convert to speech...",
        help="The text that will be synthesized into speech"
    )
    
    # Voice selection
    voice_file = st.text_input(
        "Voice File",
        value="scott.wav",
        help="Name of the voice file in the audio_files directory (e.g., scott.wav)"
    )

with col2:
    st.header("🎵 Output")
    
    # Status placeholder
    status_placeholder = st.empty()
    audio_placeholder = st.empty()

# Generate button
if st.button("🚀 Generate Speech", type="primary", use_container_width=True):
    # Validation
    if not api_endpoint:
        st.error("❌ Please enter your RunPod API endpoint")
    elif not api_key:
        st.error("❌ Please enter your API key")
    elif not text_input:
        st.error("❌ Please enter text to convert")
    elif not voice_file:
        st.error("❌ Please enter a voice file name")
    else:
        # Show loading state
        with status_placeholder:
            with st.spinner("🔄 Generating speech..."):
                try:
                    # Prepare request
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    }
                    
                    payload = {
                        "input": {
                            "text": text_input,
                            "voice": voice_file
                        }
                    }
                    
                    # Make API request
                    start_time = time.time()
                    response = requests.post(
                        api_endpoint,
                        json=payload,
                        headers=headers,
                        timeout=300  # 5 minute timeout
                    )
                    elapsed_time = time.time() - start_time
                    
                    # Check response
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Check for errors in response
                        if "error" in result and result["error"]:
                            st.error(f"❌ Error: {result['error']}")
                        elif "output" in result:
                            output = result["output"]
                            if "error" in output and output["error"]:
                                st.error(f"❌ Error: {output['error']}")
                            elif "audio_base64" in output and output["audio_base64"]:
                                # Decode base64 audio
                                audio_data = base64.b64decode(output["audio_base64"])
                                
                                # Show success message
                                st.success(f"✅ Speech generated successfully! (took {elapsed_time:.2f}s)")
                                
                                # Display audio player
                                st.audio(audio_data, format="audio/wav")
                                
                                # Download button
                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_data,
                                    file_name=f"generated_speech_{int(time.time())}.wav",
                                    mime="audio/wav"
                                )
                            else:
                                st.error("❌ No audio data in response")
                        else:
                            st.error("❌ Unexpected response format")
                            st.json(result)
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        try:
                            error_detail = response.json()
                            st.json(error_detail)
                        except:
                            st.text(response.text)
                            
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. The endpoint may be cold-starting or processing.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Request failed: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    st.exception(e)

# Footer
st.divider()
st.markdown("""
### ℹ️ About
This demo connects to your RunPod serverless endpoint running IndexTTS2.
Make sure your endpoint is running and accessible before testing.

**Note**: The first request may take longer due to cold starts.
""")

