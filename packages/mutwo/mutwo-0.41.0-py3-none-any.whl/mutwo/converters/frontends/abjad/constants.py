"""Constants to be used for and with :mod:`mutwo.converters.frontends.abjad`.
"""

import inspect

from mutwo.converters.frontends.abjad import attachments

DEFAULT_ABJAD_ATTACHMENT_CLASSES = tuple(
    cls
    for _, cls in inspect.getmembers(attachments, inspect.isclass)
    if not inspect.isabstract(cls)
)
"""Default value for argument `abjad_attachment_classes` in
:class:`~mutwo.converters.frontends.SequentialEventToAbjadVoiceConverter`."""
