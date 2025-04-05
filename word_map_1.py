from PIL import Image, ImageDraw, ImageFont
import random
import json
import os

# Define the font directories
font_dirs = ['/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts')]

# Find all .ttf and .otf files
# List of Unicode-compliant fonts known to support a wide character set
unicode_fonts = [
    "DejaVu Sans",
    "DejaVu Sans Mono",
    "DejaVu Serif",
    "DejaVu Serif Mono",
    "Noto Sans",
    "Noto Serif",
    "Noto Sans CJK",
    "Noto Sans Symbol",
    "Noto Sans Emoji",
    "Liberation Sans",
    "Liberation Serif",
    "Liberation Mono",
    "Ubuntu",
    "Ubuntu Mono",
    "FreeSans",
    "FreeSerif",
    "FreeMono",
    "Cantarell",
    "Roboto",
    "Roboto Mono",
    "Roboto Slab",
    "Source Sans Pro",
    "Source Serif Pro",
    "Source Code Pro",
    "Symbola",
    "M+ 1m",
    "M+ 1p",
    "M+ 2m",
    "Arimo",
    "STIX General",
    "STIX Math",
    "Luxi Sans",
    "Luxi Serif",
    "Luxi Mono",
    "Tamsyn",
    "Cairo",
    "Zapfino",
    "Bitstream Vera Sans",
    "Bitstream Vera Serif",
    "Bitstream Vera Mono"
]

# Find all .ttf and .otf files and filter those that are likely to support UTF-8
fonts = []
for font_dir in font_dirs:
    for root, _, files in os.walk(font_dir):
        for file in files:
            if file.endswith('.ttf') or file.endswith('.otf'):
                # Check if the font name matches a known Unicode font
                if any(font in file for font in unicode_fonts):
                    fonts.append(os.path.join(root, file))

# Use a font
#if fonts:
#    font_path = fonts[0]  # Pick the first font from the list
#    font = ImageFont.truetype(font_path, size=30)
#    print(f"Using font: {font_path}")

artist = 'Queen'
folder=f'LYRICS_{artist}'
# Specify the file path where the dictionary is saved
file_path = f'{folder}/Word_dictionary_{artist}.json'

# Read the dictionary from the JSON file
with open(file_path, 'r') as file:
    loaded_dict = json.load(file)

print(f"Dictionary loaded: {len(loaded_dict)} words in total.")


width, height = 1000, 1000
big_image = Image.new('RGB', (width, height), 'black')
draw = ImageDraw.Draw(big_image)


##### CODE FOF VECTOR SEARCH ######
occupied_pixels = [[False] * width for _ in range(height)]

#def place_word(image, word, font, color, occupied_pixels):
#    # Get word size (bounding box)
#    word_width, word_height = ImageDraw.Draw(image).textsize(word, font=font)
#    
#    # Try placing the word until a valid position is found
#    attempts = 0
#    while attempts < 100:
#        attempts += 1
#        
#        # Generate random position (x, y) for the word's top-left corner
#        x = random.randint(0, image.width - word_width)
#        y = random.randint(0, image.height - word_height)
#        
#        # Check if the word's area intersects with occupied pixels
#        overlap = False
#        for i in range(word_width):
#            for j in range(word_height):
#                if occupied_pixels[y + j][x + i]:
#                    overlap = True
#                    break
#            if overlap:
#                break
#        
#        if not overlap:
#            # Draw the word on the image
#            ImageDraw.Draw(image).text((x, y), word, font=font, fill=color)
#            
#            # Mark the pixels as occupied in the occupied_pixels matrix
#            for i in range(word_width):
#                for j in range(word_height):
#                    occupied_pixels[y + j][x + i] = True
#            
#            return True  # Word placed successfully
#    
#    return False  # Failed to place the word after multiple attempts
#
####################################################################################


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def put_word_into_text(text, size=50, rotation=0, font='LiberationSans-Regular.ttf', color='black', place=(0,0)):
    
    #my_result = textsize(text, font)
#
    #word_width = my_result[0]
    #word_height = my_result[1]


    font = ImageFont.truetype(font=font, size=size)
    text_image = Image.new('RGBA', textsize(text, font), (0,0,0,0))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0,0), text, font=font, fill=color)    
    rotated_text_image = text_image.rotate(rotation, expand=1)

    word_width = round(text_draw.textlength(text, font))
    word_height = size

    x = random.randint(0, width - word_width)
    y = random.randint(0, height - word_height)

    #word_width, word_height = rotated_text_image.textsize(word, font=font)
    #y = place[1] - word_height
    #x = place[0] - word_width

 
    # Try placing the word until a valid position is found
    attempts = 0
    while attempts < 100:
        attempts += 1
        overlap = False
        for i in range(word_width):
            for j in range(word_height):
                if occupied_pixels[y + j][x + i]:
                    overlap = True
                    break
            if overlap:
                break
            
        if not overlap:
            # Draw the word on the image
            big_image.paste(rotated_text_image, (x,y), rotated_text_image)
            
            # Mark the pixels as occupied in the occupied_pixels matrix
            for i in range(word_width):
                for j in range(word_height):
                    occupied_pixels[y + j][x + i] = True
            
            return True  # Word placed successfully

        return False  # Failed to place the word after multiple attempts
            

for word, count in loaded_dict.items() :
    #rand_locx=random.randrange(1000)
    #rand_locy=random.randrange(1000)
    #random_location = [rand_locx,rand_locy]
    random_rotation = random.choice([0,90,180,270])
    random_color = random.choice(['white','blue','green','red','yellow','purple'])
    random_font = random.choice(fonts)
    size = round(count/2) if count/5 > 1 else 1
    if not put_word_into_text(word,size,random_rotation,font=random_font,color=random_color):
        print(f"Failed to place word: {word}")

#put_word_into_text('Hello Everybody!',55,20,place=(50,50))
#put_word_into_text('How are you doing?',40,45,place=(70,300))
#put_word_into_text('Is everything good?',30,90,place=(500,300))
#put_word_into_text('OH YEAH!',100,270,place=(900,500))   

big_image.show()