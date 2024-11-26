import rtmidi
from midi.utils import send_volume, send_expression

class MidiManager:
    def __init__(self, port_name="IAC", port_index=None):
        self.midi_out = rtmidi.MidiOut()
        self.available_ports = self.midi_out.get_ports()
        print("Available ports:", self.available_ports)

        if port_name:
            port_index = next((i for i, name in enumerate(self.available_ports) if port_name in name), None)
            if port_index is None:
                raise ValueError(f"No MIDI port found containing name: {port_name}")
        
        if port_index is None:
            port_index = 0  # Default to first available port
            
        self.midi_out.open_port(port_index)

    def send_volume(self, value, channel=0):
        send_volume(self.midi_out, value=value, channel=channel)

    def send_expression(self, value, channel=0):
        send_expression(self.midi_out, value=value, channel=channel)

    def close(self):
        self.midi_out.close_port()
        del self.midi_out

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()