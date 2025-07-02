import sys
import threading
import graphics, sound_output

class SoundBuffer:
    def __init__(self, samplerate=48000, blocksize=480):
        # To ensure safe read/write between UI and output (across threads)
        self.lock = threading.Lock()
        
        # The buffer for the audio output
        self.compute_buffer = None
        # Updates to status such as {over, under}full
        self.status = []

        # Finall output audio details
        self.samplerate = samplerate
        self.blocksize = blocksize
        return


def run():
    # Flags
    custom_output_name = False
    if '-c' in sys.argv:
        custom_output_name = True

    # Create the shared frame/sound buffer between UI and sound
    shared_buffer = SoundBuffer()

    # Create and start a thread for audio
    audio = sound_output.SoundOutput(shared_buffer, custom_output_name=custom_output_name)
    audio_thread = threading.Thread(target=audio.run, daemon=True)
    audio_thread.start()

    # Start UI
    graphics.run(shared_buffer)
    return


if __name__ == "__main__":
    run()

