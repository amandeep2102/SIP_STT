from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave
import pyaudio
import speech_recognition as sr
from os import path
import threading


def transcribe_audio(frames):
    recognizer = sr.Recognizer()
    source = sr.AudioData(b"".join(frames), 8000, 1)
    try:
        print("final result " + recognizer.recognize_whisper(source))
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Whisper; {e}")


def recorded_stt(filename, call, sample_rate=8000, channels=1, chunk_size=1024):
    # Initialize pyaudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    print("\nRecording started")

    frames = []

    try:
        while call.state == CallState.ANSWERED:
            data = stream.read(chunk_size)
            frames.append(data)
            call.read_audio()  # Read audio from call to keep the call alive
            # call.write_audio(data)  # Optionally transmit the same data back
            time.sleep(0.1)
            # print("\ndata written")

    except InvalidStateError:
        print("invalid state")
        pass
    except Exception as e:
        print(f"An error occurred during recording: {e}")

    print("\nRecording stopped")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    transcribe_audio(frames=frames)


def answer(call):
    try:
        call.answer()
        print("\nCall answered")

        # recording_thread = threading.Thread(
        # target=record_audio, args=("recorded_call.wav", call)
        # )
        # recording_thread.start()
        # while call.state == CallState.ANSWERED:
        # call.read_audio()
        # time.sleep(0.1)

        # Start recording audio in a separate thread or process
        recorded_stt("recorded_call.wav", call)

        # call.hangup()
        # recording_thread.join()
    except InvalidStateError:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        call.hangup()


if __name__ == "__main__":
    # sip_domain = "sip.ippi.com"
    # username = "Asdjkl"
    # password = "Aman@123"
    sip_domain = "sip.zadarma.com"
    username = "765249"
    password = "r7mTE2au3d"
    phone = VoIPPhone(
        server=sip_domain,
        username=username,
        password=password,
        myIP="192.168.29.61",
        port=5060,
        callCallback=answer,
    )
    phone.start()
    input("Press enter to disable the phone")
    phone.stop()

    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "recorded_call.wav")
    # recognizer = sr.Recognizer()
    # with sr.AudioFile(AUDIO_FILE) as source:
    #     fin_audio = recognizer.record(source=source)

    # try:
    #     print("final result " + recognizer.recognize_whisper(fin_audio))
    # except sr.UnknownValueError:
    #     print("Whisper could not understand audio")
    # except sr.RequestError as e:
    #     print(f"Could not request results from Whisper; {e}")
