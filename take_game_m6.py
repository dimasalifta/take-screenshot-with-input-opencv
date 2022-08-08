import cv2
import argparse
import os.path
from os import path, makedirs

parser = argparse.ArgumentParser(description='Command line description')
parser.add_argument('--folder_name', type=str,help='A required folder name argument')
parser.add_argument('--camera', type=int,help='A required camera id argument')
args = parser.parse_args()
name = args.folder_name

cam = cv2.VideoCapture(args.camera)
cam.set(3, 640)
cam.set(4, 360)
# cv2.namedWindow("press space to take a photo | esc to save", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("press space to take a photo | esc to save", 500, 300)
def zoom_center(img, zoom_factor):

    y_size = img.shape[0]
    x_size = img.shape[1]
    
    # define new boundaries
    x1 = int(0.5*x_size*(1-1/zoom_factor))
    x2 = int(x_size-0.5*x_size*(1-1/zoom_factor))
    y1 = int(0.5*y_size*(1-1/zoom_factor))
    y2 = int(y_size-0.5*y_size*(1-1/zoom_factor))

    # first crop image then scale
    img_cropped = img[y1:y2,x1:x2]
    return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)
img_counter = 0

while True:
    ret, frame = cam.read()
    #create ROI
 
    center_coordinates = (320, 130)   # Center coordinates 640x480
    radius = 100            # Radius of circle
    colorb = (255, 0, 0)     # Blue color in BGR
    colorr = (0, 0, 255)     # Blue color in BGR
    colorg = (0, 255, 0)
    thickness = 1           # Line thickness of 2 px
    xx1 = 140
    yy1 = 0
    xx2 = 500
    yy2 = 360
    
    zoom = zoom_center(frame, 1)    # the value is zoom value
    roi = frame[yy1:yy2,xx1:xx2]
    
    if not ret:
        print("Kamera tidak terhubung, periksa kembali!")
        break
#     cv2.rectangle(frame, pt1=(xx1,yy1), pt2=(xx2,yy2), color=(0,255,0), thickness=3) #xy
    cv2.imshow("Tekan Spasi untuk mengambil gambar | ESC untuk menyimpan dan keluar", frame)
    cv2.imshow("roi", roi)
#     cv2.imshow("zoom", zoom)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("menekan ESC, menutup program...")
        break
    elif k%256 == 32:
        # SPACE pressed
        directory = "dataset/"+ name
        if(not path.exists(directory)):
        	makedirs(directory)
        img_name = directory+"/gambar_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
#         cv2.imwrite(img_name, roi)
#         cv2.imwrite(img_name, zoom) 
        
        print("{} tersimpan!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
