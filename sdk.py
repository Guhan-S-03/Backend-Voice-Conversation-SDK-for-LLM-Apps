import time
from io import BytesIO
import openai
import asyncio
import Deepgram
class VoiceBotSDK:
    def __init__(self, stt_config, tts_config, llm_config):
        self.stt_engine = stt_config['engine']
        self.stt_api_key = stt_config['api_key']
        self.tts_engine = tts_config['engine']
        self.tts_api_key = tts_config['api_key']
        self.llm_engine = llm_config['engine']
        self.llm_api_key = llm_config['api_key']
        self.system_prompt = llm_config['system_prompt']

        self.deepgram_client = Deepgram(self.stt_api_key)
        openai.api_key = self.llm_api_key

    async def transcribe_audio(self, audio_data):
        try:
            response = await self.deepgram_client.transcription.prerecorded({
                'buffer': audio_data,
                'mimetype': 'audio/wav'
            }, {
                'punctuate': True
            })
            return response['results']['channels'][0]['alternatives'][0]['transcript']
        except Exception as e:
            print(f"Error in transcribing audio: {e}")
            return None

    async def synthesize_text(self, text):
        if self.tts_engine == "deepgram":
            raise NotImplementedError("Deepgram TTS not implemented in SDK version 3")
        else:
            try:
                response = openai.Audio.create(
                    model="text-to-speech-001",
                    prompt=text,
                    voice="default"
                )
                return BytesIO(response['audio_content'])
            except Exception as e:
                print(f"Error in synthesizing text: {e}")
                return None

    async def stream_conversation(self, input_stream, output_stream):
        stt_start_time = time.time()

        audio_data = input_stream.read()
        stt_text = await self.transcribe_audio(audio_data)
        stt_end_time = time.time()

        if stt_text is None:
            print("STT failed, aborting conversation.")
            return

        llm_start_time = time.time()
        try:
            response = openai.Completion.create(
                engine=self.llm_engine,
                prompt=f"{self.system_prompt}\n\nUser: {stt_text}\nBot:",
                max_tokens=150
            )
            llm_text = response.choices[0].text.strip()
        except Exception as e:
            print(f"Error in LLM response: {e}")
            llm_text = "Sorry, I didn't understand that."
        llm_end_time = time.time()

        tts_start_time = time.time()
        audio_output = await self.synthesize_text(llm_text)
        if audio_output is None:
            print("TTS failed, aborting.")
            return

        tts_end_time = time.time()

        output_stream.write(audio_output.read())

        print(f"STT Time: {stt_end_time - stt_start_time} seconds")
        print(f"LLM Response Time: {llm_end_time - llm_start_time} seconds")
        print(f"TTS Generation Time: {tts_end_time - tts_start_time} seconds")
        print(f"Total Time: {tts_end_time - stt_start_time} seconds")

    def run_stream_conversation(self, input_stream, output_stream):
        asyncio.run(self.stream_conversation(input_stream, output_stream))
