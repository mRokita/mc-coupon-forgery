#!/usr/bin/python3
from io import BytesIO
from random import choice

from datetime import datetime, timedelta
from time import strftime

from flask import Flask, send_file
from PIL import Image, ImageFont, ImageDraw

app = Flask(__name__)


def write_text(draw, x, y, text, font):
    text_size = font.getsize(text)
    draw.rectangle(((x, y), (x+text_size[0]+20, y+30)), fill="white")
    draw.text((x, y), text, (0, 0, 0), font=font)


def create_coupon(date, code):
    src = Image.open("mc.jpg")
    font = ImageFont.truetype("opensans.ttf", size=22)
    draw = ImageDraw.Draw(src)
    date_x = 242
    date_y = 355
    code_x = 242
    code_y = 388
    write_text(draw, date_x, date_y, date, font)
    write_text(draw, code_x, code_y, code, font)
    return src


def generate_random_coupon():
    date = datetime.strftime(datetime.today()-timedelta(days=1), "%d-%m-%Y")
    code = ''.join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for i in range(12)])
    src = create_coupon(date, code)
    return src


@app.route('/')
def index():
    img_io = BytesIO()
    src = generate_random_coupon()
    src.save(img_io, format="JPEG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run('0.0.0.0', '6969')
