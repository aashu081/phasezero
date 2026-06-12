import soundcard as sc
import numpy as np
import threading

def list_devices():
    print("All the available devices")
    speakers = sc.all_speakers()
    for i, s in enumerate(speakers):
        print(f'[{i}] {s.name}')
    return speakers

def play_audio(speaker, audio_data, samplerate=44100):
    """pushing the audio to a single device"""
    try:
        print(f'[START] {speaker.name}')
        with speaker.player(samplerate=samplerate) as p:
            p.play(audio_data)
        print(f'[DONE]  {speaker.name}')
    except Exception as e:
        print(f'[ERROR] {speaker.name} -> {e}')

def play_in_all(speakerind, audio_data, samplerate=44100):
    """pushing same audio to multiple devices simultaneously"""
    speakers = sc.all_speakers()
    threads = []

    for idx in speakerind:
        speaker = speakers[idx]
        t = threading.Thread(
            target=play_audio,          # ← fixed: function name not speakerind
            args=(speaker, audio_data, samplerate)
        )
        threads.append(t)

    print(f"\nStarting {len(threads)} devices simultaneously\n")
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\nAll devices finished.")

def generate_test_tone(frequency=440, duration=3, samplerate=44100):
    """generate a sine wave to test output"""
    t = np.linspace(0, duration, samplerate * duration)
    tone = np.sin(2 * np.pi * frequency * t)
    tone_stereo = np.column_stack([tone, tone])
    tone_stereo = tone_stereo.astype(np.float32)

    print(f"\nTest tone generated:")
    print(f"  frequency : {frequency}Hz")
    print(f"  duration  : {duration} seconds")
    print(f"  shape     : {tone_stereo.shape}")

    return tone_stereo

if __name__ == "__main__":
    speakers = list_devices()

    print("\nPick 2 devices to test simultaneous output")
    idx1 = int(input("First device index  : "))
    idx2 = int(input("Second device index : "))

    audio_data = generate_test_tone(frequency=440, duration=3)

    print(f"Tone on BOTH devices at same time")
    print(f"If you hear echo = lag exists = Week 2 will fix it")
    print(f"If both play together = perfect\n")

    play_in_all([idx1, idx2], audio_data)