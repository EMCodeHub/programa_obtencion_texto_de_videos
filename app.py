import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
import os

def video_to_audio(video_file, audio_file):
    # Extraer el audio del video
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)

def audio_to_text(audio_file, text_file):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    chunks = audio[::60000]  # Dividir en partes de 60 segundos

    with open(text_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            chunk_file = f"chunk{i}.wav"
            chunk.export(chunk_file, format="wav")
            with sr.AudioFile(chunk_file) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="es-ES")
                    print(f"Texto reconocido en chunk {i}: {text}")  # Imprime el texto reconocido para depuración
                    f.write(text + "\n")  # Escribir texto en archivo, agregar salto de línea
                except sr.UnknownValueError:
                    print("Google Speech Recognition no pudo entender el audio")
                except sr.RequestError as e:
                    print(f"Error al solicitar los resultados del servicio de Google Speech Recognition; {e}")
            os.remove(chunk_file)

def extract_text_from_video(video_file, text_file):
    audio_file = "temp_audio.wav"
    video_to_audio(video_file, audio_file)
    audio_to_text(audio_file, text_file)
    os.remove(audio_file)

if __name__ == "__main__":
    video_file = "C:\\Users\\edume\\OneDrive\\Escritorio\\programa audio2\\video.mp4"  # Ruta completa al archivo de video
    text_file = "C:\\Users\\edume\\OneDrive\\Escritorio\\programa audio2\\texto_extraido.txt"
    extract_text_from_video(video_file, text_file)
    print(f"El texto hablado del video se ha guardado en {text_file}")
