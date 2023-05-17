import os
from PIL import Image
from typing import List
from config import ImagePixel, ImageStorage
from utils import merge

def select_image(image_list: List[str], index: int) -> str:
    if index < 0 :
        return image_list[0]
    elif index >= 0 and index < len(image_list):
        return image_list[index]
    # index >= len(image_list)
    return image_list[index % len(image_list)]


def draw_pic(
    img_dir: str,
    img_map_list: List[List[List[int]]],#img_mag_list内部元素等宽
    height: int = ImagePixel.height,
    width: int = ImagePixel.width
):
    imgs = os.listdir(img_dir)
    total_row = 0
    column = len(img_map_list[0][0])
    for ele in img_map_list:
        total_row += len(ele)
        assert column == len(ele[0])

    # 使用Image.new()方法创建一个画布
    figure = Image.new("RGB", (width*column, height*total_row),"white")

    count = 0
    start_index = 0
    for img_map in img_map_list:
        for i in range(len(img_map)):
            for j in range(column):
                if img_map[i][j] == 1:
                    continue
                # 如果元素是0, 在对应位置填充一张image
                else:
                    try:
                        image = Image.open(os.path.join(img_dir, select_image(imgs, count)))
                        # resize
                        image = image.resize((width, height))
                        figure.paste(image, (width*j, height*(i + start_index)))
                        count += 1
                    except:
                        print("Error: image path is %s" % os.path.join(img_dir, select_image(imgs, count)))

        start_index += len(img_map)

    figure.show()
    figure.save(ImageStorage.gen_save_path)


if __name__=="__main__":
    from config import ImageMap
    draw_pic(
        r"./pic/gen",
        img_map_list=[
            ImageMap._520,
            ImageMap.heart,
            ImageMap._17
        ]
    )

    merge(
        origin_image=ImageStorage.gen_save_path,
        add_image=r"./pic/fill/2.png",
        added_image=ImageStorage.final_save_path,
        scale=1.2
    )
