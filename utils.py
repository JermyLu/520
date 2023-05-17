import os
from typing import List
import cv2

def rename_files(dir_path: str):
    for i, fn in enumerate(os.listdir(dir_path)):
        old_fp = os.path.join(dir_path, fn)
        new_fp = os.path.join(dir_path, str(i+1) + "." + fn.split(".")[-1])
        os.rename(old_fp, new_fp)
    
    print("*" * 10, "Done!")


# 0 -> 1
# 1 -> 0
def convert_image_map(image_map: List[List[str]]):
    for i in range(len(image_map)):
        for j in range(len(image_map[0])):
            if image_map[i][j] == 0:
                image_map[i][j] = 1
            elif image_map[i][j] == 1:
                image_map[i][j] = 0
            
    for ele in image_map:
        print(ele, ",")


def scale_image(
    image_path: str,
    scale: float = 1.0
):
    if scale < 0.0:
        scale = 0.0
    
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    print("Original image size: height=%s, width=%s" % (height, width))
    image = cv2.resize(image, (int(width * scale), int(height * scale)))
    height, width, _ = image.shape
    cv2.imwrite(image_path, image)
    print("Resized image size: height=%s, width=%s" % (height, width))


def merge(
    origin_image: str,
    add_image: str,
    added_image: str,
    scale: float = 1.0
):
    if scale != 1.0:#进行scale
        scale_image(add_image, scale=scale)

    origin = cv2.imread(origin_image)
    added = cv2.imread(add_image)
    origin_height, origin_width = origin.shape[:2]
    added_height, added_width = added.shape[:2]

    # 确定区域
    top_left_h = origin_height - added_height
    top_left_w = origin_width - added_width
    roi = origin[top_left_h:origin_height, top_left_w:origin_width]

    # 创建掩膜
    img2gray = cv2.cvtColor(added, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    dst = cv2.add(img1_bg, added) # 进行融合
    origin[top_left_h:origin_height, top_left_w:origin_width] = dst #原图融合

    cv2.imwrite(added_image, origin)
    print("图像融合完成✅")


if __name__=="__main__":
    # image_path = r"./pic/fill/2.png"
    # scale_image(image_path, scale=2.0)
    origin_image = r"final_result.png"
    add_image = r"./pic/fill/2.png"
    merge(
        origin_image=origin_image,
        add_image=add_image,
        added_image=origin_image,
        scale=0.5
    )