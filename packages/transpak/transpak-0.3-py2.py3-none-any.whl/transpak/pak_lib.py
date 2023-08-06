import os
import time
import json
import struct
import zlib

import numpy as np

from .SerialReader import SerialReader
from . import v1
from . import v4


# Pack Functions:
# ===============


def pack(
    data_list,
    ms_timestamp,
    samplerate,
    peak=0,
    maxdeviation=0,
    affected_channels=[],
    channel_names=[],
    pak_version=4,
):

    if pak_version == 1:
        return v1.pack(
            data_list,
            ms_timestamp,
            samplerate,
            peak,
            maxdeviation,
            affected_channels=[],
        )

    elif pak_version == 4:
        return v4.pack(
            data_list,
            ms_timestamp,
            samplerate,
            peak,
            maxdeviation,
            affected_channels=[],
            channel_names=[],
        )


# Unpack Functions:
# =================


def unpack_file(filepath):
    with open(filepath, "rb") as f:
        data_list, metadata = unpack(f.read())
    return data_list, metadata


def unpack(packed_data, only_metadata=False, downsample_to=0):

    data = SerialReader(packed_data)
    pak_version = data.read("H")

    if pak_version == 1:
        return v1.unpack(packed_data, only_metadata)

    # Is version 3 still needed?
    elif pak_version == 3:
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
                data.read_raw(no_of_bytes_in_channel_name_pack)
                .decode("utf-8")
                .split("\t")
            )
        metadata["no_of_samples"] = data.read("I")
        metadata["maxvoltage"] = data.read("d")
        metadata["maxdeviation"] = data.read("d")
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
            data_list.append(np.concatenate((data0, data_rest), axis=None))

    elif pak_version == 4:
        return v4.unpack(packed_data, only_metadata, downsample_to)

    else:
        print(f"pak_version {pak_version} unknown")

    return data_list, metadata
