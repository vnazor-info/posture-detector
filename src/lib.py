from matplotlib import container
from src import config as cfg
import numpy as np
import cv2
import mediapipe as mp
from Detector import Detector
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components import containers
import math

def visualize(image,detection_result) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = (bbox.origin_x, bbox.origin_y)
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, cfg.TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (cfg.MARGIN + bbox.origin_x,
                     cfg.MARGIN + cfg.ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                cfg.FONT_SIZE, cfg.TEXT_COLOR, cfg.FONT_THICKNESS)

  return image

def crop_image(img, origin_y, origin_x, height, width):
  crop_img = img[origin_y:origin_y+height+10, origin_x-10:origin_x+width]
  cv2.imwrite("cropped.jpg", crop_img)
  return(crop_img)


def detector_showcase():
  detector = Detector(model_path=cfg.MODEL_PATH)
   
  # STEP 4: Detect objects in the input image.
  cv_image = cv2.imread(cfg.mp_image_path)
  #open image then detect
  #koristiti cv2 za open image
  mp_image = mp.Image.create_from_file(cfg.mp_image_path)
  detection_results = detector.detect(mp_image) 
   

  # STEP 5: Process the detection result. In this case, visualize it.
  print(detection_results)

  np_crop = detector.extract(mp_image.numpy_view(), detection_results[0].bounding_box)
  cv2.imwrite("cropped_detection.jpg", np.copy(np_crop))
#image_copy = np.copy(mp_image.numpy_view())
#annotated_image = visualize(image_copy, detection_result)
#rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
#cv2.imwrite("detection_result.jpg", rgb_annotated_image)
#colour_img= cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
#for detection in detections:
  #for category in detection.categories:
    #if category.category_name == "person":
      #print("nasao sam osobu")
    #else:
      #print("nema ljudi")


#if __name__ == "__main__":
  #print("Do some tests")

DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480

RegionOfInterest = vision.InteractiveSegmenterRegionOfInterest
NormalizedKeypoint = containers.keypoint.NormalizedKeypoint

def resize_and_show(image):
  h, w = image.shape[:2]
  if h < w:
    img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
  else:
    img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
  cv2.imwrite("area.jpg",img)

def person_detect():
  # Create the options that will be used for ImageSegmenter
  base_options = python.BaseOptions(model_asset_path='/home/bil/posture_detector/resources/selfie_segmenter_landscape.tflite')
  options = vision.ImageSegmenterOptions(base_options=base_options, output_category_mask=True)
  IMAGE_FILENAMES = ['/home/bil/posture_detector/resources/man-standing-861098.jpg']

  with vision.InteractiveSegmenter.create_from_options(options) as segmenter:
  
    for image_file_name in IMAGE_FILENAMES:
      BG_COLOR = (0, 0, 0) # gray
      MASK_COLOR = (255, 255, 255) # white
      IMAGE_FILENAMES = ['/home/bil/posture_detector/resources/man-standing-861098.jpg']
      images = {name: cv2.imread(name) for name in IMAGE_FILENAMES}

      image = mp.Image.create_from_file(image_file_name)

        # Retrieve the masks for the segmented image

      roi = RegionOfInterest(format=RegionOfInterest.Format.KEYPOINT,
                           keypoint=NormalizedKeypoint(DESIRED_HEIGHT/2, DESIRED_WIDTH/2))
      segmentation_result = segmenter.segment(image,roi)
      category_mask = segmentation_result.category_mask

      # Generate solid color images for showing the output segmentation mask.
      image_data = image.numpy_view()
      fg_image = np.zeros(image_data.shape, dtype=np.uint8)
      fg_image[:] = MASK_COLOR
      bg_image = np.zeros(image_data.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR

      condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
      output_image = np.where(condition, fg_image, bg_image)

      print(f'Segmentation mask of {image}:')
      resize_and_show(output_image)
      