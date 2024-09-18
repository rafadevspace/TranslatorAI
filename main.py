import gradio as gr
import whisper
from translate import Translator
from dotenv import dotenv_values
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import ssl
import urllib.request


config = dotenv_values(".env")

ELEVENLABS_API_KEY = config["ELEVENLABS_API_KEY"]

# Deshabilitar verificación SSL (solo para desarrollo)
ssl._create_default_https_context = ssl._create_unverified_context


def translator(audio_file):

    # 1.Transcribir Texto 

    # Se usara Whisper: #https://github.com/openai/whisper
    # Alternativa API Online: https://www.assemblyai.com

    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file, language="Spanish", fp16=False)
        transcription = result["text"]
    except Exception as e:
        raise gr.Error(
            f"Se ha producido un error transcribiendo el texto: {str(e)}")

    
    print(f"Texto original: {transcription}")

    # 2. Traducir texto
    # Se usara translate: https://github.com/terryyin/translate-python
    try:
        en_transcription = Translator(
            from_lang="es", to_lang="en").translate(transcription)
        it_transcription = Translator(
            from_lang="es", to_lang="it").translate(transcription)
        fr_transcription = Translator(
            from_lang="es", to_lang="fr").translate(transcription)
        ja_transcription = Translator(
            from_lang="es", to_lang="ja").translate(transcription)
    except Exception as e:
        raise gr.Error(
            f"Se ha producido un error traduciendo el texto: {str(e)}")

    print(f"Texto traducido a Inglés: {en_transcription}")
    print(f"Texto traducido a Italiano: {it_transcription}")
    print(f"Texto traducido a Francés: {fr_transcription}")
    print(f"Texto traducido a Japonés: {ja_transcription}")


    # 3. Generar audio traducido

    # Usamos Elevenlabs IO: https://elevenlabs.io/docs/api-reference/getting-started

    en_save_file_path = text_to_speach(en_transcription, "en")
    it_save_file_path = text_to_speach(it_transcription, "it")
    fr_save_file_path = text_to_speach(fr_transcription, "fr")
    ja_save_file_path = text_to_speach(ja_transcription, "ja")

    return en_save_file_path, it_save_file_path, fr_save_file_path, ja_save_file_path

def text_to_speach(text: str, language: str) -> str:

    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=0.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        save_file_path = f"audios/{language}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

    except Exception as e:
        raise gr.Error(
            f"Se ha producido un error creando el audio: {str(e)}")

    return save_file_path


web = gr.Interface(
    fn=translator,
    inputs=gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="Español"
    ),
    outputs=[gr.Audio(label="Inglés"),
        gr.Audio(label="Italiano"),
        gr.Audio(label="Francés"),
        gr.Audio(label="Japonés")
    ],
    title="Traductor de voz",
    description="Traductor de voz con AI a varios idiomas"
)

web.launch()