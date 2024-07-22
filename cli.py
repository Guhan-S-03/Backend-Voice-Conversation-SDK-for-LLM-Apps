import argparse
import pyaudio
from sdk import VoiceBotSDK


class PyAudioInputStream:
    def __init__(self, chunk_size=1024):
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                                  frames_per_buffer=chunk_size)

    def read(self):
        return self.stream.read(self.chunk_size)


class PyAudioOutputStream:
    def __init__(self, chunk_size=1024):
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True,
                                  frames_per_buffer=chunk_size)

    def write(self, data):
        self.stream.write(data)


def main():
    parser = argparse.ArgumentParser(description="VoiceBot SDK CLI")
    parser.add_argument("--stt_api_key", required=True, help="API Key for STT engine")
    parser.add_argument("--tts_api_key", required=True, help="API Key for TTS engine")
    parser.add_argument("--llm_api_key", required=True, help="API Key for LLM engine")
    args = parser.parse_args()

    stt_config = {
        'engine': 'deepgram',
        'api_key': args.stt_api_key
    }

    tts_config = {
        'engine': 'deepgram',
        'api_key': args.tts_api_key
    }

    llm_config = {
        'engine': 'gpt-3.5',
        'api_key': args.llm_api_key,
        'system_prompt': "You are a helpful assistant."
    }

    sdk = VoiceBotSDK(stt_config, tts_config, llm_config)

    input_stream = PyAudioInputStream()
    output_stream = PyAudioOutputStream()

    sdk.run_stream_conversation(input_stream, output_stream)


if __name__ == "__main__":
    main()
