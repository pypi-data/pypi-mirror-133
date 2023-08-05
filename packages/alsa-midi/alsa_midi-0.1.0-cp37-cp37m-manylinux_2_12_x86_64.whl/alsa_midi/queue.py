
from typing import TYPE_CHECKING, Optional

from ._ffi import alsa, ffi
from .event import EventType
from .exceptions import Error, StateError
from .util import _check_alsa_error

if TYPE_CHECKING:
    from .client import SequencerClientBase, _snd_seq_t


class Queue:
    """Sequencer queue.

    :ivar client: client object this queue belongs to
    :ivar queue_id: queue identifier
    """

    client: Optional['SequencerClientBase']
    queue_id: Optional[int]

    def __init__(self, client: 'SequencerClientBase', queue_id: int):
        self.client = client
        self.queue_id = queue_id

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

        Wraps :alsa:`snd_seq_free_queue`."""
        if self.queue_id is None or self.client is None:
            return
        handle = self.client.handle
        queue = self.queue_id
        self.queue_id = None
        self.client = None
        if handle:
            err = alsa.snd_seq_free_queue(handle, queue)
            _check_alsa_error(err)

    def set_tempo(self, tempo: int = 500000, ppq: int = 96):
        """Set the tempo of the queue.

        :param tempo: MIDI tempo – microseconds per quarter note
        :param ppq: MIDI pulses per quarter note

        Wraps :alsa:`snd_seq_set_queue_tempo`.
        """
        handle = self._get_client_handle()
        q_tempo_p = ffi.new("snd_seq_queue_tempo_t **", ffi.NULL)
        err = alsa.snd_seq_queue_tempo_malloc(q_tempo_p)
        _check_alsa_error(err)
        q_tempo = ffi.gc(q_tempo_p[0], alsa.snd_seq_queue_tempo_free)
        alsa.snd_seq_queue_tempo_set_tempo(q_tempo, tempo)
        alsa.snd_seq_queue_tempo_set_ppq(q_tempo, ppq)
        err = alsa.snd_seq_set_queue_tempo(handle, self.queue_id, q_tempo)
        _check_alsa_error(err)

    def control(self, event_type: EventType, value: int = 0):
        """Queue control (start/stop/continue).

        :param event_type: queue control event type
        :param value: value for the event

        Creates and sends (to the output buffer) queue control event.
        :meth:`~alsa_midi.SequencerClient.drain_output()` needs to be called for the
        event to actually be sent and executed.

        Wraps :alsa:`snd_seq_control_queue`.
        """
        # TODO: event argument
        handle = self._get_client_handle()
        err = alsa.snd_seq_control_queue(handle, self.queue_id, event_type, value, ffi.NULL)
        _check_alsa_error(err)

    def start(self):
        """Start the queue.

        :meth:`~alsa_midi.SequencerClient.drain_output()` needs to be called for actual effect.
        """
        return self.control(EventType.START)

    def stop(self):
        """Stop the queue.

        :meth:`~alsa_midi.SequencerClient.drain_output()` needs to be called for actual effect.
        """
        return self.control(EventType.STOP)

    def continue_(self):
        """Continue running the queue.

        :meth:`~alsa_midi.SequencerClient.drain_output()` needs to be called for actual effect.
        """
        return self.control(EventType.CONTINUE)


__all__ = ["Queue"]
