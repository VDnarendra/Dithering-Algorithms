# Dithering-Algorithms
Pre-processing of Gray scale images to make them binary images but with Shades that don't appear when we just use Simple Thresholding


# http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
# Usage:
    img = cv2.imread('test.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    converter = DiluteChannel(DiluteChannel.d[3])

    con = converter.dilute(img,1)
    plt.imshow(con,cmap='gray')
    plt.show()


# Implimented Algorithms:

    0:'FloydSteinbergDithering',
    1:'FloydSteinberg',
    2:'JarvisJudiceNinkeDithering',
    3:'StuckiDithering',
    4:'AtkinsonDithering',
    5:'BurkesDithering',
    6:'SierraDithering',
    7:'TwoRowSierra',
    8:'SierraLite'
