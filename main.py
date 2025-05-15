from ultralytics import YOLO
import cv2

import util
from sort.sort import *
from util import get_car, read_number_plate, write_csv

results = {}

obj_tracker = Sort()

#loading models
model = YOLO('yolov8n.pt')
number_plate_detector = YOLO('./models/LP-detection.pt')

#loading video
cap = cv2.VideoCapture('./12361704_1920_1080_30fps.mp4')

vehicles = [2, 3, 5, 7]
#reading frames
frame_num = -1
ret = True
while ret:
    frame_num += 1
    ret, frame = cap.read()
    if ret:
        if frame_num > 10:
            break 
        results[frame_num] = {}
        #detecting vehicles
        detections = model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])


        #tracking vehicles
        track_ids = obj_tracker.update(np.asarray(detections_))

        #detecting number plates
        number_plates = number_plate_detector(frame)[0]
        for number_plate in number_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = number_plate

            #assign car to number plate bcoz we have numberplates and cars now we should know which numplate is for which car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(number_plate, track_ids)

            if car_id != -1:
                
                #cropping the number plate
                number_plate_crop = frame[int(y1):int(y2),int(x1):int(x2), :]

                #processing image of number plate
                number_plate_crop_gray = cv2.cvtColor(number_plate_crop, cv2.COLOR_BGR2GRAY)
                _, number_plate_crop_thresh = cv2.threshold(number_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV) #for taking pixels lower than 64 to 255 and higher to 0


                #read number plate
                number_plate_text, number_plate_text_score = util.read_number_plate(number_plate_crop_thresh)

                if number_plate_text is not None:
                    results[frame_num][car_id] = {'car':{'bbox': [ xcar1, ycar1, xcar2, ycar2]}, 
                                                'number_plate':{'bbox':[x1, y1, x2, y2],
                                                                'text': number_plate_text, 
                                                                'bbox_score': score, 
                                                                'text_score': number_plate_text_score}}

#writing results
write_csv(results,'./test.csv')