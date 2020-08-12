#!/home/pedro/Venv/3.7/bin/python
import xml.etree.ElementTree as ET
import os
import click
import cv2

@click.command()
@click.argument('input-file')
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--extension', default='tif', help='image format')
def rescale(input_file, width, height, extension):
    directory = os.path.abspath(input_file)

    imgs = [x for x in os.listdir(directory) if x.split('.')[-1] == extension]
    for img_path in imgs:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (width, height))
        status = cv2.imwrite(img_path, img)
        print(f'saved? {status}')

if __name__ == '__main__':
    rescale()