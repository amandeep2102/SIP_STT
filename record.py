from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave
import pyaudio
import threading


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

    frames = []

    try:
        while call.state == CallState.ANSWERED:
            data = stream.read(chunk_size)
            frames.append(data)
            call.read_audio()  # Read audio from call to keep the call alive
            # call.write_audio(data)  # Optionally transmit the same data back
            time.sleep(0.1)
            print("\ndata written")
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
