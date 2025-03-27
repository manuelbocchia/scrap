from PIL import Image, ImageDraw, ImageFont
from random import Random

width, height = 1000, 1000
big_image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(big_image)


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def put_word_into_text(text, size=50, rotation=0, font='LiberationSans-Regular.ttf', color='black', place=(0,0)):
    
    font = ImageFont.truetype(font=font, size=size)
    text_image = Image.new('RGBA', textsize(text, font), (0,0,0,0))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0,0), text, font=font, fill=color)    
    rotated_text_image = text_image.rotate(rotation, expand=1)
    big_image.paste(rotated_text_image, place, rotated_text_image)

put_word_into_text('Hello Everybody!',55,20,place=(50,50))
put_word_into_text('How are you doing?',40,45,place=(70,300))
put_word_into_text('Is everything good?',30,90,place=(500,300))
put_word_into_text('OH YEAH!',100,270,place=(900,500))   

big_image.show()