
from enum import IntFlag
from typing import TYPE_CHECKING, Any, Callable, List, NewType, Optional

from ._ffi import alsa, ffi
from .address import Address, AddressType
from .exceptions import Error, StateError
from .util import _check_alsa_error

if TYPE_CHECKING:
    from .client import SequencerClientBase, _snd_seq_t


class PortCaps(IntFlag):
    """Port capability flags."""
    _NONE = 0
    READ = alsa.SND_SEQ_PORT_CAP_READ
    WRITE = alsa.SND_SEQ_PORT_CAP_WRITE
    SYNC_READ = alsa.SND_SEQ_PORT_CAP_SYNC_READ
    SYNC_WRITE = alsa.SND_SEQ_PORT_CAP_SYNC_WRITE
    DUPLEX = alsa.SND_SEQ_PORT_CAP_DUPLEX
    SUBS_READ = alsa.SND_SEQ_PORT_CAP_SUBS_READ
    SUBS_WRITE = alsa.SND_SEQ_PORT_CAP_SUBS_WRITE
    NO_EXPORT = alsa.SND_SEQ_PORT_CAP_NO_EXPORT


class PortType(IntFlag):
    """Port type flags."""
    ANY = 0
    SPECIFIC = alsa.SND_SEQ_PORT_TYPE_SPECIFIC
    MIDI_GENERIC = alsa.SND_SEQ_PORT_TYPE_MIDI_GENERIC
    MIDI_GM = alsa.SND_SEQ_PORT_TYPE_MIDI_GM
    MIDI_GS = alsa.SND_SEQ_PORT_TYPE_MIDI_GS
    MIDI_XG = alsa.SND_SEQ_PORT_TYPE_MIDI_XG
    MIDI_MT32 = alsa.SND_SEQ_PORT_TYPE_MIDI_MT32
    MIDI_GM2 = alsa.SND_SEQ_PORT_TYPE_MIDI_GM2
    SYNTH = alsa.SND_SEQ_PORT_TYPE_SYNTH
    DIRECT_SAMPLE = alsa.SND_SEQ_PORT_TYPE_DIRECT_SAMPLE
    SAMPLE = alsa.SND_SEQ_PORT_TYPE_SAMPLE
    HARDWARE = alsa.SND_SEQ_PORT_TYPE_HARDWARE
    SOFTWARE = alsa.SND_SEQ_PORT_TYPE_SOFTWARE
    SYNTHESIZER = alsa.SND_SEQ_PORT_TYPE_SYNTHESIZER
    PORT = alsa.SND_SEQ_PORT_TYPE_PORT
    APPLICATION = alsa.SND_SEQ_PORT_TYPE_APPLICATION


READ_PORT = PortCaps.READ | PortCaps.SUBS_READ
WRITE_PORT = PortCaps.WRITE | PortCaps.SUBS_WRITE
RW_PORT = READ_PORT | WRITE_PORT

READ_PORT_PREFERRED_TYPES = [
        PortType.MIDI_GENERIC
        ]

RW_PORT_PREFERRED_TYPES = READ_PORT_PREFERRED_TYPES

WRITE_PORT_PREFERRED_TYPES = [
        PortType.MIDI_GENERIC | PortType.MIDI_GM
        | PortType.SYNTHESIZER,
        PortType.MIDI_GENERIC | PortType.SYNTHESIZER,
        PortType.MIDI_GENERIC | PortType.MIDI_GM,
        PortType.MIDI_GENERIC
        ]

DEFAULT_PORT_TYPE = PortType.MIDI_GENERIC | PortType.SOFTWARE


