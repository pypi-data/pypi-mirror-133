"""Render midi files (SMF) from mutwo data.

"""

import functools
import itertools
import operator
import typing
import warnings

import expenvelope  # type: ignore
import mido  # type: ignore

from mutwo.converters import abc
from mutwo.converters.frontends import midi_constants
from mutwo.converters import symmetrical

from mutwo import events
from mutwo import parameters
from mutwo import utilities

__all__ = (
    "MutwoPitchToMidiPitchConverter",
    "MidiFileConverter",
)

ConvertableEvents = typing.Union[
    events.basic.SimpleEvent,
    events.basic.SequentialEvent[events.basic.SimpleEvent],
    events.basic.SimultaneousEvent[
        events.basic.SequentialEvent[events.basic.SimpleEvent]
    ],
]

MidiNote = int
PitchBend = int

MidiPitch = tuple[MidiNote, PitchBend]


class MutwoPitchToMidiPitchConverter(abc.Converter):
    """Convert mutwo pitch to midi pitch number and midi pitch bend number.

    :param maximum_pitch_bend_deviation: sets the maximum pitch bending range in cents.
        This value depends on the particular used software synthesizer and its settings,
        because it is up to the respective synthesizer how to interpret the pitch
        bending messages. By default mutwo sets the value to 200 cents which
        seems to be the most common interpretation among different manufacturers.
    :type maximum_pitch_bend_deviation: int
    """

    def __init__(self, maximum_pitch_bend_deviation: typing.Optional[float] = None):
        if maximum_pitch_bend_deviation is None:
            maximum_pitch_bend_deviation = (
                midi_constants.DEFAULT_MAXIMUM_PITCH_BEND_DEVIATION_IN_CENTS
            )

        self._maximum_pitch_bend_deviation = maximum_pitch_bend_deviation
        self._pitch_bending_warning = (
            f"Maximum pitch bending is {maximum_pitch_bend_deviation} cents up or down!"
        )

    def _cent_deviation_to_pitch_bending_number(
        self,
        cent_deviation: utilities.constants.Real,
    ) -> int:
        pitch_bend_percent = (cent_deviation + self._maximum_pitch_bend_deviation) / (
            self._maximum_pitch_bend_deviation * 2
        )

        if pitch_bend_percent > 1:
            pitch_bend_percent = 1
            warnings.warn(self._pitch_bending_warning)

        if pitch_bend_percent < 0:
            pitch_bend_percent = 0
            warnings.warn(self._pitch_bending_warning)

        pitch_bending_number = round(
            midi_constants.MAXIMUM_PITCH_BEND * pitch_bend_percent
        )
        pitch_bending_number -= midi_constants.NEUTRAL_PITCH_BEND

        return pitch_bending_number

    def convert(
        self,
        mutwo_pitch_to_convert: parameters.abc.Pitch,
        midi_note: typing.Optional[int] = None,
    ) -> MidiPitch:
        """Find midi note and pitch bending for given mutwo pitch

        :param mutwo_pitch_to_convert: The mutwo pitch which shall be converted.
        :type mutwo_pitch_to_convert: parameters.abc.Pitch
        :param midi_note: Can be set to a midi note value if one wants to force
            the converter to calculate the pitch bending deviation for the passed
            midi note. If this argument is ``None`` the converter will simply use
            the closest midi pitch number to the passed mutwo pitch. Default to ``None``.
        :type midi_note: typing.Optional[int]
        """

        frequency = mutwo_pitch_to_convert.frequency
        if midi_note:
            closest_midi_pitch = midi_note
        else:
            closest_midi_pitch = utilities.tools.find_closest_index(
                frequency, parameters.pitches_constants.MIDI_PITCH_FREQUENCIES
            )
        difference_in_cents_to_closest_midi_pitch = parameters.abc.Pitch.hertz_to_cents(
            parameters.pitches_constants.MIDI_PITCH_FREQUENCIES[closest_midi_pitch],
            frequency,
        )
        pitch_bending_number = self._cent_deviation_to_pitch_bending_number(
            difference_in_cents_to_closest_midi_pitch
        )

        return closest_midi_pitch, pitch_bending_number


