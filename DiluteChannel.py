import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys


# http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/

class DiluteChannel():

    d={
        0:'FloydSteinbergDithering',
        1:'FloydSteinberg',
        2:'JarvisJudiceNinkeDithering',
        3:'StuckiDithering',
        4:'AtkinsonDithering',
        5:'BurkesDithering',
        6:'SierraDithering',
        7:'TwoRowSierra',
        8:'SierraLite'
    }

    def __init__(self,method = 'FloydSteinbergDithering'):
        if method == 'FloydSteinbergDithering':
            mat = [
                    [0,0,0,7,0],
                    [0,3,5,1,0],
                    [0,0,0,0,0]
            ]
        if method == 'FloydSteinberg':
            mat = [
                    [0,0,0,3,0],
                    [0,0,3,2,0],
                    [0,0,0,0,0]
            ]
        if method == 'JarvisJudiceNinkeDithering':
            mat = [
                    [0,0,0,7,5],
                    [3,5,7,5,3],
                    [1,3,5,3,1]
            ]
        if method == 'StuckiDithering':
            mat = [
                    [0,0,0,8,4],
                    [2,4,8,4,2],
                    [1,2,4,2,1]
            ]
        if method == 'AtkinsonDithering':
            mat = [
                    [0,0,0,1,1],
                    [0,1,1,1,0],
                    [0,0,1,0,0]
            ]
        if method == 'BurkesDithering':
            mat = [
                    [0,0,0,8,4],
                    [2,4,8,4,2],
                    [0,0,0,0,0]
            ]
        if method == 'SierraDithering':
            mat = [
                    [0,0,0,5,3],
                    [2,4,5,4,2],
                    [0,2,3,2,0]
            ]
        if method == 'TwoRowSierra':
            mat = [
                    [0,0,0,4,3],
                    [1,2,3,2,1],
                    [0,0,0,0,0]
            ]
        if method == 'SierraLite':
            mat = [
                    [0,0,0,2,0],
                    [0,1,1,0,0],
                    [0,0,0,0,0]
            ]
        DEN = np.sum(np.sum(mat))
        self.FILTER = np.mat(mat)/DEN

    def dilute(self , img,factor=1,reshape=True,flage=True):

        # Check if the image is with 2 channels or 3 channels
        if len(img.shape)!=2:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # You can remove this if you want to work with full image[But takes more time]
        if reshape:
            pixelWIDTH = 384
            img = cv2.resize(img, (0,0), fx=pixelWIDTH/(img.shape[1]), fy=pixelWIDTH/(img.shape[1]))

        img = np.array(img,dtype='float64')
        h,w = img.shape
        dummy = np.zeros((h+2, w+4), dtype='float64')
        dummy[:-2, 2:-2] = img
        img = dummy

        for y in range( h ):
            for x in range( 2,w+2 ):
                old = img[y][x]
                img[y][x] = round(factor * (img[y][x] / 255.0)) * (255/factor)

                quant_error = old - img[y][x]
                img[y:y+3, x-2:x+3] += (quant_error*self.FILTER)

        img = np.array(img[:-2, 2:-2],dtype='uint8')
        # use this line if FACTOR==1, It makes image to 0 or 1
        if factor==1 and flage:
            ret,img = cv2.threshold(img  ,110,1,cv2.THRESH_BINARY)
        return img

    def dilute_on_3channel(self , img,factor=1,reshape=True):
        # Check if the image is with 2 channels or 3 channels
        if len(img.shape)!=3:
            return self.dilute(img, factor, reshape)

        if reshape:
            pixelWIDTH = 384
            img = cv2.resize(img, (0,0), fx=pixelWIDTH/(img.shape[1]), fy=pixelWIDTH/(img.shape[1]))

        for channel in range(3):
            img[:,:,channel] = self.dilute(img[:,:,channel],factor,False,False)
        return img


if __name__ == '__main__':
    img = cv2.imread('test.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    converter = DiluteChannel(DiluteChannel.d[3])


    # The second argument 'factor' is for number of Levels in outPut image
    # for example factor = 1 implies ---- 2 levels in outPut image (for single channel image)
    #             factor = 2 implies ---- 3 levels in outPut image (for single channel image)
    # for example factor = 1 implies ---- 3^2 = 8  levels in outPut image (for 3 channel image)
    #             factor = 2 implies ---- 3^3 = 27  levels in outPut image (for 3 channel image)

    con = converter.dilute(img,255)
    plt.imshow(con,cmap='gray')
    plt.show()
    con_3 = converter.dilute_on_3channel(img,1)
    plt.imshow(con_3,cmap='gray')
    plt.show()
