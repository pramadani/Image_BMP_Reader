from PIL import Image

def bmp_convert(input_path, output_path, width=None, height=None):
    img = Image.open(input_path)

    if width != None or height != None:
        img = img.resize((width, height), Image.LANCZOS)

    img_rgb = img.convert("RGB")
    img_rgb.save(output_path, format='BMP')
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    input_path = 'images/player.png'
    output_path = 'images/player.bmp'

    bmp_convert(input_path, output_path)