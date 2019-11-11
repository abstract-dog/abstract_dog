import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

'''
It cleans img from noise
'''
def clear_img(file_name):
    img = cv2.imread(file_name, 0)

    dilated_img = cv2.dilate(img, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 1)
    diff_img = 255 - cv2.absdiff(img, bg_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    thr_img[thr_img < 240] = 0
    cv2.imwrite('new.jpg', thr_img)
    return 'new.jpg'

'''
It enlarges the image
'''
def resize_img(img, scale):
    return cv2.resize(img,((int)(img.shape[1] * scale), int(img.shape[0] * scale)))


def peak_search(img, min, max):
    return cv2.Canny(img, min, max)

def search_mol_nodes(image):
    img = resize_img(cv2.imread(image), 0.3)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 30, 3, 0.04)
    ret, dst = cv2.threshold(dst, 0.1*dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5,5), (-1,-1), criteria)
    for i in range(1, len(corners)):
        cv2.circle(img, (int(corners[i,0]), int(corners[i,1])), 30, (0,255,0), 4)
    return img

def get_contours(img):
    edged = peak_search(img, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    image[::] = 255
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    return img

def find_word(img):

    matches = ['o.jpg', 'CH3.jpg', 'F.jpg', 'CL.jpg', 'OH.jpg', 'O.jpg', 'O_.jpg', '_O.jpg', 'H3C.jpg', 'N_1.PNG']
    cord_forml = {}
    img_rgb = resize_img(img, 1)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for match in matches:
        template = cv2.imread(match, 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        i = 0
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            cord_forml[match.replace('.jpg', '')] = [pt[0], pt[1]]
            i += 1
    
    cv2.imwrite('res.png',img_rgb)
    for k, v in cord_forml.items():
        print(str(k) + ':' + str(v))

    return img_rgb

if __name__ == "__main__":
########################################################################
#    if len(sys.argv) != 2:
#        print('Not enough arguments')
#        print("usage: # python find_molecule.py [name image]")
#        exit(0)
#    else:
#        print('If you want to find molecule nodes press: 1')
#        print('If you want to find word on picture press: 2')
#        chois = int(input("your choose:"))
#    
#        if chois == 1:
#            file_name = clear_img(sys.argv[1])
#            img = search_mol_nodes(file_name)
#            plt.imshow(img)
#            plt.show()
#            cv2.waitKey(0)
#        elif chois == 2:
#            file_name = clear_img(sys.argv[1])
#            img = find_word(file_name)
#            plt.imshow(img)
#            plt.show()
#            cv2.waitKey(0)
#        else:
#            print('Error: sorry, you need to choise 1 or 2')
####################################################################

    file_name = clear_img(sys.argv[1])
    img = search_mol_nodes(file_name)
    plt.imshow(img)
    plt.show()
    cv2.waitKey(0)