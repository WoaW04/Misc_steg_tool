from math import sin, pi
from random import random
from contextlib import closing
from itertools import cycle, chain
from array import array
import wave

FREQ_VIS_BIT1 = 1100
FREQ_SYNC = 1200
FREQ_VIS_BIT0 = 1300
FREQ_BLACK = 1500
FREQ_VIS_START = 1900
FREQ_WHITE = 2300
FREQ_RANGE = FREQ_WHITE - FREQ_BLACK
FREQ_FSKID_BIT1 = 1900
FREQ_FSKID_BIT0 = 2100

MSEC_VIS_START = 300
MSEC_VIS_SYNC = 10
MSEC_VIS_BIT = 30
MSEC_FSKID_BIT = 22


class SSTV(object):

    def __init__(self, image, samples_per_sec, bits):
        self.image = image
        self.samples_per_sec = samples_per_sec
        self.bits = bits
        self.vox_enabled = False
        self.fskid_payload = ''
        self.nchannels = 1
        self.on_init()

    def on_init(self):
        pass

    BITS_TO_STRUCT = {8: 'b', 16: 'h'}

    def write_wav(self, filename):
        """writes the whole image to a Microsoft WAV file"""
        fmt = self.BITS_TO_STRUCT[self.bits]
        data = array(fmt, self.gen_samples())
        if self.nchannels != 1:
            data = array(fmt, chain.from_iterable(
                zip(*([data] * self.nchannels))))
        with closing(wave.open(filename, 'wb')) as wav:
            wav.setnchannels(self.nchannels)
            wav.setsampwidth(self.bits // 8)
            wav.setframerate(self.samples_per_sec)
            wav.writeframes(data)

    def gen_samples(self):
        """generates discrete samples from gen_values()

           performs quantization according to
           the bits per sample value given during construction
        """
        max_value = 2 ** self.bits
        alias = 1 / max_value
        amp = max_value // 2
        lowest = -amp
        highest = amp - 1
        alias_cycle = cycle((alias * (random() - 0.5) for _ in range(1024)))
        for value, alias_item in zip(self.gen_values(), alias_cycle):
            sample = int(value * amp + alias_item)
            yield (lowest if sample <= lowest else
                sample if sample <= highest else highest)

    def gen_values(self):
        """generates samples between -1 and +1 from gen_freq_bits()

           performs sampling according to
           the samples per second value given during construction
        """
        spms = self.samples_per_sec / 1000
        offset = 0
        samples = 0
        factor = 2 * pi / self.samples_per_sec
        sample = 0
        for freq, msec in self.gen_freq_bits():
            samples += spms * msec
            tx = int(samples)
            freq_factor = freq * factor
            for sample in range(tx):
                yield sin(sample * freq_factor + offset)
            offset += (sample + 1) * freq_factor
            samples -= tx

    def gen_freq_bits(self):
        """generates tuples (freq, msec) that describe a sine wave segment

           frequency "freq" in Hz and duration "msec" in ms
        """
        if self.vox_enabled:
            for freq in (1900, 1500, 1900, 1500, 2300, 1500, 2300, 1500):
                yield freq, 100
        yield FREQ_VIS_START, MSEC_VIS_START
        yield FREQ_SYNC, MSEC_VIS_SYNC
        yield FREQ_VIS_START, MSEC_VIS_START
        yield FREQ_SYNC, MSEC_VIS_BIT  # start bit
        vis = self.VIS_CODE
        num_ones = 0
        for _ in range(7):
            bit = vis & 1
            vis >>= 1
            num_ones += bit
            bit_freq = FREQ_VIS_BIT1 if bit == 1 else FREQ_VIS_BIT0
            yield bit_freq, MSEC_VIS_BIT
        parity_freq = FREQ_VIS_BIT1 if num_ones % 2 == 1 else FREQ_VIS_BIT0
        yield parity_freq, MSEC_VIS_BIT
        yield FREQ_SYNC, MSEC_VIS_BIT  # stop bit
        yield from self.gen_image_tuples()
        for fskid_byte in map(ord, self.fskid_payload):
            for _ in range(6):
                bit = fskid_byte & 1
                fskid_byte >>= 1
                bit_freq = FREQ_FSKID_BIT1 if bit == 1 else FREQ_FSKID_BIT0
                yield bit_freq, MSEC_FSKID_BIT

    def gen_image_tuples(self):
        return []

    def add_fskid_text(self, text):
        self.fskid_payload += '\x20\x2a{0}\x01'.format(
                ''.join(chr(ord(c) - 0x20) for c in text))

    def horizontal_sync(self):
        yield FREQ_SYNC, self.SYNC


def byte_to_freq(value):
    return FREQ_BLACK + FREQ_RANGE * value / 255

##########################################################################################################

class GrayscaleSSTV(SSTV):
    def on_init(self):
        self.pixels = self.image.convert('LA').load()

    def gen_image_tuples(self):
        for line in range(self.HEIGHT):
            yield from self.horizontal_sync()
            yield from self.encode_line(line)

    def encode_line(self, line):
        msec_pixel = self.SCAN / self.WIDTH
        image = self.pixels
        for col in range(self.WIDTH):
            pixel = image[col, line]
            freq_pixel = byte_to_freq(pixel[0])
            yield freq_pixel, msec_pixel


class Robot8BW(GrayscaleSSTV):
    VIS_CODE = 0x02
    WIDTH = 160
    HEIGHT = 120
    SYNC = 7
    SCAN = 60


class Robot24BW(GrayscaleSSTV):
    VIS_CODE = 0x0A
    WIDTH = 320
    HEIGHT = 240
    SYNC = 7
    SCAN = 93

MODES = (Robot8BW, Robot24BW)

##########################################################################################################

from itertools import chain
from enum import Enum


class Color(Enum):
    red = 0
    green = 1
    blue = 2


class ColorSSTV(GrayscaleSSTV):
    def on_init(self):
        self.pixels = self.image.convert('RGB').load()

    def encode_line(self, line):
        msec_pixel = self.SCAN / self.WIDTH
        image = self.pixels
        for color in self.COLOR_SEQ:
            yield from self.before_channel(color)
            for col in range(self.WIDTH):
                pixel = image[col, line]
                freq_pixel = byte_to_freq(pixel[color.value])
                yield freq_pixel, msec_pixel
            yield from self.after_channel(color)

    def before_channel(self, color):
        return []

    after_channel = before_channel


class MartinM1(ColorSSTV):
    COLOR_SEQ = (Color.green, Color.blue, Color.red)
    VIS_CODE = 0x2c
    WIDTH = 320
    HEIGHT = 256
    SYNC = 4.862
    SCAN = 146.432
    INTER_CH_GAP = 0.572

    def before_channel(self, color):
        if color is Color.green:
            yield FREQ_BLACK, self.INTER_CH_GAP

    def after_channel(self, color):
        yield FREQ_BLACK, self.INTER_CH_GAP


class MartinM2(MartinM1):
    VIS_CODE = 0x28
    WIDTH = 160
    SCAN = 73.216


class ScottieS1(MartinM1):
    VIS_CODE = 0x3c
    SYNC = 9
    INTER_CH_GAP = 1.5
    SCAN = 138.24 - INTER_CH_GAP

    def horizontal_sync(self):
        return []

    def before_channel(self, color):
        if color is Color.red:
            yield from MartinM1.horizontal_sync(self)
        yield FREQ_BLACK, self.INTER_CH_GAP


class ScottieS2(ScottieS1):
    VIS_CODE = 0x38
    SCAN = 88.064 - ScottieS1.INTER_CH_GAP
    WIDTH = 160


class Robot36(ColorSSTV):
    VIS_CODE = 0x08
    WIDTH = 320
    HEIGHT = 240
    SYNC = 9
    INTER_CH_GAP = 4.5
    Y_SCAN = 88
    C_SCAN = 44
    PORCH = 1.5
    SYNC_PORCH = 3
    INTER_CH_FREQS = [None, FREQ_WHITE, FREQ_BLACK]

    def on_init(self):
        self.yuv = self.image.convert('YCbCr').load()

    def encode_line(self, line):
        pixels = [self.yuv[col, line] for col in range(self.WIDTH)]
        channel = 2 - (line % 2)
        y_pixel_time = self.Y_SCAN / self.WIDTH
        uv_pixel_time = self.C_SCAN / self.WIDTH
        return chain(
                [(FREQ_BLACK, self.SYNC_PORCH)],
                ((byte_to_freq(p[0]), y_pixel_time) for p in pixels),
                [(self.INTER_CH_FREQS[channel], self.INTER_CH_GAP),
                    (FREQ_VIS_START, self.PORCH)],
                ((byte_to_freq(p[channel]), uv_pixel_time) for p in pixels))


MODES = (MartinM1, MartinM2, ScottieS1, ScottieS2, Robot36)
