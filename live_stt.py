from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave
import pyaudio
import speech_recognition as sr
import threading

frames = []


def live_transcribe():
    print("\nstarted Transcribing")
    while True:
        audio_data = sr.AudioData(
            frame_data=b"".join(frames), sample_rate=8000, sample_width=1
        )
        recognizer = sr.Recognizer()

        try:
            print("final result " + recognizer.recognize_whisper(audio_data=audio_data))
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Whisper; {e}")

        time.sleep(1)


def record_audio(filename, call, sample_rate=8000, channels=1, chunk_size=1024):
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

    try:
        while call.state == CallState.ANSWERED:
            data = stream.read(chunk_size)
            frames.append(data)
            call.read_audio()  # Read audio from call to keep the call alive
            # speech = recognizer.listen(call.read_audio())
            # call.write_audio(data)  # Optionally transmit the same data back
            time.sleep(0.1)
            # print("\ndata written")
            # thread2.start()

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

    # Save the recorded data as a WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))


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
        record_audio("recorded_call.wav", call)

        # call.hangup()
        # recording_thread.join()
    except InvalidStateError:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        call.hangup()


def main():
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


if __name__ == "__main__":
    thread1 = threading.Thread(target=main)
    thread2 = threading.Thread(target=live_transcribe)
    thread1.start()
    time.sleep(1)
    thread2.start()
