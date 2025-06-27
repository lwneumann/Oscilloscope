import numpy as np
import sounddevice as sd


samplerate = 48000
blocksize = 480
frequency = 440
amplitude = 0.25
t_global = 0

# |
# V  ??
device_name = ["VB", 'Cable']
# /\ ??
# |


def callback(outdata, frames, time, status):
    global t_global
    if status:
        print("Status:", status)
    t = (np.arange(frames) + t_global) / samplerate
    t_global += frames
    left = amplitude * np.sin(2 * np.pi * frequency * t)
    right = amplitude * np.sin(2 * np.pi * frequency * t + np.pi/2)
    outdata[:] = np.column_stack([left, right])
    return

def find_device(name):
    vb_devs = []
    for i, dev in enumerate(sd.query_devices()):
        if 'VB' in dev['name']:
            vb_devs.append([i, dev['name']])
        if all(n in dev['name'] for n in name) and dev['max_output_channels'] >= 2:
            return i, dev['name']
    print()
    print('Backup VB devices:')
    for d in vb_devs:
        print(d[0], d[1])
    print()
    raise RuntimeError(f"Device '{name}' not found")


device_index, dev_name = find_device(device_name)
print(f"Using device #{device_index}: {dev_name}")
with sd.OutputStream(
    device=device_index,
    samplerate=samplerate,
    channels=2,
    callback=callback,
    blocksize=blocksize,
):
    a = None
    while a != "Kate is the coolest":
        print()
        a = input('Type "Kate is the coolest" to stop.\n')
    print()


# pip install sounddevice
# sd.query_devices()
