import numpy as np
import sounddevice as sd


class SoundOutput:
    def __init__(self, sound_buffer, custom_output_name=False):
        # Shared buffer of audio to play
        self.sound_buffer = sound_buffer

        self.t_global = 0

        # If the custom output isn't selected it will default
        # TODO
        # This is tested on windows so the names may vary based on instillation for now
        # I would allow passing custom input names in but thats frankly just annoying to type when running so I dont want to
        if custom_output_name:
            device_name = ["VB", "Cable"]
            self.device_index = self.find_device(device_name)
            print(f"Using output #{self.device_index}: {device_name}")
        else:
            self.device_index = None
            default_output_index = sd.default.device[1]  # (input, output)
            default_output_info = sd.query_devices(default_output_index)
            print(f"Using default output #{default_output_index}: {default_output_info['name']}")
        return

    def find_device(self, name):
        for i, dev in enumerate(sd.query_devices()):
            if all(n in dev['name'] for n in name) and dev['max_output_channels'] >= 2:
                return i
        raise RuntimeError(f"Device '{name}' not found")

    def callback(self, outdata, frames, time, status):
        """
        outdata:
            - A preallocated NumPy array you must fill with shape (frames, channels). This becomes the actual audio output.
        frames:
            - How many audio frames (samples) you must provide (e.g., 480 if block size = 480).
        time:
            - Contains timing info; you usually don't need it.
        status:
            - Reports underflow, overflow, etc.
        """

        t = (np.arange(frames) + self.t_global * frames) / self.sound_buffer.samplerate
        self.t_global += 1

        with self.sound_buffer.lock:
            if status:
                self.sound_buffer.status.append(status)
                print(status)
            if self.sound_buffer.compute_buffer is not None:
                x, y, z = self.sound_buffer.compute_buffer(t)
            else:
                x = y = np.zeros_like(t)

        outdata[:] = np.column_stack([x, y])
        return

    def run(self):
        with sd.OutputStream(
            device=self.device_index,
            samplerate=self.sound_buffer.samplerate,
            channels=2,
            callback=self.callback,
            blocksize=self.sound_buffer.blocksize,
        ):
            while True:
                pass
        return
