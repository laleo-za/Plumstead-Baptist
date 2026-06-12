from PIL import Image
import os

def make_favicon(input_path, output_path=None):
    # Default output: same folder, name = favicon.png
    if output_path is None:
        base = os.path.dirname(input_path)
        output_path = os.path.join(base, "favicon.png")

    img = Image.open(input_path)

    # Convert to RGBA for transparency support
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Resize to 32x32 while preserving aspect ratio
    img.thumbnail((32, 32), Image.LANCZOS)

    # Create a 32x32 transparent canvas
    canvas = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    x = (32 - img.width) // 2
    y = (32 - img.height) // 2

    # Paste resized image onto the canvas
    canvas.paste(img, (x, y), img)

    # Save as PNG (best for favicons)
    canvas.save(output_path, format="PNG")
    print(f"Favicon saved as: {output_path}")


if __name__ == "__main__":
    input_file = r"C:\Users\djoli\Source\repos\Plumstead Baptist\static\images\PBC logo favicon.png"   # <-- CHANGE THIS
    make_favicon(input_file)
