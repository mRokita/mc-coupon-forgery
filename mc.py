#!/usr/bin/python3
from io import BytesIO
from random import choice

from datetime import datetime, timedelta
from time import strftime

from flask import Flask, send_file, abort
from PIL import Image, ImageFont, ImageDraw

app = Flask(__name__)


def write_text(draw, x, y, text, font):
    text_size = font.getsize(text)
    draw.rectangle(((x, y), (x+text_size[0]+20, y+30)), fill="white")
    draw.text((x, y), text, (0, 0, 0), font=font)


def create_coupon(date, code, coupon_type):
    file = None
    if coupon_type == "fryty":
        file = "mc_fryty.jpg"
    elif coupon_type == "cheese":
        file = "mc_cheese.jpg"
    elif coupon_type == "burger":
        file = "mc.jpg"
    src = Image.open(file)
    font = ImageFont.truetype("opensans.ttf", size=22)
    draw = ImageDraw.Draw(src)
    date_x = 242
    date_y = 355
    code_x = 242
    code_y = 388
    write_text(draw, date_x, date_y, date, font)
    write_text(draw, code_x, code_y, code, font)
    return src


def generate_random_coupon(coupon_type):
    date = datetime.strftime(datetime.today()-timedelta(days=1), "%d-%m-%Y")
    code = ''.join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for i in range(12)])
    src = create_coupon(date, code, coupon_type)
    return src


@app.route('/<coupon_type>.jpg')
def coupon(coupon_type):
    if coupon_type not in ("fryty", "burger", "cheese"):
        abort(404)
    img_io = BytesIO()
    src = generate_random_coupon(coupon_type)
    src.save(img_io, format="JPEG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


@app.route('/')
def index():
    return '<html><head><title>Kupony do mc</title><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><a href="/burger.jpg"><h4>Hamburger/Lody<h4></a><a href="/cheese.jpg"><h4>Cheeseburger<h4></a><a href="/fryty.jpg"><h4>Frytki<h4></a></body></html>'

if __name__ == "__main__":
    app.run('0.0.0.0', '6969')
