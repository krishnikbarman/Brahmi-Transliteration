from pathlib import Path
import shutil


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE = PROJECT_ROOT / "dataset"
DEST = PROJECT_ROOT / "dataset_v2"


DEST.mkdir(exist_ok=True)


for class_folder in SOURCE.iterdir():

    if class_folder.is_dir():

        target = DEST / class_folder.name
        target.mkdir(exist_ok=True)

        for image in class_folder.glob("*"):

            shutil.copy(
                image,
                target / image.name
            )


print("Dataset V2 created")