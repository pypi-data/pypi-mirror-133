""" Version 4 of the transpak format
- ready for up to 16 channels (number is variable)
- diff-packing only
- zlib-compression of all channels together
- Encode channel names with '\t' as separator
"""

import struct
import zlib
import functools
import numpy as np
from .SerialReader import SerialReader


PAK_VERSION = 4


@functools.lru_cache()
def compute_ds_linspace(len_a, to):
    return np.linspace(0, len_a - 1, to, dtype=int)


def downsample(wave, to):
    pos = compute_ds_linspace(len(wave), to)
    da = wave[pos]
    return da


def calc_affected_channels_code(affected_channels, max_channels=8):
    affected_channels_code = 0
    for i in range(max_channels):
        if i in affected_channels:
            affected_channels_code += 2 ** i
    return affected_channels_code


def pack(
    data_list,
    ms_timestamp,
    samplerate,
    peak=0,
    maxdeviation=0,
    affected_channels=[],
    channel_names=[],
):
    affected_channels_code = calc_affected_channels_code(
        affected_channels, max_channels=16
    )

    if not channel_names:
        # print(f"No channel names given")
        channel_names = [""] * len(data_list)
    if len(channel_names) is not len(data_list):
        print(
            f"Different number of channels in channel_names ({len(channel_names)}) and data_list ({len(data_list)})"
        )

    pack = struct.pack("H", int(PAK_VERSION))
    pack += struct.pack("Q", int(ms_timestamp))
    pack += struct.pack("I", int(samplerate))
    pack += struct.pack("H", len(data_list))  # Number of channels
    channels_names_pack = b"\t".join(
        [ch_name.encode("utf-8") for ch_name in channel_names]
    )
    pack += struct.pack(
        "H", len(channels_names_pack)
    )  # Number of bytes in channel_names_pack
    pack += channels_names_pack
    pack += struct.pack("I", data_list[0].size)  # Number of samples per channel
    pack += struct.pack("d", peak)
    pack += struct.pack("d", maxdeviation)
    pack += struct.pack("H", int(affected_channels_code))

    # Pack data as diff and compress:
    datapack = b"".join(
        struct.pack(f"{len(data)}f", data[0], *np.diff(data)) for data in data_list
    )
    datapack = zlib.compress(datapack)

    pack += datapack

    return pack


def unpack(packed_data, only_metadata=False, downsample_to=0):

    data = SerialReader(packed_data)
    pak_version = data.read("H")

    metadata = {}
    metadata["ms_timestamp"] = data.read("Q")
    metadata["samplerate"] = data.read("I")
    metadata["no_of_channels"] = data.read("H")
    no_of_bytes_in_channel_name_pack = data.read("H")
    if no_of_bytes_in_channel_name_pack == 0:
        metadata["channel_names"] = [
            f"CH{i}" for i in range(metadata["no_of_channels"], 1)
        ]
    else:
        metadata["channel_names"] = (
            data.read_raw(no_of_bytes_in_channel_name_pack).decode("utf-8").split("\t")
        )
    metadata["no_of_samples"] = data.read("I")
    metadata["peak"] = data.read("d")
    metadata["max_deviation"] = data.read("d")
    metadata["affected_channels"] = data.read("H")

    if only_metadata:
        return metadata

    decompressed_rest = zlib.decompress(data.read_rest_raw())
    data_buffer = SerialReader(decompressed_rest)
    data_list = []
    for i in range(metadata["no_of_channels"]):
        data0 = np.array(data_buffer.read("f"))
        data_rest = data0 + np.cumsum(
            np.array(data_buffer.read(f'{metadata["no_of_samples"]-1}f'))
        )

        wave = np.concatenate((data0, data_rest), axis=None)

        if downsample_to:
            wave = downsample(wave, downsample_to)

        data_list.append(wave)

    return data_list, metadata
