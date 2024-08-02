class BMP_Reader:
    def __init__(self, filename):
        self.filename = filename
        self.width = 0
        self.height = 0
        self.offset = 0

    def _read_header(self):
        with open(self.filename, 'rb') as f:
            if f.read(2) != b'BM':
                return False  # Not a BMP file

            f.seek(10)
            self.offset = int.from_bytes(f.read(4), 'little')

            f.seek(18)
            self.width = int.from_bytes(f.read(4), 'little')
            self.height = int.from_bytes(f.read(4), 'little')

            f.seek(28)
            depth = int.from_bytes(f.read(2), 'little')
            compression = int.from_bytes(f.read(4), 'little')

            if depth != 24 or compression != 0:
                return False  # Not a 24-bit uncompressed BMP

            return True

    def to_bytes(self):
        if not self._read_header():
            return None, 0, 0

        with open(self.filename, 'rb') as f:
            rowsize = (self.width * 3 + 3) & ~3
            flip = self.height > 0
            height = abs(self.height)
            width = min(self.width, 128)
            height = min(height, 160)

            pixels = bytearray(width * height * 2)  # 2 bytes per pixel for 16-bit color

            f.seek(self.offset)
            for row in range(height):
                pos = self.offset + (height - 1 - row) * rowsize if flip else self.offset + row * rowsize
                f.seek(pos)
                for col in range(width):
                    bgr = f.read(3)
                    r, g, b = bgr[2], bgr[1], bgr[0]
                    rgb565 = self.rgb565(r, g, b)
                    index = (row * width + col) * 2
                    pixels[index:index+2] = rgb565.to_bytes(2, 'big')

            return pixels, width, height

    def to_matrix(self):
        if not self._read_header():
            return None, 0, 0

        with open(self.filename, 'rb') as f:
            rowsize = (self.width * 3 + 3) & ~3
            flip = self.height > 0
            height = abs(self.height)
            width = min(self.width, 128)
            height = min(height, 160)

            matrix = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

            f.seek(self.offset)
            for row in range(height):
                pos = self.offset + (height - 1 - row) * rowsize if flip else self.offset + row * rowsize
                f.seek(pos)
                for col in range(width):
                    b, g, r = f.read(3)
                    matrix[row][col] = (r, g, b)

            return matrix, width, height

    def to_matrix565(self):
        if not self._read_header():
            return None, 0, 0

        with open(self.filename, 'rb') as f:
            rowsize = (self.width * 3 + 3) & ~3
            flip = self.height > 0
            height = abs(self.height)
            width = min(self.width, 128)
            height = min(height, 160)

            matrix = [[0 for _ in range(width)] for _ in range(height)]

            f.seek(self.offset)
            for row in range(height):
                pos = self.offset + (height - 1 - row) * rowsize if flip else self.offset + row * rowsize
                f.seek(pos)
                for col in range(width):
                    b, g, r = f.read(3)
                    rgb565 = self.rgb565(r, g, b)
                    matrix[row][col] = rgb565

            return matrix, width, height

    @staticmethod
    def rgb565(r, g, b):
        return ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)
