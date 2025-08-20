# Installation

## Digital Oscilloscope
If you are using [sosci](https://osci-render.com/sosci/) or a similar enumerator for an Oscilloscope, install [VB-Cable Virtual Audio Device](https://vb-audio.com/Cable/). Use the default device name, or update the device selection logic in `sound_output.py` to match your configuration. 

Pass the `-c` flag to enable custom audio output into the [Virtual Cable](https://vb-audio.com/Cable/).
```
python .\main.py -c
```
This switches the output from the default device output to the internal cable to route back to [sosci](https://osci-render.com/sosci/). Ensure you change and enable the audio input in [sosci](https://osci-render.com/sosci/) (the microphone icon below the display).

## Analog Oscilloscope
You will need some additional hardware to connect to an analog oscilloscope. Aside from an oscilloscope itself you also will need an audio interface is useful as the output of most computers isn't strong enough to show up. Ensure it has an option to be DC. Likely various cords and adapters to connect these as well.

[Here is a helpful video talking about getting started with 'Oscilloscope Music'.](https://www.youtube.com/watch?v=1YdpCH9v5Kk)

# Usage
Broadly this project allows you to create custom waveforms by adding and or multiplying various waveforms supported by binding variables to parameters. These are then assigned to X, Y, Z of a shape.

## Hotkeys

| Input            | Action                                      |
|------------------|---------------------------------------------|
| Esc (twice)      | Quit                                        |
| r                | Return to root                              |
| w                | Add a waveform to the selected node         |
| a                | Add a new collection to the selected node   |
| Tab              | Toggle the mode of the selected node        |
| Enter            | Edit the value of a selected parameter      |
| Arrow keys       | Navigate the tree                           |
| /                | Collapse selected node                      |
| ?                | Collapse all nodes                          |
| S                | Select                                      |
| x                | Bind variable                               |
| Shift+Tab        | Toggle variable menu                        |
| v (in variable)  | Add variable                                |

- Shift+Tab switches between the data tree and variable menu, and each has its respective indices that remain active on both trees.
- In the variable menu, use 'a' to add a variable, then in the data tree when selecting a node 'x' to bind the variable currently selected in the varaible menu.
- Press Enter to edit numeric values.
