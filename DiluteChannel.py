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
        self.K = 0.0
        self.L = 0.0
        self.offsetS = 1
        self.offsetE = 1
        self.offsetB = 1
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
            self.offsetS = 0
        if method == 'JarvisJudiceNinkeDithering':
            mat = [
                    [0,0,0,7,5],
                    [3,5,7,5,3],
                    [1,3,5,3,1]
            ]
            self.offsetS = 2
            self.offsetE = 2
            self.offsetB = 2
        if method == 'StuckiDithering':
            mat = [
                    [0,0,0,8,4],
                    [2,4,8,4,2],
                    [1,2,4,2,1]
            ]
                
            self.offsetS = 2
            self.offsetE = 2
            self.offsetB = 2
        if method == 'AtkinsonDithering':
            mat = [
                    [0,0,0,1,1],
                    [0,1,1,1,0],
                    [0,0,1,0,0]
            ]
            self.offsetE = 2
            self.offsetB = 2
        if method == 'BurkesDithering':
            
            mat = [
                    [0,0,0,8,4],
                    [2,4,8,4,2],
                    [0,0,0,0,0]
            ]
            self.offsetS = 2
            self.offsetE = 2
        if method == 'SierraDithering':
            mat = [
                    [0,0,0,5,3],
                    [2,4,5,4,2],
                    [0,2,3,2,0]
            ]
            self.offsetS = 2
            self.offsetE = 2
            self.offsetB = 2
        if method == 'TwoRowSierra':
            mat = [
                    [0,0,0,4,3],
                    [1,2,3,2,1],
                    [0,0,0,0,0]
            ]
            self.offsetS = 2
            self.offsetE = 2
        if method == 'SierraLite':
            mat = [
                    [0,0,0,2,0],
                    [0,1,1,0,0],
                    [0,0,0,0,0]
            ]
        DEN = np.sum(np.sum(mat))
        [
            [self.p,self.q,self.r,self.A,self.B],
            [self.C,self.D,self.E,self.F,self.G],
            [self.H,self.I,self.J,self.K,self.L],
        ] = mat/DEN
        print(DEN)
        print(self.A)
        print(self.B)
            
    def dilute(self , img,factor=1,reshape=True):
        
        if len(img.shape)!=2:
            print(img.shape)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if reshape:
            pixelWIDTH = 384
            img = cv2.resize(img, (0,0), fx=pixelWIDTH/(img.shape[1]), fy=pixelWIDTH/(img.shape[1])) 
        img = np.array(img,dtype='int')
        h,w = img.shape
        
        for y in range(h-self.offsetB):
            for x in range(self.offsetS , w-self.offsetE):
                old = img[y][x]
                img[y][x] = round(factor * (img[y][x] / 255.0)) * (255/factor)
                
                quant_error = old - img[y][x]
                
                if self.A !=0.0:
                    img[y    ][x + 1] +=( quant_error * self.A)
                
                if self.B !=0.0:
                    img[y    ][x + 2] +=( quant_error * self.B)
                
                
                if self.C !=0.0:
                    img[y + 1][x - 2] +=( quant_error * self.C)
                
                if self.D !=0.0:
                    img[y + 1][x - 1] +=( quant_error * self.D)
                
                if self.E !=0.0:
                    img[y + 1][x    ] +=( quant_error * self.E)
                
                if self.F !=0.0:
                    img[y + 1][x + 1] +=( quant_error * self.F)
                
                if self.G !=0.0:
                    img[y + 1][x + 2] +=( quant_error * self.G)
                
                
                if self.H !=0.0:
                    img[y + 2][x - 2] +=( quant_error * self.H)
                
                if self.I !=0.0:
                    img[y + 2][x - 1] +=( quant_error * self.I)
                
                if self.J !=0.0:
                    img[y + 2][x    ] +=( quant_error * self.J)
                
                if self.K !=0.0:
                    img[y + 2][x + 1] +=( quant_error * self.K)
                
                if self.L !=0.0:
                    img[y + 2][x + 2] +=( quant_error * self.L)
        img = np.array(img,dtype='uint8')
        ret,img = cv2.threshold(img  ,110,1,cv2.THRESH_BINARY)
        return img
        
if __name__ == '__main__':
    img = cv2.imread('test.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    converter = DiluteChannel(DiluteChannel.d[3])

    con = converter.dilute(img,1)
    plt.imshow(con,cmap='gray')
    plt.show()
