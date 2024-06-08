from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave


def answer(call):
    try:
        f = wave.open("/home/polarbeer/Documents/VoIP/sample2.wav", "rb")
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        print("\ncall answered")

        call.answer()

        # call.read_audio()
        call.write_audio(
            data
        )  # This writes the audio data to the transmit buffer, this must be bytes.

        stop = time.time() + (
            frames / 8000
        )  # frames/8000 is the length of the audio in seconds. 8000 is the hertz of PCMU.

        while time.time() <= stop and call.state == CallState.ANSWERED:
            time.sleep(0.1)
        call.hangup()
        print("\nhung up")
    except InvalidStateError:
        pass
    except:
        call.hangup()


if __name__ == "__main__":
    sip_domain = "sip.ippi.com"
    username = "Asdjkl"
    password = "Aman@123"
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
