#!/home/pedro/Venv/3.7/bin/python
import xml.etree.ElementTree as ET
import os
import click

@click.command()
@click.argument('input-file')
def convert(input_file):
    directory = os.path.abspath(input_file)

    files = [x for x in os.listdir(directory)]
    files = list(map(lambda x: os.path.join(directory, x), files))
    files_xml = list(filter(lambda x : x.split('.')[-1] == 'xml', files))

    with open('train.txt', 'w') as f:

        for xml_file in files_xml:
            img_file = xml_file.split('.')
            img_file[-1] = '.tif'
            img_file = ''.join(img_file)

            xml_tree = ET.parse(xml_file)
            xml = xml_tree.getroot()

            width = int(xml.find('./size/width').text)
            height = int(xml.find('./size/height').text)

            txt_file = xml_file.split('.')
            txt_file[-1] = '.txt'
            txt_file = ''.join(txt_file)
            for annot in xml.findall('./object'):
                xmin, xmax = int(annot.find('./bndbox/xmin').text), int(annot.find('./bndbox/xmax').text)
                ymin, ymax = int(annot.find('./bndbox/ymin').text), int(annot.find('./bndbox/ymax').text)
                ann_class = annot.find('./name').text
                
                f.write(f'{img_file},{xmin},{ymin},{xmax},{ymax},{ann_class}\n')


if __name__ == '__main__':
    convert()