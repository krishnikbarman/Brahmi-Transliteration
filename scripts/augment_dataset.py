from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import random
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET = PROJECT_ROOT / "dataset_v2"

TARGET_IMAGES = 15


def add_noise(image):
    array = np.array(image)

    noise = np.random.normal(
        0,
        5,
        array.shape
    )

    noisy = array + noise

    noisy = np.clip(
        noisy,
        0,
        255
    ).astype(np.uint8)

    return Image.fromarray(noisy)


def augment_image(image):

    choice = random.choice([
        "rotate",
        "contrast",
        "brightness",
        "blur",
        "noise"
    ])

    if choice == "rotate":
        angle = random.randint(-5, 5)
        return image.rotate(angle)

    elif choice == "contrast":
        factor = random.uniform(0.8, 1.2)
        return ImageEnhance.Contrast(image).enhance(factor)

    elif choice == "brightness":
        factor = random.uniform(0.8, 1.2)
        return ImageEnhance.Brightness(image).enhance(factor)

    elif choice == "blur":
        return image.filter(
            ImageFilter.GaussianBlur(radius=0.5)
        )

    elif choice == "noise":
        return add_noise(image)


total_before = 0
total_after = 0


for class_folder in DATASET.iterdir():

    if not class_folder.is_dir():
        continue


    images = list(class_folder.glob("*.png")) + list(class_folder.glob("*.jpg"))

    original_images = images.copy()

    count = len(images)

    total_before += count


    if count >= TARGET_IMAGES:
        total_after += count
        continue


    index = 0

    while count < TARGET_IMAGES:

        source = random.choice(original_images)


        with Image.open(source) as img:

            img = img.convert("L")

            augmented = augment_image(img)


            output = class_folder / f"aug_{index}.png"

            # avoid overwrite
            while output.exists():
                index += 1
                output = class_folder / f"aug_{index}.png"


            augmented.save(output)


        count += 1
        index += 1


    total_after += count

    print(
        f"{class_folder.name}: {len(original_images)} → {count}"
    )


print("\n====================")
print("Augmentation Complete")
print("====================")

print("Before:", total_before)
print("After :", total_after)