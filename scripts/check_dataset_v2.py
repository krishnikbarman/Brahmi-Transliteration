from pathlib import Path


DATASET = Path("dataset_v2")

TARGET = 15

total_classes = 0
total_images = 0

smallest_class = ""
smallest_count = 999

largest_class = ""
largest_count = 0

below_target = []


for folder in sorted(DATASET.iterdir()):

    if not folder.is_dir():
        continue

    total_classes += 1

    images = (
        list(folder.glob("*.png"))
        + list(folder.glob("*.jpg"))
        + list(folder.glob("*.jpeg"))
    )

    count = len(images)

    total_images += count


    if count < smallest_count:
        smallest_count = count
        smallest_class = folder.name


    if count > largest_count:
        largest_count = count
        largest_class = folder.name


    if count < TARGET:
        below_target.append(
            (folder.name, count)
        )


print("====================")
print("Dataset V2 Report")
print("====================")

print("Total Classes :", total_classes)
print("Total Images  :", total_images)

if total_classes:
    print(
        "Average Images/Class:",
        round(total_images / total_classes, 2)
    )

print()

print(
    "Smallest Class:",
    smallest_class,
    smallest_count
)

print(
    "Largest Class:",
    largest_class,
    largest_count
)

print()

print(
    "Classes below target (15):",
    len(below_target)
)

for name, count in below_target:
    print(name, "->", count)