import streamlit as st
import tensorflow as tf
import numpy as np
import json

from PIL import Image


# =====================
# Configuration
# =====================

MODEL_PATH = "model/brahmi_mobilenetv2_final.keras"
MAPPING_PATH = "mapping/brahmi_class_mapping.json"

IMAGE_SIZE = (224, 224)


# =====================
# Load Model
# =====================

@st.cache_resource
def load_model():

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    return model


model = load_model()



# =====================
# Load Mapping
# =====================

with open(
    MAPPING_PATH,
    "r",
    encoding="utf-8"
) as f:

    class_mapping = json.load(f)



# =====================
# Preprocessing
# =====================

def preprocess_image(image):

    img = image.convert("L")

    img_array = np.array(img)


    # Threshold
    img_array = np.where(
        img_array < 200,
        0,
        255
    )


    # Crop character

    coords = np.argwhere(
        img_array < 255
    )


    if coords.size > 0:

        y0, x0 = coords.min(axis=0)

        y1, x1 = coords.max(axis=0)


        img_array = img_array[
            y0:y1+1,
            x0:x1+1
        ]


    img = Image.fromarray(
        img_array.astype("uint8")
    )


    # Resize maintaining ratio

    img.thumbnail(
        IMAGE_SIZE
    )


    # White canvas

    canvas = Image.new(
        "L",
        IMAGE_SIZE,
        255
    )


    x = (IMAGE_SIZE[0] - img.size[0]) // 2

    y = (IMAGE_SIZE[1] - img.size[1]) // 2


    canvas.paste(
        img,
        (x,y)
    )


    return canvas



# =====================
# Prediction
# =====================

def predict(image):


    img = preprocess_image(
        image
    )


    img_array = np.array(
        img
    ).astype(
        "float32"
    )


    img_array = np.expand_dims(
        img_array,
        axis=-1
    )


    img_array = np.expand_dims(
        img_array,
        axis=0
    )


    prediction = model.predict(
        img_array,
        verbose=0
    )[0]


    class_id = np.argmax(
        prediction
    )


    confidence = prediction[class_id]


    character = class_mapping[
        str(class_id)
    ]


    # =====================
    # Top 5 Debug
    # =====================

    print("\nTop 5 Predictions")
    print("=================")


    top5 = np.argsort(
        prediction
    )[-5:][::-1]


    for idx in top5:

        print(
            class_mapping[str(idx)],
            ":",
            round(
                float(prediction[idx])*100,
                2
            ),
            "%"
        )


    return character, confidence, img



# =====================
# Streamlit UI
# =====================

st.title(
    "Brahmi Script Recognition & Transliteration"
)


st.write(
    "Upload a Brahmi character image"
)



uploaded_file = st.file_uploader(
    "Choose Image",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)



if uploaded_file:


    image = Image.open(
        uploaded_file
    )


    st.image(
        image,
        caption="Original Image",
        width=250
    )


    if st.button("Predict"):


        character, confidence, processed = predict(
            image
        )


        st.image(
            processed,
            caption="Processed Image",
            width=250
        )


        st.success(
            f"Detected Character: {character}"
        )


        st.info(
            f"Confidence: {confidence*100:.2f}%"
        )