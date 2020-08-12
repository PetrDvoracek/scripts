#!/home/pedro/Venv/3.7/bin/python
import click
import os
import cv2
import xml.etree.ElementTree as ET

@click.command()
@click.argument('directory')
@click.argument('xmin')
@click.argument('xmax')
@click.argument('ymin')
@click.argument('ymax')
@click.option('--extension', default='tif', help='image extension')
def crop(directory, xmin, xmax, ymin, ymax, extension):
    xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)
    directory = os.path.abspath(directory)

    files = [x for x in os.listdir(directory)]
    files = list(map(lambda x: os.path.join(directory, x), files))
    files_xml = list(filter(lambda x : x.split('.')[-1] == 'xml', files))
    files_img = list(filter(lambda x : x.split('.')[-1] == extension, files))

    for img_file in files_img:
        img = cv2.imread(img_file)
        img = img[ymin:ymax, xmin:xmax]

        xml_file = img_file.split('.')
        xml_file[-1] = '.xml'
        xml_file = ''.join(xml_file)
        
        xml_tree = ET.parse(xml_file)
        xml = xml_tree.getroot()

        xml_width = xml.find('./size/width').text
        xml_width_before = xml_width
        assert int(xml_width) > (xmin + (int(xml_width) - xmax)), f'xmin + (WIDTH - xmax) cannot be greater than xml annotation width {xml_width}'
        xml.find('./size/width').text = str(int(xml_width) - xmin - (int(xml_width) - xmax))

        xml_height = xml.find('./size/height').text
        xml_height_before = xml_height
        assert int(xml_height) > (ymin + (int(xml_height) - ymax)), f'ymin + (HEIGHT - ymax) cannot be greater than xml annotation height {xml_height}'
        xml.find('./size/height').text = str(int(xml_height) - ymin - (int(xml_height) - ymax))

        annotations = xml.findall('./object/bndbox')
        for annot in annotations:
            an_xmin, an_xmax = annot.find('./xmin'), annot.find('./xmax')
            an_ymin, an_ymax = annot.find('./ymin'), annot.find('./ymax')
            assert int(int(an_xmin.text)) > xmin, f'annotaion cropped! use smaller xmin (<{an_xmin.text})'
            assert int(int(an_xmax.text)) < xmax, f'annotation cropped! use greater xmax (>{an_xmax.text})'
            assert int(int(an_ymin.text)) > ymin, f'annotation cropped! use smaller ymin (<{an_ymin.text})'
            assert int(int(an_ymax.text)) < ymax, f'annotation cropped! use greater ymax (>{an_ymax.text})'

            an_xmin.text = str(int(an_xmin.text) - xmin)
            an_xmax.text = str(int(an_xmax.text) - xmin)
            an_ymin.text = str(int(an_ymin.text) - ymin)
            an_ymax.text = str(int(an_ymax.text) - ymin)


        cv2.imwrite(img_file, img)
        xml_tree.write(xml_file)



if __name__ == '__main__':
    crop()