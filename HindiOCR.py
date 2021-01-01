import gc
import easyocr
import torch
import os
import glob
from PIL import Image


def process_image(imgpath):

    jsonpath = imgpath.replace(".jpg", ".json")

    if not os.path.isfile(jsonpath):
        print()
        print()
        print("Processing image {%s}" % imgpath)
        im = Image.open(imgpath)
        width, height = im.size

        newsize = (635, 900)
        im1 = im.resize(newsize)

        if os.path.isfile('page.jpg'):
            os.remove('page.jpg')

        im1.save('page.jpg')

        reader = easyocr.Reader(['hi', 'en'])
        result = reader.readtext('page.jpg', paragraph=True)

        with open(jsonpath, "wb") as f:

            f.write('{'.encode("UTF-8"))

            no = imgpath.replace('page', '').replace('.jpg', '')

            f.write(('"no": %s, ' % no).encode("UTF-8"))

            f.write(('"height": %d, ' % height).encode("UTF-8"))
            f.write(('"width": %d, ' % width).encode("UTF-8"))

            f.write('"imgsrc": "", '.encode("UTF-8"))

            f.write('"paras" : ['.encode("UTF-8"))

            for item in result:
                l = int(item[0][0][0])
                t = int(item[0][0][1])
                r = int(item[0][2][0])
                b = int(item[0][2][1])

                f.write(('{\"l\": % d, \"t\": % d, \"w\": % d, \"h\": % d, \"hi\": \"%s\"}, ' %
                         (l, t, r-l, b-t, item[1].replace('"', '&quot;'))).encode("UTF-8"))

            f.write('], '.encode("UTF-8"))

            f.write('"trans": [] '.encode("UTF-8"))

            f.write('}, '.encode("UTF-8"))

            f.close()

            print()
            print()

            for item in result:
                print(item[1])
                print()

            print()
            print()

        if os.path.isfile('page.jpg'):
            os.remove('page.jpg')

        print("Completed!")
        return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    torch.cuda.empty_cache()

    for imgpath in glob.glob('pages\\*.jpg'):
        process_image(imgpath)
