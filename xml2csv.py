#!/home/pedro/Venv/3.7/bin/python

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import click

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

@click.command()
@click.argument('input-folder')
@click.argument('output-file')
def main(input_folder, output_file):
    xml_df = xml_to_csv(input_folder)
    xml_df.to_csv(output_file, index=None)
    print('Successfully converted xml to csv.')

if __name__ == '__main__':
    main()