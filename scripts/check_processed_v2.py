from pathlib import Path


DATASET = Path("processed_dataset_v2")


classes = [
    folder for folder in DATASET.iterdir()
    if folder.is_dir()
]


images = sum(
    len(list(folder.glob("*.png")))
    for folder in classes
)


print("====================")
print("Processed Dataset V2")
print("====================")

print("Classes:", len(classes))
print("Images :", images)
print("Average:", round(images / len(classes), 2))