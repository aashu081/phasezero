import sounddevice as sd
import numpy as np

def list_devices():
    """Print all audio devices with their IDs"""
    devices = sd.query_devices()
    print("\n=== Available Audio Devices ===\n")
    for i, d in enumerate(devices):
        in_ch = d['max_input_channels']
        out_ch = d['max_output_channels']
        print(f"[{i}] {d['name']}")
        print(f"     in: {in_ch} ch | out: {out_ch} ch")
        print()

def find_loopback_device():
    """Find the default output device for loopback capture"""
    default = sd.query_devices(kind='output')
    print(f"Default output device: {default['name']}")
    return default

def capture_system_audio(device_id, duration_seconds=5):
    """
    Capture whatever is playing on your system right now
    device_id: ID of your speaker/output device
    """
    SAMPLE_RATE = 44100
    CHANNELS = 2
    BLOCK_SIZE = 1024

    print(f"\nCapturing system audio for {duration_seconds} seconds...")
    print("Play something on your PC now!\n")

    captured_chunks = []

    def callback(indata, frames, time, status):
        if status:
            print(f"Status: {status}")
        # indata is a numpy array — this is your raw audio
        captured_chunks.append(indata.copy())
        print(f"Captured chunk — shape: {indata.shape}, "
              f"max amplitude: {np.max(np.abs(indata)):.4f}")

    with sd.InputStream(
        device=device_id,
        channels=CHANNELS,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        loopback=True,           # WASAPI loopback — captures system audio
        callback=callback
    ):
        sd.sleep(duration_seconds * 1000)

    print(f"\nDone. Captured {len(captured_chunks)} chunks.")
    return captured_chunks


if __name__ == "__main__":
    # Step 1 — see all devices
    list_devices()

    # Step 2 — find your default output
    default = find_loopback_device()

    # Step 3 — get device ID from user
    device_id = int(input("\nEnter the device ID of your speakers from the list above: "))

    # Step 4 — capture for 5 seconds
    chunks = capture_system_audio(device_id, duration_seconds=5)