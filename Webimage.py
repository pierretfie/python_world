from PIL import Image
import os


def reduce_img(input_path, output_path, quality=80, target_height = None):

    with Image.open(input_path) as img:
        if target_height:
            aspect_ratio = img.width / img.height
            target_width = int(target_height*aspect_ratio)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)


            img.save(output_path, optimize = True, quality = quality)

    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
    return compressed_size
input_path = os.path.expanduser('~/Desktop/coding space/ic_design_center/case-studies/files')
output_path = os.path.expanduser('~/Desktop/coding space/ic_design_center/case-studies/files/resized')
if not os.path.exists(output_path):
    os.makedirs(output_path)

else:
    pass
target_height = 1024

for img in os.listdir(input_path):
    input_image_path = os.path.join(input_path, img)
    output_image_path = os.path.join(output_path, img)

    if img.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):

        if img in os.listdir(output_path):
            print(f"{img} already compressed")
        else:

            compressed_size = reduce_img(input_image_path, output_image_path, quality=80, target_height=target_height)
            print(f'output image size:{output_image_path.strip(output_path)}:{compressed_size:.2f} Mbs')




