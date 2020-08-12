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
    for img_name in imgs:
        img_path = os.path.join(directory, img_name)
        xml_name = img_name.split('.')
        xml_name[-1] = '.xml'
        xml_name = ''.join(xml_name)
        xml_path = os.path.join(directory, xml_name)
        if not os.path.exists(xml_path):
            print(f'voc dos not exist! {xml_path}')
            continue
        try:
            img = cv2.imread(img_name)
            img = cv2.resize(img, (width, height))
            width_before = img.shape[1]
            height_before = img.shape[0]


            xml_tree = ET.parse(xml_path)
            xml = xml_tree.getroot()
            xml.find('./size/width').text = str(width)
            xml.find('./size/height').text = str(height)

            annotations = xml.findall('./object/bndbox')
            for annot in annotations:
                an_xmin, an_xmax = annot.find('./xmin'), annot.find('./xmax')
                an_ymin, an_ymax = annot.find('./ymin'), annot.find('./ymax')
                an_xmin.text = str(round(int(an_xmax.text) * ( width / width_before )))
                an_xmax.text = str(round(int(an_xmax.text) * ( width / width_before )))
                an_ymin.text = str(round(int(an_ymin.text) * ( height / height_before )))
                an_ymax.text = str(round(int(an_ymax.text) * ( height / height_before )))
            xml_tree.write(xml_path)
            status = cv2.imwrite(img_name, img)
            print(f'saved? {status}')
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    rescale()