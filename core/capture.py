import soundcard as sc
import numpy as np

def list_devices():
    """Print all speakers available for loopback capture"""
    print("\n=== Available Speakers (Loopback Devices) ===\n")
    speakers = sc.all_speakers()
    for i, s in enumerate(speakers):
        print(f"[{i}] {s.name}")
    return speakers

def capture_system_audio(speaker_index, duration_seconds=5):
    SAMPLE_RATE = 44100

    speakers = sc.all_speakers()
    target_speaker = speakers[speaker_index]

    print(f"\nCapturing from: {target_speaker.name}")
    print(f"Duration: {duration_seconds} seconds")
    print("Play something on your PC now!\n")

    # get loopback mic object directly — no context manager
    mic = sc.get_microphone(
        id=str(target_speaker.name),
        include_loopback=True
    )

    # record directly
    data = mic.record(
        samplerate=SAMPLE_RATE,
        numframes=SAMPLE_RATE * duration_seconds
    )

    print(f"Captured shape: {data.shape}")
    print(f"Max amplitude : {np.max(np.abs(data)):.4f}")

    if np.max(np.abs(data)) < 0.001:
        print("\nWARNING: Audio is silent — make sure something is playing")
    else:
        print("\nSUCCESS: Audio captured correctly")

    return data

if __name__ == "__main__":
    # Step 1 — list all speakers
    speakers = list_devices()

    # Step 2 — pick one
    index = int(input("\nEnter speaker index from list above: "))

    # Step 3 — capture
    audio_data = capture_system_audio(index, duration_seconds=5)

    print(f"\nFirst 5 samples: {audio_data[:5]}")