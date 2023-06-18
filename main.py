from PIL import Image
import os

INPUT_DIRECTORY = r".\input"
OUTPUT_DIRECTORY = r".\output"

ALLOWED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp"]
REMOVED_BEZEL_X = 0.03 # 3% of the image's width will be de-bezelled around the borders by default
BLEED = 0.1562 # 31% of the image's width will be added around the borders by default


def trim_bezel(img):
    w, h = img.size
    
    # Pixels to be removed from each side of the bezel
    r_pixels = int(w * REMOVED_BEZEL_X) 
    
    # Remove the bezel and replace with black
    img = img.crop((r_pixels, r_pixels, w - r_pixels, h - r_pixels))
    trim_img = Image.new('RGB', (w, h), (0, 0, 0))
    trim_img.paste(img, (r_pixels, r_pixels))
    return trim_img

def bleed(img):
    w, h = img.size
    
    # Pixels to be added to each side of the bezel 
    add_pixels = int(w * BLEED) 
    # Remove the bezel and replace with black
    bleed_img = Image.new('RGB', (w+add_pixels, h+add_pixels), (0, 0, 0))
    bleed_img.paste(img, (add_pixels//2, add_pixels//2))
    return bleed_img

def main():
    for filename in os.listdir(INPUT_DIRECTORY):
        f = os.path.join(INPUT_DIRECTORY, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filename = os.path.split(f)[-1]
            ext = os.path.splitext(f)[-1].lower()
            if ext in ALLOWED_IMAGE_FORMATS:
                img = Image.open(f)
                trim_img = trim_bezel(img)
                bleed_img = bleed(trim_img)
                bleed_img.save(os.path.join(OUTPUT_DIRECTORY, filename))
                

if __name__ == "__main__":
    main()