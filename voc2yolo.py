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

    for xml_file in files_xml:
        xml_tree = ET.parse(xml_file)
        xml = xml_tree.getroot()

        width = int(xml.find('./size/width').text)
        height = int(xml.find('./size/height').text)

        txt_file = xml_file.split('.')
        txt_file[-1] = '.txt'
        txt_file = ''.join(txt_file)


        with open(txt_file, 'w') as f:
            for annot in xml.findall('./object'):
                xmin, xmax = int(annot.find('./bndbox/xmin').text), int(annot.find('./bndbox/xmax').text)
                ymin, ymax = int(annot.find('./bndbox/ymin').text), int(annot.find('./bndbox/ymax').text)
                ann_class = annot.find('./name').text
                if ann_class == 'x':
                    ann_class = '10'
                x = (xmin + (xmax - xmin)) / width
                y = (ymin + (ymax - ymin)) / height
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height
                assert x > 0
                assert y > 0
                assert w > 0
                assert h > 0
                f.write(f'{ann_class} {x} {y} {w} {h}\n')


if __name__ == '__main__':
    convert()