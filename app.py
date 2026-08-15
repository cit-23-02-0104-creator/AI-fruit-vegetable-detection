from roboflow import Roboflow
import cv2

API_KEY = "aNQojwGzi6K6FI8x9Mpl"

image_path = input("Image Path: ")

rf = Roboflow(api_key=API_KEY)

project = rf.workspace().project("fruits-and-vegetables-2vf7u")
model = project.version(1).model

prediction = model.predict(
    image_path,
    confidence=40,
    overlap=30
).json()

image = cv2.imread(image_path)

for pred in prediction["predictions"]:

    x = int(pred["x"])
    y = int(pred["y"])
    w = int(pred["width"])
    h = int(pred["height"])

    class_name = pred["class"]
    confidence = pred["confidence"]

    x1 = int(x - w / 2)
    y1 = int(y - h / 2)
    x2 = int(x + w / 2)
    y2 = int(y + h / 2)

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    label = f"{class_name} {confidence:.2f}"

    cv2.putText(
        image,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

cv2.imshow("Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("output.jpg", image)

print("Saved: output.jpg")