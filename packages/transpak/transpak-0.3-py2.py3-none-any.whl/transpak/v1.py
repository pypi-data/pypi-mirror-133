import struct
import zlib
import numpy as np
from .SerialReader import SerialReader

PAK_VERSION = 1


def pack_data(data_list, samplerate):
    versions = []
    data_lengths = []
    data_paks = []
    for data in data_list:
        paksizes = []
        paks_temp = []
        # for ver in (1, 2, 3, 4):
        for ver in (1, 2):
            pak = pack_wave(ver, data, samplerate)
            pak_compressed = zlib.compress(pak)
            paks_temp.append(pak_compressed)
            paksizes.append(len(pak_compressed))
        best_version_index = paksizes.index(min(paksizes))
        data_lengths.append(min(paksizes))
        data_paks.append(paks_temp[best_version_index])
        versions.append((1, 2, 3, 4)[best_version_index])
    return versions, data_lengths, data_paks


def pack_wave(version, data, samplerate):
    if version == 1:
        pack = struct.pack(f"{len(data)}f", *data)
    elif version == 2:
        diff_data = np.diff(data)
        pack = struct.pack(f"{len(data)}f", data[0], *diff_data)
    return pack


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
):

    pack = struct.pack("H", PAK_VERSION)
    pack += struct.pack("Q", int(ms_timestamp))
    pack += struct.pack("I", int(samplerate))
    pack += struct.pack("I", data_list[0].size)
    pack += struct.pack("d", peak)
    pack += struct.pack("d", maxdeviation)
    pack += struct.pack("H", calc_affected_channels_code(affected_channels))

    versions, data_lengths, data_paks = pack_data(data_list, samplerate)
    pack += struct.pack("8I", *data_lengths)
    pack += struct.pack("8H", *versions)

    for data_pak in data_paks:
        pack += data_pak

    return pack


def unpack(packed_data, only_metadata=False):

    data = SerialReader(packed_data)
    pak_version = data.read("H")

    metadata = {}
    metadata["ms_timestamp"] = data.read("Q")
    metadata["samplerate"] = data.read("I")
    metadata["no_of_samples"] = data.read("I")
    metadata["maxvoltage"] = data.read("d")
    metadata["maxdeviation"] = data.read("d")
    metadata["affected_channels"] = data.read("H")

    if only_metadata:
        return metadata

    data_lengths = data.read("8I")
    versions = data.read("8H")
    data_list = []
    for length, version in zip(data_lengths, versions):
        data_buffer = zlib.decompress(packed_data[data.pointer : data.pointer + length])
        if version == 1:
            data_list.append(np.frombuffer(data_buffer, dtype=np.float32))
        elif version == 2:
            data0 = np.array(struct.unpack("f", data_buffer[:4]))
            data_rest = data0 + np.cumsum(
                np.frombuffer(data_buffer, dtype=np.float32, offset=4)
            )
            data_list.append(np.concatenate((data0, data_rest)))
        elif version == 3 or version == 4:
            u_recr = unpack3(data_buffer)
            data_list.append(u_recr)
        data.pointer += length

    return data_list, metadata
