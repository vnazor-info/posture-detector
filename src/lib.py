from matplotlib import container
from src import config as cfg
from src import lib
import numpy as np
import cv2
import mediapipe as mp
from . import Detector
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components import containers
from mediapipe.framework.formats import landmark_pb2  
from mediapipe import solutions
import math
from time import sleep
from PIL import Image
from . import Camera
from . import Detector
from . import Landmark
from tkinter import *
import threading


def angle_3_points(a, b, c):
# b is the intersection point
  ang = math.degrees(
    math.atan2(c[1]-b[1], c[0]-b[0]) - 
    math.atan2(a[1]-b[1], a[0]-b[0])
)
  return ang + 360 if ang < 0 else ang

def percent_difference(num1, num2):
  if (num1 + num2) == 0:
    return 0 # Both are zero
  return (abs(num2 - num1) / ((num1 + num2) / 2)) * 100

def camera_test():
  #picam = Picamera2()
  #
  #config = picam.create_preview_configuration()
  #picam.configure(config)
  # 
  #picam.start_preview(Preview.QTGL)
  #
  #picam.start()
  #sleep(2)
  #camera_image = picam.capture_image().convert('RGB')
  #picam.close()
  #camera_image.save("output.jpg")
  print("camerat test")

def camera_class_test():
  cam = Camera.Camera()
  cam.preview(5)
  cam.capture_save()
  #cam.off()

  def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
      pose_landmarks = pose_landmarks_list[idx]

      # Draw the pose landmarks.
      pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
      pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
      ])
      solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image
  
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
  base_options = python.BaseOptions(model_asset_path='/home/vlatko/posture_detector/resources/selfie_segmenter_landscape.tflite')
  options = vision.ImageSegmenterOptions(base_options=base_options, output_category_mask=True)
  IMAGE_FILENAMES = ['/home/vlatko/Projects/posture-detector/resources/man_standing.jpg']

  with vision.InteractiveSegmenter.create_from_options(options) as segmenter:
  
    for image_file_name in IMAGE_FILENAMES:
      BG_COLOR = (0, 0, 0) # gray
      MASK_COLOR = (255, 255, 255) # white
      IMAGE_FILENAMES = ['/home/vlatko/Projects/posture-detector/resources/man_standing.jpg']
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