class Port:
    """Sequencer port.

    :ivar client: the client object this port belongs to
    :ivar client_id: client identifier
    :ivar port_id: port identifier
    """

    client: Optional['SequencerClientBase']
    client_id: int
    port_id: int

    def __init__(self, client: 'SequencerClientBase', port_id: int):
        self.client_id = client.client_id
        self.port_id = port_id
        self.client = client

    def __del__(self):
        try:
            self.close()
        except Error:
            pass

    def _get_client_handle(self) -> '_snd_seq_t':
        if self.client is None:
            raise StateError("Already closed")
        handle = self.client.handle
        if handle is None:
            raise StateError("Sequencer already closed")
        return handle

    def close(self):
        """Close the port, freeing any resources.

        Wraps :alsa:`snd_seq_delete_simple_port`."""
        if self.client is None:
            return
        handle = self.client.handle
        port_id = self.port_id
        self.client = None
        if handle:
            err = alsa.snd_seq_delete_simple_port(handle, port_id)
            _check_alsa_error(err)

    def connect_to(self, dest: AddressType):
        """Connect port to another one.

        :param dest: destination port

        Wraps :alsa:`snd_seq_connect_to`.
        """
        client_id, port_id = Address(dest)
        handle = self._get_client_handle()
        err = alsa.snd_seq_connect_to(handle, self.port_id, client_id, port_id)
        _check_alsa_error(err)

    def disconnect_to(self, dest: AddressType):
        """Disconnect port from another one.

        :param dest: destination port

        Wraps :alsa:`snd_seq_disconnect_to`.
        """
        client_id, port_id = Address(dest)
        handle = self._get_client_handle()
        err = alsa.snd_seq_disconnect_to(handle, self.port_id, client_id, port_id)
        _check_alsa_error(err)

    def connect_from(self, src: AddressType):
        """Connect another port to this one.

        :param src: source port

        Wraps :alsa:`snd_seq_connect_from`.
        """
        client_id, port_id = Address(src)
        handle = self._get_client_handle()
        err = alsa.snd_seq_connect_from(handle, self.port_id, client_id, port_id)
        _check_alsa_error(err)

    def disconnect_from(self, src: AddressType):
        """Disconnect another port from this one.

        :param src: source port

        Wraps :alsa:`snd_seq_disconnect_from`.
        """
        client_id, port_id = Address(src)
        handle = self._get_client_handle()
        err = alsa.snd_seq_disconnect_from(handle, self.port_id, client_id, port_id)
        _check_alsa_error(err)

    def get_info(self) -> 'PortInfo':
        """Get information about the port.

        Wraps :alsa:`snd_seq_get_port_info`.
        """
        if self.client is None:
            raise StateError("Already closed")
        return self.client.get_port_info(self)

    def set_info(self, info: 'PortInfo'):
        """Update information about the port.

        Wraps :alsa:`snd_seq_set_port_info`.
        """
        if self.client is None:
            raise StateError("Already closed")
        return self.client.set_port_info(self, info)


_snd_seq_port_info_t = NewType("_snd_seq_port_info_t", object)


