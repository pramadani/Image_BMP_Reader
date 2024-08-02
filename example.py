from bmp_reader import BMP_Reader

bmp_processor = BMP_Reader('images/player.bmp')

# Convert to RGB565 byte array
pixels, width, height = bmp_processor.to_bytes()
print(f"Width: {width}, Height: {height}, Pixels: {pixels}")

# Convert to RGB matrix
matrix, width, height = bmp_processor.to_matrix()
print(f"Width: {width}, Height: {height}, Matrix: {matrix}")

# Convert to RGB565 matrix
matrix565, width, height = bmp_processor.to_matrix565()
print(f"Width: {width}, Height: {height}, Matrix565: {matrix565}")