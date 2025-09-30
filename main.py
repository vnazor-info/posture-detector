##classes
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from src import lib

##model
if __name__ == "__main__":
  

  # STEP 4: Detect objects in the input image.
  detection_result = detector.detect(mp_image)

  # STEP 5: Process the detection result. In this case, visualize it.
  print(detection_result)

  bbox = detection_result.detections[0].bounding_box

#image_copy = np.copy(mp_image.numpy_view())
#annotated_image = visualize(image_copy, detection_result)
#rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
#cv2.imwrite("detection_result.jpg", rgb_annotated_image)
#colour_img= cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
for detection in detections:
  for category in detection.categories:
    if category.category_name == "person":
      print("nasao sam osobu")
    else:
      print("nema ljudi")