class MidiFileConverter(abc.Converter):
    """Class for rendering standard midi files (SMF) from mutwo data.

    Mutwo offers a wide range of options how the respective midi file shall
    be rendered and how mutwo data shall be translated. This is necessary due
    to the limited and not always unambiguous nature of musical encodings in
    midi files. In this way the user can tweak the conversion routine to her
    or his individual needs.

    :param simple_event_to_pitch_list: Function to extract from a
        :class:`mutwo.events.basic.SimpleEvent` a tuple that contains pitch objects
        (objects that inherit from :class:`mutwo.parameters.abc.Pitch`).
        By default it asks the Event for its :attr:`pitch_list` attribute
        (because by default :class:`mutwo.events.music.NoteLike` objects are expected).
        When using different Event classes than ``NoteLike`` with a different name for
        their pitch property, this argument should be overridden. If the function call
        raises an :obj:`AttributeError` (e.g. if no pitch can be extracted),
        mutwo will interpret the event as a rest.
    :type simple_event_to_pitch_list: typing.Callable[
            [events.basic.SimpleEvent], tuple[parameters.abc.Pitch, ...]]
    :param simple_event_to_volume: Function to extract the volume from a
        :class:`mutwo.events.basic.SimpleEvent` in the purpose of generating midi notes.
        The function should return an object that inhertis from
        :class:`mutwo.parameters.abc.Volume`. By default it asks the Event for
        its :attr:`volume` attribute (because by default
        :class:`mutwo.events.music.NoteLike` objects are expected).
        When using different Event classes than ``NoteLike`` with a
        different name for their volume property, this argument should be overridden.
        If the function call raises an :obj:`AttributeError` (e.g. if no volume can be
        extracted), mutwo will interpret the event as a rest.
    :type simple_event_to_volume: typing.Callable[
            [events.basic.SimpleEvent], parameters.abc.Volume]
    :param simple_event_to_control_message_tuple: Function to generate midi control messages
        from a simple event. By default no control messages are generated. If the
        function call raises an AttributeError (e.g. if an expected control value isn't
        available) mutwo will interpret the event as a rest.
    :type simple_event_to_control_message_tuple: typing.Callable[
            [events.basic.SimpleEvent], tuple[mido.Message, ...]]
    :param midi_file_type: Can either be 0 (for one-track midi files) or 1 (for
         synchronous multi-track midi files). Mutwo doesn't offer support for generating
         type 2 midi files (midi files with asynchronous tracks).
    :type midi_file_type: int
    :param available_midi_channels: tuple containing integer where each integer
        represents the number of the used midi channel. Integer can range from 0 to 15.
        Higher numbers of available_midi_channels (like all 16) are recommended when
        rendering microtonal music. It shall be remarked that midi-channel 9 (or midi
        channel 10 when starting to count from 1) is often ignored by several software
        synthesizer, because this channel is reserved for percussion instruments.
    :type available_midi_channels: tuple[int, ...]
    :param distribute_midi_channels: This parameter is only relevant if more than one
        :class:`~mutwo.events.basic.SequentialEvent` is passed to the convert method.
        If set to ``True`` each :class:`~mutwo.events.basic.SequentialEvent`
        only makes use of exactly n_midi_channel (see next parameter).
        If set to ``False`` each converted :class:`SequentialEvent` is allowed to make use of all
        available channels. If set to ``True`` and the amount of necessary MidiTracks is
        higher than the amount of available channels, mutwo will silently cycle through
        the list of available midi channel.
    :type distribute_midi_channels: bool
    :param n_midi_channels_per_track: This parameter is only relevant for
        distribute_midi_channels == True. It sets how many midi channels are assigned
        to one SequentialEvent. If microtonal chords shall be played by
        one SequentialEvent (via pitch bending messages) a higher number than 1 is
        recommended. Defaults to 1.
    :type n_midi_channels_per_track: int
    :param mutwo_pitch_to_midi_pitch_converter: class to convert from mutwo pitches
        to midi pitches. Default to :class:`MutwoPitchToMidiPitchConverter`.
    :type mutwo_pitch_to_midi_pitch_converter: :class:`MutwoPitchToMidiPitchConverter`
    :param ticks_per_beat: Sets the timing precision of the midi file. From the mido
        documentation: "Typical values range from 96 to 480 but some use even more
        ticks per beat".
    :type ticks_per_beat: int
    :param instrument_name: Sets the midi instrument of all channels.
    :type instrument_name: str
    :param tempo_envelope: All Midi files should specify their tempo. The default
        value of mutwo is 120 BPM (this is also the value that is assumed by any
        midi-file-reading-software if no tempo has been specified). Tempo changes
        are supported (and will be written to the resulting midi file).
    :type tempo_envelope: expenvelope.Envelope

    **Example**:

    >>> from mutwo.converters.frontends import midi
    >>> from mutwo.parameters import pitches
    >>> # midi file converter that assign a middle c to all events
    >>> midi_converter = midi.MidiFileConverter(
    >>>     simple_event_to_pitch_list=lambda event: (pitches.WesternPitch('c'),)
    >>> )

    **Disclaimer**:
        The current implementation doesn't support glissandi yet (only static pitches),
        time-signatures (the written time signature is always 4/4 for now) and
        dynamically changing tempo (ritardando or accelerando).
    """

    _tempo_point_converter = symmetrical.tempos.TempoPointConverter()

    def __init__(
        self,
        simple_event_to_pitch_list: typing.Callable[
            [events.basic.SimpleEvent], tuple[parameters.abc.Pitch, ...]
        ] = lambda event: event.pitch_list,  # type: ignore
        simple_event_to_volume: typing.Callable[
            [events.basic.SimpleEvent], parameters.abc.Volume
        ] = lambda event: event.volume,  # type: ignore
        simple_event_to_control_message_tuple: typing.Callable[
            [events.basic.SimpleEvent], tuple[mido.Message, ...]
        ] = lambda event: tuple([]),
        midi_file_type: int = None,
        available_midi_channels: tuple[int, ...] = None,
        distribute_midi_channels: bool = False,
        n_midi_channels_per_track: typing.Optional[int] = None,
        mutwo_pitch_to_midi_pitch_converter: MutwoPitchToMidiPitchConverter = MutwoPitchToMidiPitchConverter(),
        ticks_per_beat: typing.Optional[int] = None,
        instrument_name: typing.Optional[str] = None,
        tempo_envelope: typing.Optional[expenvelope.Envelope] = None,
    ):
        # TODO(find a less redundant way of setting default values)
        # set current default values if parameters aren't defined
        if midi_file_type is None:
            midi_file_type = midi_constants.DEFAULT_MIDI_FILE_TYPE

        if available_midi_channels is None:
            available_midi_channels = midi_constants.DEFAULT_AVAILABLE_MIDI_CHANNELS

        if n_midi_channels_per_track is None:
            n_midi_channels_per_track = midi_constants.DEFAULT_N_MIDI_CHANNELS_PER_TRACK

        if ticks_per_beat is None:
            ticks_per_beat = midi_constants.DEFAULT_TICKS_PER_BEAT

        if instrument_name is None:
            instrument_name = midi_constants.DEFAULT_MIDI_INSTRUMENT_NAME

        if tempo_envelope is None:
            tempo_envelope = midi_constants.DEFAULT_TEMPO_ENVELOPE

        # check for correct values of midi specifications (have to be correct to be
        # able to write a readable midi file)
        self._assert_midi_file_type_has_correct_value(midi_file_type)
        self._assert_available_midi_channels_have_correct_value(available_midi_channels)

        # initialise the attributes of the class
        self._simple_event_to_pitch_list = simple_event_to_pitch_list
        self._simple_event_to_volume = simple_event_to_volume
        self._simple_event_to_control_message_tuple = (
            simple_event_to_control_message_tuple
        )

        self._distribute_midi_channels = distribute_midi_channels
        self._n_midi_channels_per_track = n_midi_channels_per_track
        self._available_midi_channels = available_midi_channels
        self._midi_file_type = midi_file_type
        self._mutwo_pitch_to_midi_pitch_converter = mutwo_pitch_to_midi_pitch_converter
        self._ticks_per_beat = ticks_per_beat
        self._instrument_name = instrument_name

        self._tempo_envelope = tempo_envelope

    # ###################################################################### #
    #                          static methods                                #
    # ###################################################################### #

    @staticmethod
    def _assert_midi_file_type_has_correct_value(midi_file_type: int):
        try:
            assert midi_file_type in (0, 1)
        except AssertionError:
            message = (
                "Unknown midi_file_type '{}'. Only midi type 0 and 1 are supported."
            )
            raise ValueError(message)

    @staticmethod
    def _assert_available_midi_channels_have_correct_value(
        available_midi_channels: tuple[int, ...],
    ):
        # check for correct range of each number
        for midi_channel in available_midi_channels:
            try:
                assert midi_channel in midi_constants.ALLOWED_MIDI_CHANNELS
            except AssertionError:
                message = "Found unknown midi channel '{}' in available_midi_channels.".format(
                    midi_constants.ALLOWED_MIDI_CHANNELS
                )
                message += " Only midi channel '{}' are allowed.".format(
                    midi_constants.ALLOWED_MIDI_CHANNELS
                )
                raise ValueError(message)

        # check for duplicate
        try:
            assert len(available_midi_channels) == len(set(available_midi_channels))
        except AssertionError:
            message = "Found duplicate in available_midi_channels '{}'.".format(
                available_midi_channels
            )
            raise ValueError(message)

    @staticmethod
    def _adjust_beat_length_in_microseconds(
        tempo_point: typing.Union[
            utilities.constants.Real, parameters.tempos.TempoPoint
        ],
        beat_length_in_microseconds: int,
    ) -> int:
        """This method makes sure that ``beat_length_in_microseconds`` isn't too big.

        Standard midi files define a slowest allowed tempo which is around 3.5 BPM.
        In case the tempo is lower than this slowest allowed tempo, `mutwo` will
        automatically set the tempo to the lowest allowed tempo.
        """

        if beat_length_in_microseconds >= midi_constants.MAXIMUM_MICROSECONDS_PER_BEAT:
            beat_length_in_microseconds = midi_constants.MAXIMUM_MICROSECONDS_PER_BEAT
            message = "TempoPoint '{}' is too slow for Standard Midi Files. ".format(
                tempo_point
            )
            message += (
                "The slowest possible tempo is '{0}' BPM. Tempo has been set to"
                " '{0}' BPM.".format(
                    mido.tempo2bpm(midi_constants.MAXIMUM_MICROSECONDS_PER_BEAT)
                )
            )
            warnings.warn(message)

        return beat_length_in_microseconds

    # ###################################################################### #
    #                         helper methods                                 #
    # ###################################################################### #

    def _beats_per_minute_to_beat_length_in_microseconds(
        self, beats_per_minute: utilities.constants.Real
    ) -> int:
        """Method for converting beats per minute (BPM) to midi tempo.

        Midi tempo is stated in beat length in microseconds.
        """

        beat_length_in_seconds = self._tempo_point_converter.convert(beats_per_minute)
        beat_length_in_microseconds = int(
            beat_length_in_seconds * midi_constants.MIDI_TEMPO_FACTOR
        )
        return beat_length_in_microseconds

    def _find_available_midi_channels_per_sequential_event(
        self,
        simultaneous_event: events.basic.SimultaneousEvent[
            events.basic.SequentialEvent[events.basic.SimpleEvent]
        ],
    ) -> tuple[tuple[int, ...], ...]:
        """Find midi channels for each SequentialEvent.

        Depending on whether distribute_midi_channels has been set
        to True this method distributes all available midi channels
        on the respective SequentialEvents.
        """

        if self._distribute_midi_channels:
            available_midi_channels_cycle = itertools.cycle(
                self._available_midi_channels
            )
            available_midi_channels_per_sequential_event = tuple(
                tuple(
                    next(available_midi_channels_cycle)
                    for _ in range(self._n_midi_channels_per_track)
                )
                for _ in simultaneous_event
            )

        else:
            available_midi_channels_per_sequential_event = tuple(
                self._available_midi_channels for _ in simultaneous_event
            )

        return available_midi_channels_per_sequential_event

    def _beats_to_ticks(self, absolute_time: parameters.abc.DurationType) -> int:
        return int(self._ticks_per_beat * absolute_time)

    # ###################################################################### #
    #             methods for converting mutwo data to midi data             #
    # ###################################################################### #

    def _tempo_envelope_to_midi_messages(
        self, tempo_envelope: expenvelope.Envelope
    ) -> tuple[mido.MetaMessage, ...]:
        """Converts a SequentialEvent of ``EnvelopeEvent`` to midi Tempo messages."""

        absolute_times = utilities.tools.accumulate_from_zero(tempo_envelope.durations)

        midi_messages = []
        for absolute_time, tempo_point in zip(absolute_times, tempo_envelope.levels):
            absolute_tick = self._beats_to_ticks(absolute_time)
            beat_length_in_microseconds = (
                self._beats_per_minute_to_beat_length_in_microseconds(tempo_point)
            )

            beat_length_in_microseconds = (
                MidiFileConverter._adjust_beat_length_in_microseconds(
                    tempo_point, beat_length_in_microseconds
                )
            )

            tempo_message = mido.MetaMessage(
                "set_tempo", tempo=beat_length_in_microseconds, time=absolute_tick
            )
            midi_messages.append(tempo_message)

        return tuple(midi_messages)

    def _tune_pitch(
        self,
        absolute_tick_start: int,
        pitch_to_tune: parameters.abc.Pitch,
        midi_channel: int,
    ) -> tuple[MidiNote, mido.Message]:
        (
            midi_pitch,
            pitch_bending_number,
        ) = self._mutwo_pitch_to_midi_pitch_converter.convert(pitch_to_tune)
        pitch_bending_message_time = absolute_tick_start
        if absolute_tick_start != 0:
            # if possible add bending one tick earlier to avoid glitches
            pitch_bending_message_time -= 1

        pitch_bending_message = mido.Message(
            "pitchwheel",
            channel=midi_channel,
            pitch=pitch_bending_number,
            time=pitch_bending_message_time,
        )
        return midi_pitch, pitch_bending_message

    def _note_information_to_midi_messages(
        self,
        absolute_tick_start: int,
        absolute_tick_end: int,
        velocity: int,
        pitch: parameters.abc.Pitch,
        available_midi_channels_cycle: typing.Iterator,
    ) -> tuple[mido.Message, ...]:
        """Generate 'pitch bending', 'note on' and 'note off' messages for one tone."""

        midi_channel = next(available_midi_channels_cycle)
        midi_pitch, pitch_bending_message = self._tune_pitch(
            absolute_tick_start,
            pitch,
            midi_channel,
        )

        midi_messages = [pitch_bending_message]

        for time, message_name in (
            (absolute_tick_start, "note_on"),
            (absolute_tick_end, "note_off"),
        ):
            midi_messages.append(
                mido.Message(
                    message_name,
                    note=midi_pitch,
                    velocity=velocity,
                    time=time,
                    channel=midi_channel,
                )
            )

        return tuple(midi_messages)

    def _extracted_data_to_midi_messages(
        self,
        absolute_time: utilities.constants.Real,
        duration: parameters.abc.DurationType,
        available_midi_channels_cycle: typing.Iterator,
        pitch_list: tuple[parameters.abc.Pitch, ...],
        volume: parameters.abc.Volume,
        control_messages: tuple[mido.Message, ...],
    ) -> tuple[mido.Message, ...]:
        """Generates pitch-bend / note-on / note-off messages for each tone in a chord.

        Concatenates the midi messages for every played tone with the global control
        messages.

        Gets as an input relevant data for midi message generation that has been
        extracted from a :class:`mutwo.abc.Event` object.
        """

        absolute_tick_start = self._beats_to_ticks(absolute_time)
        absolute_tick_end = absolute_tick_start + self._beats_to_ticks(duration)
        velocity = volume.midi_velocity

        midi_messages = []

        # add control messages
        for control_message in control_messages:
            control_message.time = absolute_tick_start
            midi_messages.append(control_message)

        # add note related messages
        for pitch in pitch_list:
            midi_messages.extend(
                self._note_information_to_midi_messages(
                    absolute_tick_start,
                    absolute_tick_end,
                    velocity,
                    pitch,
                    available_midi_channels_cycle,
                )
            )

        return tuple(midi_messages)

    def _simple_event_to_midi_messages(
        self,
        simple_event: events.basic.SimpleEvent,
        absolute_time: utilities.constants.Real,
        available_midi_channels_cycle: typing.Iterator,
    ) -> tuple[mido.Message, ...]:
        """Converts ``SimpleEvent`` (or any object that inherits from ``SimpleEvent``).

        Return tuple filled with midi messages that represent the mutwo data in the
        midi format.
        """

        extracted_data = []

        # try to extract the relevant data
        is_rest = False
        for extraction_function in (
            self._simple_event_to_pitch_list,
            self._simple_event_to_volume,
            self._simple_event_to_control_message_tuple,
        ):
            try:
                extracted_data.append(extraction_function(simple_event))
            except AttributeError:
                is_rest = True
                break

        # if not all relevant data could be extracted, simply ignore the
        # event
        if is_rest:
            return tuple([])

        # otherwise generate midi messages from the extracted data
        midi_messages = self._extracted_data_to_midi_messages(
            absolute_time,
            simple_event.duration,
            available_midi_channels_cycle,
            *extracted_data,  # type: ignore
        )
        return tuple(midi_messages)

    def _sequential_event_to_midi_messages(
        self,
        sequential_event: events.basic.SequentialEvent[events.basic.SimpleEvent],
        available_midi_channels: tuple[int, ...],
    ) -> tuple[mido.Message, ...]:
        """Iterates through the ``SequentialEvent`` and converts each ``SimpleEvent``.

        Return unsorted tuple of Midi messages where the time attribute of each message
        is the absolute time in ticks.
        """

        midi_data: list[mido.Message] = []

        available_midi_channels_cycle = itertools.cycle(available_midi_channels)

        # fill midi track with the content of the sequential event
        for absolute_time, simple_event in zip(
            sequential_event.absolute_times, sequential_event
        ):
            midi_messages = self._simple_event_to_midi_messages(
                simple_event, absolute_time, available_midi_channels_cycle
            )
            midi_data.extend(midi_messages)

        return tuple(midi_data)

    def _midi_messages_to_midi_track(
        self,
        midi_data: tuple[mido.Message, ...],
        duration: parameters.abc.DurationType,
        is_first_track: bool = False,
    ) -> mido.MidiTrack:
        """Convert unsorted midi message with absolute timing to a midi track.

        In the resulting midi track the timing of the messages is relative.
        """

        # initialise midi track
        track = mido.MidiTrack([])
        track.append(mido.MetaMessage("instrument_name", name=self._instrument_name))

        if is_first_track:
            # standard time signature 4/4
            track.append(mido.MetaMessage("time_signature", numerator=4, denominator=4))
            midi_data += self._tempo_envelope_to_midi_messages(self._tempo_envelope)

        # sort midi data
        sorted_midi_data = sorted(midi_data, key=lambda message: message.time)

        # add end of track message
        duration_in_ticks = self._beats_to_ticks(duration)
        sorted_midi_data.append(
            mido.MetaMessage("end_of_track", time=duration_in_ticks)
        )

        # convert from absolute to relative time
        delta_ticks_per_message = tuple(
            message1.time - message0.time
            for message0, message1 in zip(sorted_midi_data, sorted_midi_data[1:])
        )
        delta_ticks_per_message = (sorted_midi_data[0].time,) + delta_ticks_per_message
        for dt, message in zip(delta_ticks_per_message, sorted_midi_data):
            message.time = dt

        # add midi data to midi track
        track.extend(sorted_midi_data)

        return track

    # ###################################################################### #
    #           methods for filling the midi file (only called once)         #
    # ###################################################################### #

    def _add_simple_event_to_midi_file(
        self, simple_event: events.basic.SimpleEvent, midi_file: mido.MidiFile
    ) -> None:
        """Adds simple event to midi file."""
        self._add_sequential_event_to_midi_file(
            events.basic.SequentialEvent([simple_event]), midi_file
        )

    def _add_sequential_event_to_midi_file(
        self,
        sequential_event: events.basic.SequentialEvent[events.basic.SimpleEvent],
        midi_file: mido.MidiFile,
    ) -> None:
        """Adds sequential event to midi file."""
        self._add_simultaneous_event_to_midi_file(
            events.basic.SimultaneousEvent([sequential_event]), midi_file
        )

    def _add_simultaneous_event_to_midi_file(
        self,
        simultaneous_event: events.basic.SimultaneousEvent[
            events.basic.SequentialEvent[events.basic.SimpleEvent]
        ],
        midi_file: mido.MidiFile,
    ) -> None:
        """Adds one simultaneous event to a midi file.

        Depending on the midi_file_type either adds a tuple of MidiTrack
        objects (for midi_file_type = 1) or adds only one MidiTrack
        (for midi_file_type = 0).
        """

        # TODO(split this method, make it more readable!)

        available_midi_channels_per_sequential_event = (
            self._find_available_midi_channels_per_sequential_event(simultaneous_event)
        )

        midi_data_per_sequential_event = tuple(
            self._sequential_event_to_midi_messages(
                sequential_event, available_midi_channels
            )
            for sequential_event, available_midi_channels in zip(
                simultaneous_event, available_midi_channels_per_sequential_event
            )
        )

        duration = simultaneous_event.duration

        # midi file type 0 -> only one track
        if self._midi_file_type == 0:
            midi_data_for_one_track = functools.reduce(
                operator.add, midi_data_per_sequential_event
            )
            midi_track = self._midi_messages_to_midi_track(
                midi_data_for_one_track, duration, is_first_track=True
            )
            midi_file.tracks.append(midi_track)

        # midi file type 1
        else:
            midi_tracks = (
                self._midi_messages_to_midi_track(
                    midi_data, duration, is_first_track=nth_midi_data == 0
                )
                for nth_midi_data, midi_data in enumerate(
                    midi_data_per_sequential_event
                )
            )
            midi_file.tracks.extend(midi_tracks)

    def _event_to_midi_file(self, event_to_convert: ConvertableEvents) -> mido.MidiFile:
        """Convert mutwo event object to mido MidiFile object."""

        midi_file = mido.MidiFile(
            ticks_per_beat=self._ticks_per_beat, type=self._midi_file_type
        )

        # depending on the event types timing structure different methods are called
        if isinstance(event_to_convert, events.basic.SimultaneousEvent):
            self._add_simultaneous_event_to_midi_file(event_to_convert, midi_file)
        elif isinstance(event_to_convert, events.basic.SequentialEvent):
            self._add_sequential_event_to_midi_file(event_to_convert, midi_file)
        elif isinstance(event_to_convert, events.basic.SimpleEvent):
            self._add_simple_event_to_midi_file(event_to_convert, midi_file)
        else:
            message = "Can't convert object '{}' of type '{}' to a MidiFile.".format(
                event_to_convert, type(event_to_convert)
            )
            message += " Supported types include all inherited classes "
            message += "from '{}'.".format(ConvertableEvents)
            raise TypeError(message)

        return midi_file

    # ###################################################################### #
    #               public methods for interaction with the user             #
    # ###################################################################### #

    def convert(self, event_to_convert: ConvertableEvents, path: str) -> None:
        """Render a Midi file to the converters path attribute from the given event.

        :param event_to_convert: The given event that shall be translated
            to a Midi file.
        :type event_to_convert: typing.Union[events.basic.SimpleEvent, events.basic.SequentialEvent[events.basic.SimpleEvent], events.basic.SimultaneousEvent[events.basic.SequentialEvent[events.basic.SimpleEvent]]]
        :param path: where to write the midi file. The typical file type extension '.mid'
            is recommended, but not mandatory.
        :type path: str

        The following example generates a midi file that contains a simple ascending
        pentatonic scale:

        >>> from mutwo.events import basic, music
        >>> from mutwo.parameters import pitches
        >>> from mutwo.converters.frontends import midi
        >>> ascending_scale = basic.SequentialEvent(
        >>>     [
        >>>         music.NoteLike(pitches.WesternPitch(pitch), duration=1, volume=0.5)
        >>>         for pitch in 'c d e g a'.split(' ')
        >>>     ]
        >>> )
        >>> midi_converter = midi.MidiFileConverter(
        >>>     available_midi_channels=(0,)
        >>> )
        >>> midi_converter.convert(ascending_scale, 'ascending_scale.mid')

        **Disclaimer:** when passing nested structures, make sure that the
        nested object matches the expected type. Unlike other mutwo
        converter classes (like :class:`mutwo.converters.symmetrical.TempoConverter`)
        :class:`MidiFileConverter` can't convert infinitely nested structures
        (due to the particular way how Midi files are defined). The deepest potential
        structure is a :class:`mutwo.events.basic.SimultaneousEvent` (representing
        the complete MidiFile) that contains :class:`mutwo.events.basic.SequentialEvent`
        (where each ``SequentialEvent`` represents one MidiTrack) that contains
        :class:`mutwo.events.basic.SimpleEvent` (where each ``SimpleEvent``
        represents one midi note). If only one ``SequentialEvent`` is send,
        this ``SequentialEvent`` will be read as one MidiTrack in a MidiFile.
        If only one ``SimpleEvent`` get passed, this ``SimpleEvent`` will be
        interpreted as one MidiEvent (note_on and note_off) inside one
        MidiTrack inside one MidiFile.
        """

        midi_file = self._event_to_midi_file(event_to_convert)
        midi_file.save(filename=path)
