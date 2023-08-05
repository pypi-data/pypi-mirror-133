#!/usr/bin/python3
# Import any necessary modules.
import os
import shutil
import sys
import numpy

from glxaudio.Audio import Audio
from glxaudio.AudioConstants import GLXAUDIO
from glxviewer.colors import Colors

# Do a basic screen clear.
os.system("clear")
# Turn the cursor off to look prettier... ;o)
os.system("setterm -cursor off")

if os.path.isdir("."):
    pass


class AudioScope(Audio):
    def __init__(self):

        # Audio section
        Audio.__init__(self)
        self.format = GLXAUDIO.FORMAT_INT16
        self.rate = 22050
        self.channels = 1
        self.chunk_size = int(self.rate * 0.025)
        # Internal class
        self.colors_gradient = []

        self.chars = " ░▒▓\t▓▒░"

    def __enter__(self):
        """Open the microphone stream."""

        # device_info = self.audio.get_default_input_device_info()
        # rate = int(device_info['defaultSampleRate'])

        self.stream = self.create_audio().open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )

        return self

    def __exit__(self):
        self.stream_close()

    def listen(self):
        """
        Start a list action
        """

        while True:
            data = numpy.fromstring(
                self.stream.read(self.chunk_size, exception_on_overflow=False),
                dtype=self.dtype,
            )

            data_left = data[0::2]
            data_right = data[1::2]

            peak_left = numpy.abs(numpy.max(data_left) - numpy.min(data_left)) / self.get_base_ten_signed_max_value()
            peak_right = numpy.abs(numpy.max(data_right) - numpy.min(data_right)) / self.get_base_ten_signed_max_value()

            half_size = int(self._get_terminal_width() / 2) - 2

            # chart = '▓▒░'

            if int(half_size / 100 * (peak_left * 100)) >= 2:
                left_progress = "▓" * int((half_size / 100 * (peak_left * 100)) - 3) + "▒"
                left_progress = "".join(Colors.CBLUE + "▓▒" + Colors.end + left_progress)
            elif int(half_size / 100 * (peak_left * 100)) == 1:
                left_progress = "".join(Colors.CBLUE + "▒" + Colors.end)
            else:
                left_progress = "".join(Colors.CBLUE + "░" + Colors.end)

            if int(half_size / 100 * (peak_right * 100)) >= 2:
                right_progress = "▒" + "▓" * int((half_size / 100 * (peak_right * 100)) - 3)
                right_progress = "".join(right_progress + Colors.CBLUE + "▒▓" + Colors.end)
            elif int(half_size / 100 * (peak_right * 100)) == 1:
                right_progress = "".join(Colors.CBLUE + "▒" + Colors.end)
            else:
                right_progress = "".join(Colors.CBLUE + "░" + Colors.end)

            line_new = "{0:>{1}}{2:<{3}}".format(left_progress, half_size, right_progress, half_size)
            # line_new = "{0:>{1}}".format(left_progress, half_size)
            # sys.stdout.write(line_new + '\auto_gain_control_queue_size')
            #
            # # line = (self.color(x) for x in line_new[:half_size])

            sys.stdout.write("".join(line_new) + "\n")
            sys.stdout.flush()

    def color(self, value):
        """
        Given 0 <= x <= 1 (input is clamped), return a string of ANSI
        escape sequences representing a colors_gradient color.

        :param value: a value
        :type value: float
        """
        value = max(0.0, min(1.0, value))
        return self.colors_gradient[int(value * (len(self.colors_gradient) - 1))]

    @staticmethod
    def _get_terminal_width():
        """
        return width after have estimate the terminal size.

        :return: terminal width
        :rtype: int
        """
        try:
            width, _ = shutil.get_terminal_size()
        except AttributeError:
            width = 80

        return int(width)


if __name__ == "__main__":
    # Do a basic screen clear.
    os.system("clear")
    # Turn the cursor off to look prettier... ;o)
    os.system("setterm -cursor off")

    with AudioScope() as audioscope:
        try:
            while True:
                audioscope.listen()

        # Assuming a Ctrl-C arrives here enable the cursor again.
        except KeyboardInterrupt:
            if bool(audioscope.stream):
                audioscope.stream.stop_stream()
                audioscope.stream.close()
            if bool(audioscope.get_audio()):
                audioscope.get_audio().terminate()
            sys.exit(0)
