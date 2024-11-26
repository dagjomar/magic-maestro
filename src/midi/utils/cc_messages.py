from typing import Optional
import rtmidi
from rtmidi.midiconstants import (
    CONTROL_CHANGE,
)

def send_cc_message(
    port: rtmidi.MidiOut,
    control: int,
    value: int,
    channel: Optional[int] = 0,
) -> None:
    """
    Send a MIDI Control Change message.
    
    Args:
        port: MIDI output port (must be already opened)
        control: CC control number (0-127)
        value: CC value (0-127)
        channel: MIDI channel (0-15), defaults to 0
    
    Raises:
        TypeError: If port is not an opened rtmidi.MidiOut instance
    """
    if not isinstance(port, rtmidi.MidiOut):
        raise TypeError("Port must be an rtmidi.MidiOut instance")
    if not port.is_port_open():
        raise RuntimeError("MIDI port must be opened before sending messages")

    # MIDI CC message format: [status_byte, control, value]
    # status_byte = 0xB0 (176, CONTROL_CHANGE) + channel
    status_byte = CONTROL_CHANGE | channel
    message = [status_byte, control, value]
    port.send_message(message)

def send_volume(port: rtmidi.MidiOut, value: int, channel: int = 0) -> None:
    """
    Send Volume CC message (CC #7)
    Args:
        port: MIDI output port (must be already opened)
        value: Volume value (0-127)
        channel: MIDI channel (0-15)
    """
    send_cc_message(port, control=7, value=value, channel=channel)

def send_expression(port: rtmidi.MidiOut, value: int, channel: int = 0) -> None:
    """
    Send Expression CC message (CC #11)
    Args:
        port: MIDI output port (must be already opened)
        value: Expression value (0-127)
        channel: MIDI channel (0-15)
    """
    send_cc_message(port, control=11, value=value, channel=channel)

def send_modulation(port: rtmidi.MidiOut, value: int, channel: int = 0) -> None:
    """
    Send Modulation CC message (CC #1)
    Args:
        port: MIDI output port (must be already opened)
        value: Modulation value (0-127)
        channel: MIDI channel (0-15)
    """
    send_cc_message(port, control=1, value=value, channel=channel)

def send_pan(port: rtmidi.MidiOut, value: int, channel: int = 0) -> None:
    """
    Send Pan CC message (CC #10)
    Args:
        port: MIDI output port (must be already opened)
        value: Pan value (0=left, 64=center, 127=right)
        channel: MIDI channel (0-15)
    """
    send_cc_message(port, control=10, value=value, channel=channel)