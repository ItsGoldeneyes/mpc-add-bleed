from PIL import Image
from tqdm import tqdm
import sys
import os

INPUT_DIRECTORY = r".\input"
OUTPUT_DIRECTORY = r".\output"

ALLOWED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp"]
REMOVED_BEZEL_X = 0.01 # 1% of the image's width will be de-bezelled around the borders by default
BLEED = 0.15 # 15% of the image's width will be added around the borders by default
COLOR = (255, 255, 255) # Color to be used for the bezel removal


def trim_bezel(img):
    w, h = img.size
    
    # Pixels to be removed from each side of the bezel
    r_pixels = int(w * REMOVED_BEZEL_X) 
    
    # Remove the bezel and replace with black
    img = img.crop((r_pixels, r_pixels, w - r_pixels, h - r_pixels))
    trim_img = Image.new('RGB', (w, h), COLOR)
    trim_img.paste(img, (r_pixels, r_pixels))
    return trim_img

def bleed(img):
    w, h = img.size
    
    # Pixels to be added to each side of the bezel 
    add_pixels = int(w * BLEED) 
    # Remove the bezel and replace with black
    bleed_img = Image.new('RGB', (w+add_pixels, h+add_pixels), COLOR)
    bleed_img.paste(img, (add_pixels//2, add_pixels//2))
    return bleed_img

def main():
    for filename in tqdm(os.listdir(INPUT_DIRECTORY)):
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
    if  "--h" in sys.argv or "--help" in sys.argv:
        print(" -------- HELP PAGE -------- \
            \n-- help: Displays this page \
            \n-- input: STR - Set the input directory. default: .\input \
            \n-- output: STR - Set the output directory. default: .\output \
            \n-- bleed: FLOAT - Amount of bleed to be added. Percentage of the image width. default: 0.1562 \
            \n-- bezel: FLOAT - Amount of bezel to be removed and replaced. Percentage of the image width. default: 0.03")
    
    for i in range(len(sys.argv)):
        error = False
        
        if sys.argv[i] == "--input":
            if i == len(sys.argv) - 1:
                print("No input directory provided")
                error = True
            elif os.path.isdir(sys.argv[i+1]):
                INPUT_DIRECTORY = sys.argv[i+1]
            else:
                print("Invalid input directory")
                error = True
                
        elif sys.argv[i] == "--output":
            if i == len(sys.argv) - 1:
                print("No output directory provided")
                error = True
            elif os.path.isdir(sys.argv[i+1]):
                OUTPUT_DIRECTORY = sys.argv[i+1]
            else:
                print("Invalid output directory")
                error = True
                
        elif sys.argv[i] == "--bleed":
            if i == len(sys.argv) - 1:
                print("No bleed value provided")
                error = True
            elif not sys.argv[i+1].replace('.','',1).isdecimal() or float(sys.argv[i+1]) > 10 or float(sys.argv[i+1]) < 0:
                print("Bleed value must be a float between 0 and 10")
                error = True
            else: 
                BLEED = float(sys.argv[i+1])
            
        elif sys.argv[i] == "--bezel":
            if i == len(sys.argv) - 1:
                print("No bezel removal value provided")
                error = True
            elif not sys.argv[i+1].replace('.','',1).isdecimal() or float(sys.argv[i+1]) > 0.5 or float(sys.argv[i+1]) < 0:
                print("Bezel removal value must be a float between 0 and 0.5")
                error = True
            else:
                REMOVED_BEZEL_X = float(sys.argv[i+1])
        
    if not error:
        main()
        
    print(sys.argv)