class PortInfo:
    """Sequencer port information.

    :ivar client_id: client identifier
    :ivar port_id: port identifier
    :ivar name: port name
    :ivar capability: port capabilities
    :ivar type: port type
    :ivar midi_channels: number of MIDI channels
    :ivar midi_voices: number of MIDI voices
    :ivar synth_voices: number of synth voices
    :ivar read_use: number of readers
    :ivar write_use: number of writers
    :ivar port_specified: `True` when port is specified in the structure
    :ivar timestamping: enable time stamping
    :ivar timestamp_real: use real time (not MIDI ticks) for time stamping
    :ivar timestamp_queue_id: queue used for timestamping
    :ivar client_name: client name. Set only when :meth:`~alsa_midi.SequencerClient.list_ports()`
                       was used to obtain this information.

    Represents :alsa:`snd_seq_port_info_t` with extra optional
    :attr:`client_name` attribute added when created by
    :meth:`~alsa_midi.SequencerClient.list_ports()`.
    """

    client_id: int
    port_id: int
    name: str
    capability: PortCaps
    type: PortType
    midi_channels: int
    midi_voices: int
    synth_voices: int
    read_use: int
    write_use: int
    port_specified: bool
    timestamping: bool
    timestamp_real: bool
    timestamp_queue_id: int

    client_name: Optional[str]

    def __init__(self,
                 client_id: int = 0,
                 port_id: int = None,
                 name: str = None,
                 capability: PortCaps = PortCaps._NONE,
                 type: PortType = PortType.ANY,
                 midi_channels: int = 0,
                 midi_voices: int = 0,
                 synth_voices: int = 0,
                 read_use: int = 0,
                 write_use: int = 0,
                 port_specified: bool = None,
                 timestamping: bool = False,
                 timestamp_real: bool = False,
                 timestamp_queue_id: int = 0):

        self.client_id = client_id
        if port_id is not None:
            self.port_id = port_id
            if port_specified is None:
                port_specified = True
        else:
            self.port_id = 0
            if port_specified is None:
                port_specified = False
        if name:
            self.name = name
        else:
            self.name = ""
        self.capability = capability
        self.type = type
        self.midi_channels = midi_channels
        self.midi_voices = midi_voices
        self.synth_voices = synth_voices
        self.read_use = read_use
        self.write_use = write_use
        self.port_specified = port_specified
        self.timestamping = timestamping
        self.timestamp_real = timestamp_real
        self.timestamp_queue_id = timestamp_queue_id
        self.client_name = None

    def __repr__(self):
        if self.client_name is not None:
            at_client_name = f" @ {self.client_name!r}"
        else:
            at_client_name = ""
        return f"<PortInfo {self.client_id}:{self.port_id} {self.name!r}{at_client_name}>"

    @classmethod
    def _from_alsa(cls, info: _snd_seq_port_info_t):
        name = ffi.string(alsa.snd_seq_port_info_get_name(info))
        caps = alsa.snd_seq_port_info_get_capability(info)
        p_type = alsa.snd_seq_port_info_get_type(info)
        return cls(
                client_id=alsa.snd_seq_port_info_get_client(info),
                port_id=alsa.snd_seq_port_info_get_port(info),
                name=name.decode(),
                capability=PortCaps(caps),
                type=PortType(p_type),
                midi_channels=alsa.snd_seq_port_info_get_midi_channels(info),
                midi_voices=alsa.snd_seq_port_info_get_midi_voices(info),
                synth_voices=alsa.snd_seq_port_info_get_synth_voices(info),
                read_use=alsa.snd_seq_port_info_get_read_use(info),
                write_use=alsa.snd_seq_port_info_get_write_use(info),
                port_specified=(alsa.snd_seq_port_info_get_port_specified(info) == 1),
                timestamping=(alsa.snd_seq_port_info_get_timestamping(info) == 1),
                timestamp_real=(alsa.snd_seq_port_info_get_timestamp_real(info) == 1),
                timestamp_queue_id=alsa.snd_seq_port_info_get_timestamp_queue(info),
                )

    def _to_alsa(self) -> _snd_seq_port_info_t:
        info_p = ffi.new("snd_seq_port_info_t **")
        err = alsa.snd_seq_port_info_malloc(info_p)
        _check_alsa_error(err)
        info = ffi.gc(info_p[0], alsa.snd_seq_port_info_free)
        alsa.snd_seq_port_info_set_client(info, self.client_id)
        alsa.snd_seq_port_info_set_port(info, self.port_id)
        alsa.snd_seq_port_info_set_name(info, self.name.encode())
        alsa.snd_seq_port_info_set_capability(info, self.capability)
        alsa.snd_seq_port_info_set_type(info, self.type)
        alsa.snd_seq_port_info_set_midi_channels(info, self.midi_channels)
        alsa.snd_seq_port_info_set_midi_voices(info, self.midi_voices)
        alsa.snd_seq_port_info_set_synth_voices(info, self.synth_voices)
        alsa.snd_seq_port_info_set_port_specified(info, self.port_specified)
        alsa.snd_seq_port_info_set_timestamping(info, self.timestamping)
        alsa.snd_seq_port_info_set_timestamp_real(info, self.timestamp_real)
        alsa.snd_seq_port_info_set_timestamp_queue(info, self.timestamp_queue_id)
        return info


def get_port_info_sort_key(preferred_types: List[PortType] = []
                           ) -> Callable[[PortInfo], Any]:
    """Return a :class:`PortInfo` sorting key function for given type
    preference."""
    def key(info: PortInfo):
        is_midi_through = info.client_name == "Midi Through"
        preference = len(preferred_types)
        for i, types in enumerate(preferred_types):
            if info.type & types == types:
                preference = i
                break
        return (is_midi_through, preference, info.client_id, info.port_id)
    return key


__all__ = ["PortCaps", "PortType", "Port",
           "READ_PORT", "WRITE_PORT", "RW_PORT", "DEFAULT_PORT_TYPE",
           "READ_PORT_PREFERRED_TYPES", "WRITE_PORT_PREFERRED_TYPES", "RW_PORT_PREFERRED_TYPES",
           "PortInfo"]