def stickfigure_videotest():
  stick_figure = Landmark.Landmark("resources/pose_landmarker_heavy.task")
  detect = Detector.Detector(cfg.MODEL_PATH)
  cam = Camera.Camera()

  while True:
    cv_image = cam.capture_image()
    np_image = np.array(cv_image)
    whole_img = mp.Image(
      image_format=mp.ImageFormat.SRGB,
      data=np_image
    )
    detect_result = detect.detect(whole_img)
    show_img=whole_img
    print("detect_result", detect_result)
    for result in detect_result:
      #crop_image = detect.crop_person(whole_img, bbox=result.bounding_box)
      show_img = stick_figure.draw_landmark(person_crop=whole_img)
      if result.categories[0].category_name != "person":
        break
    #detector = Detector(model_path="resources/pose_landmarker_heavy.task")
    #def draw_landmarks_on_image(rgb_image, detection_result):
      #pose_landmarks_list = detection_result.pose_landmarks

    # annotated_image = np.copy(rgb_image)
    #crop_image = cv2.imread(drawlandmarks.jpg)
    #cv2.imwrite("points_detection.jpg", img_landfmarks)
      cv2.imshow("landmarks", show_img)
      
      right_shoulder = stick_figure.pose_landmarks_proto.landmark[12]
      left_hip = stick_figure.pose_landmarks_proto.landmark[23]
      right_hip = stick_figure.pose_landmarks_proto.landmark[24]
      left_knee = stick_figure.pose_landmarks_proto.landmark[25]
      right_knee = stick_figure.pose_landmarks_proto.landmark[26]
      right_elbow = stick_figure.pose_landmarks_proto.landmark[14]
      left_elbow = stick_figure.pose_landmarks_proto.landmark[13]
      left_shoulder = stick_figure.pose_landmarks_proto.landmark[11]
      dictionary = {
        "left_shoulder": (left_shoulder.x, left_shoulder.y),
        "right_shoulder": (right_shoulder.x, right_shoulder.y),  
        "left_hip": (left_hip.x, left_hip.y),
        "right_hip": (right_hip.x, right_hip.y),
        "left_knee": (left_knee.x, left_knee.y),
        "right_knee": (right_knee.x, right_knee.y),
        "left_elbow": (left_elbow.x, left_elbow.y),
        "right_elbow": (right_elbow.x, right_elbow.y),
      }

      left_arm = {
        "left_shoulder" : (left_shoulder.x, left_shoulder.y),
        "left_elbow": (left_elbow.x, left_elbow.y),
      }
      right_arm = {
        "right_shoulder": (right_shoulder.x, right_shoulder.y),
        "right_elbow": (right_elbow.x, right_elbow.y),
      }
      left_leg = {
        "left_hip": (left_hip.x, left_hip.y),
        "left_knee": (left_knee.x, left_knee.y),
      }
      right_leg = {
        "right_hip": (right_hip.x, right_hip.y),
        "right_knee": (right_knee.x, right_knee.y),
      }
      dict_parts = {
        "left_arm" : left_arm,
        "right_arm" : right_arm,
        "left_leg" : left_leg,
        "right_leg" : right_leg
      }
  
    if cv2.waitKey(1) == ord('p'):
      print("left_shoulder"), print (dictionary["left_shoulder"])
      print("right_shoulder"), print(dictionary["right_shoulder"])
      print("left_hip"), print(dictionary["left_hip"])
      print("right_hip"), print(dictionary["right_hip"])
      print("left_knee"), print(dictionary["left_knee"])
      print("right_knee"), print(dictionary["right_knee"])
      print("left_elbow"), print(dictionary["left_elbow"])
      print("right_elbow"), print(dictionary_parts["left_hand"])



  # Example: Comparing 20 and 30
  

  # Example: 90 degree corner                                 
      p1 = (dict_parts["left_arm"]["left_elbow"])             
      p_center = (dict_parts["left_arm"]["left_shoulder"])
      p2 = (dict_parts["right_arm"]["right_shoulder"])
      final_angel = angle_3_points(p2, p_center, p1)
        

      if cv2.waitKey(1) == ord('q'):
        p1 = (dict_parts["left_arm"]["left_elbow"])
        p_center = (dict_parts["left_arm"]["left_shoulder"])
        p2 = (dict_parts["right_arm"]["right_elbow"])
        cv2.imwrite("final_landmarks.jpg", show_img)
        cv2.destroyAllWindows()
        break
      if cv2.waitKey(1) == ord('a'):
        print(f"Angle: {angle_3_points(p2, p_center, p1):.2f} degrees") 
        print(f"Percent Difference: {percent_difference(90, final_angel):.2f}%")

var = 1
  
def tktinker_test():
  print("tkinter test")
  root = Tk()

  # Widgets are added here
  label = Label(root, text="Posture Detector")
  label.pack(pady=10)

  button = Button(root, text="Start", width=25, command=thread)
  button1 = Button(root, text="Stop", width=25, command=close_window)
  button1.pack()
  button.pack()
  root.mainloop()

def thread():
  t = threading.Thread(target=start_window)
  t.start()

def start_window():
  print("start window")
  global var
  var = 1
  playground()

def close_window():
  print("close window")
  global var
  var = 0
    

def playground():
  #code for testing new stuff
  global var
  lap_cam = Camera.Camera()
  detect = Landmark.Detective()
  print (var)
  while True:
    
    lap_cam.open_window()
    print("in the loop")
    still_image = lap_cam.capture_image()
    whole_img = mp.Image(
      image_format=mp.ImageFormat.SRGB,
      data=still_image
    )
  
    if detect.person_detected(whole_img):
      landmark_img = detect.draw_landmarks(whole_img)
    
    lap_cam.present_img(landmark_img)
    if var == 0:
      print("breaking loop")
      cv2.destroyAllWindows()
      break

