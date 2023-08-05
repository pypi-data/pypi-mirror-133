# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

import time
import wave
import pyaudio
from glxviewer import viewer
from glxaudio.Audio import Audio
from glxaudio.file import File
from glxaudio.AudioUtils import sec2time


class AudioPLayer(Audio):
    def __init__(self):
        Audio.__init__(self)

        self.__duration_start = None
        self.__detached = None
        self.__file = None

        self.duration_start = None
        self.detached = None
        self.file = None

        self.verbose = True
        self.chunk_size = 512

        self.create_audio()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    @ property
    def file(self):
        return self.__file

    @ file.setter
    def file(self, value):
        """
        Set the path of the audio file to read.

        Default: None (Create a new File object with no setting)

        When you use it function the file existence and require permission's will be tested.

        :param value: The File object to store
        :type value: glxaudio.file.File
        :raise TypeError: When value parameter is not a `glxaudio.file.File` type or `None`
        """
        if value is None:
            self.__file = File()
            return
        if not isinstance(value, File):
            raise TypeError("'file' property value must be a File type or None")
        if self.file != value:
            self.__file = value

    @property
    def duration_start(self):
        """
        Get the time when play sound has start. It's use internally for report statistic's

        :return: Unix time
        :rtype: int
        """
        return self.__duration_start

    @duration_start.setter
    def duration_start(self, value):
        if self.duration_start != value:
            self.__duration_start = value

    @property
    def detached(self):
        """
        Return the number of channels as set by Audio.set_channel()

        :return: False is disable, True if enable
        :rtype: bool
        """
        return self.__detached

    @detached.setter
    def detached(self, value):
        """
        Set the Player will play sound on a detached thread.

        Note: In call back no debug information's are available

        Default True

        :param value: False for disable
        :type value: bool
        :raise TypeError: when ``value`` is not a bool type or None
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'value' must be a bool type")
        if self.detached != bool(value):
            self.__detached = bool(value)

    def callback(self, _, frame_count, __, ___):
        """
        Internat funtion it play
        """
        # Display
        if self.verbose and self.duration_start:
            viewer.write(
                column_1=str(sec2time(time.time() - self.duration_start)),
                status_text="PLAY",
                status_text_color="GREEN",
                status_symbol=">",
                prompt=True,
            )

        data = self.wave.readframes(frame_count)

        flag = pyaudio.paContinue

        # if self.wav.getnframes() == self.wave.tell():
        #     flag = pyaudio.paComplete

        return data, flag

    def play_detached(self, output_device_index=None):
        """
        PLay a sound over a callback, in a detached Thread.

        That is done automatically by PyAudio.

        :return: Time it have take for play the audio file
        :rtype: int
        """
        # instantiate PyAudio via self.get_new_audio()
        if output_device_index is None:
            output_device_index = self.get_sysdefault_id()

        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            output_device_index=output_device_index,
            stream_callback=self.callback,
        )

        # start the stream
        self.duration_start = time.time()
        self.stream_start()

        # wait for stream to finish
        if self.debug:
            viewer.write(
                column_1=self.__class__.__name__ + str(":"),
                column_2="play " + str(self.file.path),
            )
        while self.stream.is_active():
            pass

        if self.verbose:
            viewer.flush_a_new_line()

        # Close Stream Pyaudio and Wave
        self.stream_close()
        self.close_pyaudio()
        self.close_wave()

        return time.time() - self.duration_start

    def play_normal(self, output_device_index=None):
        """
        Play a sound.

        :return: Time it have take for play the audio file
        :rtype: int
        """
        if output_device_index is None:
            output_device_index = self.get_sysdefault_id()

        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            output_device_index=output_device_index,
        )

        self.stream_start()
        self.duration_start = time.time()
        if self.debug:
            viewer.write(column_1=self.__class__.__name__ + str(":"), column_2="play")

        data = self.wave.readframes(self.chunk_size)

        while len(data) > 0:
            if len(data) > 0:
                self.stream.write(data)
            else:
                pass
            data = self.wave.readframes(self.chunk_size)
            # Display
            if self.verbose:
                # /tmp/tmpRqQsrP Wav,16 bit int,Mono,16KHz,29K
                viewer.write(
                    column_1=str(sec2time(time.time() - self.duration_start)),
                    status_text="PLAY",
                    status_text_color="GREEN",
                    status_symbol=">",
                    prompt=True,
                )

        if self.verbose:
            viewer.flush_a_new_line()

        if self.debug:
            viewer.write(column_1=self.__class__.__name__ + str(":"), column_2="stop")
            viewer.flush_a_new_line()

        # Close Stream Pyaudio and Wave
        self.stream_close()
        self.close_pyaudio()
        self.close_wave()

        return time.time() - self.duration_start

    def play(self, output_device_index=None):
        """
        Wrapper function for play in detached thread or not.

        If you let filename=None and have all ready set a
        ``wave_path`` with AudioPlayer.set_wave_path(), the function
        will use AudioPlayer.wave_path as file. It permit to call it function without parameter.

        See: AudioPlayer.set_is_detached() for have influence on the choose

        :param output_device_index: a  index id as returned by pyaudio or None for get the \
                sysdefault id
        :type output_device_index: int or None
        """
        if self.file.path is None:
            raise EnvironmentError("'AudioPlayer.file.path' must be set before user play() function")

        self.wave = wave.open(self.file.path, "rb")

        # Set the format
        self.format = pyaudio.get_format_from_width(self.wave.getsampwidth())

        # Set the channel number
        self.channels = self.wave.getnchannels()

        # Set the Frame Rate
        self.rate = self.wave.getframerate()

        self.get_wave_informations(self.file.path)

        if self.detached:
            if self.debug:
                viewer.write(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="detached mode is enable",
                )
            duration = self.play_detached(output_device_index=output_device_index)
        else:
            if self.debug:
                viewer.write(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="detached mode is disable",
                )
            duration = self.play_normal(output_device_index=output_device_index)

        return duration
