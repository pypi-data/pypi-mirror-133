import struct


class SerialReader:
    def __init__(self, data, initial_position=0):
        self.pointer = initial_position
        self.data = data

    def read(self, format_chars):
        """ Read format_chars from the data """

        is_one_value = len(format_chars) == 1
        size = struct.calcsize(format_chars)
        if format_chars[0] != "=":
            format_chars = "=" + format_chars
        values = struct.unpack(
            format_chars, self.data[self.pointer : self.pointer + size]
        )
        self.pointer += size
        if is_one_value:
            return values[0]
        return values

    def read_rest(self, format_char):
        format_size = struct.calcsize(format_chars)
        remaining_data_size = len(self.data) - self.pointer
        if remaining_data_size % format_size != 0:
            print(
                "WARNING: format_char does not align with remaining data in read_rest"
            )
        computed_format_chars = remaining_data_size // format_size
        return read(computed_format_chars)

    def read_raw(self, no_of_bytes=1):
        raw_bytes = self.data[self.pointer : self.pointer + no_of_bytes]
        self.pointer += no_of_bytes
        return raw_bytes

    def read_rest_raw(self):
        return self.data[self.pointer :]

    def reset_pointer(self, pos=0):
        self.pointer = pos
