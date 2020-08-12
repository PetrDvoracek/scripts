#!/home/pedro/Venv/3.7/bin/python
import cv2
import click
from pathlib import Path
@click.command()
@click.argument('image_path', required=True)
@click.argument('width', type=int, required=True)
@click.argument('height', type=int, required=True)
def main(image_path, width, height):
    # try:
    print(image_path, width, height)
    image_path = Path(image_path)
    image_name = image_path.name
    image_folder = image_path.parent.absolute()
    
    img = cv2.imread(str(image_path))
    rescaled = cv2.resize(img, (width, height))
    save_path = f"{str(image_folder)}/rescaled_{str(image_name)}"
    was_saved = cv2.imwrite(save_path, rescaled)
    print(f"Saved? {was_saved}")
    # except:
    #     print(f"Error resizing image {image_name}")
    

if __name__ == '__main__':
    main()