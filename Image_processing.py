from collections import defaultdict

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

''' Display Image '''


def display_image(title, image):
    cv.imshow(title, image)
    cv.waitKey(0)


''' Bit Conversion Question 1 '''


def bit_conversion(image):
    m, n = image.shape
    chg_pxl = int(input("Enter change bit(less than 8): "))
    value = pow(2, 8-chg_pxl)
    for i in range(m):
        for j in range(n):
            image[i, j] /= value
    display_image(f'{chg_pxl} bit Converted Image', image)


''' Question 2 '''



def add_extra(image):                   # Adding an extra image with extended columns and rows
    row, column = image.shape
    print("Image is this")
    midr = row/2
    midc = column/2
    for i in range(row):
        for j in range(column):
            pixel = image[i][j]
            pixel = (pixel* image[midr][midc])%256
            image[i][j] = pixel
     
            
            
    print("\n")
    new_image = []
    temp = []
    for i in range(row):
        for j in range(column-1):
            temp.append(image[i][j])
            temp.append(image[i][j])
        new_image.append(temp)
        temp = []
    new_image = np.array(new_image, dtype=np.uint8)
    return new_image


def zooming(image):                   # Zooming function
    new_image = add_extra(image)
    new_image = np.transpose(new_image)
    new_image2 = add_extra(new_image)
    new_image = np.transpose(new_image2)
    display_image('Zoomed Image', new_image)


def remove_extra(image):                   # Adding the extra image with reduced columns and rows
    row, column = image.shape
    new_image = []
    temp = []
    for i in range(row-1):
        for j in range(0, column-1, 2):
            temp.append(image[i][j])
        new_image.append(temp)
        temp = []

    new_image = np.array(new_image, dtype=np.uint8)
    return new_image


def shrink(image):                   # Shrinking Function
    new_image = remove_extra(image)
    new_image = np.transpose(new_image)
    new_image2 = remove_extra(new_image)
    new_image = np.transpose(new_image2)
    display_image('Shrinked Image', new_image)


''' Question 3 '''


def gamma_correction(image):                   # Gamma Function
    gamma = []
    n = int(input("Enter no of trails: "))
    while n != 0:
        ga = float(input("Enter gamma value"))
        gamma.append(ga)
        n -= 1
    for g in gamma:
        c = np.array(255*(image/255)**g, dtype=None)
        display_image(f'Gamma transform for {g}', c)


''' Question 4'''


def get_dict(image):                   # Plotting the Histogram for the image
    m, n = image.shape
    pxl = defaultdict(int)
    for i in range(m):
        for j in range(n):
            pxl[image[i, j]] += 1
    plt.bar(pxl.keys(), pxl.values(), color='red')
    plt.show()
    return pxl


def change(image, search, c):
    m, n = image.shape
    for i in range(m):
        for j in range(n):
            if image[i, j] == search:
                image[i, j] = c
    return image


def histogram_equalizer(image):                   # Histogram Equalization
    m, n = image.shape
    pixels = get_dict(image)
    prob = []
    levels = sorted(pixels.keys())
    temp = 0
    for i in range(257):
        if i in pixels.keys():
            temp += (pixels[i] / (m*n))
            prob.append(temp*(levels[len(levels)-1]-1))

    for i in range(len(levels)):
        image = change(image, levels[i], round(
            prob[i]))
    get_dict(image)
    display_image('Historically Equalised image', image)


''' Question 5 '''


def dec_to_bin(n):                   # Converting decimal to binary
    return bin(n).replace("0b", "")


def bit_plane(image):                   # Bit Plane
    a, b = (input("Enter Bits : ").split(" "))
    a = int(a)
    b = int(b)
    m, n = image.shape
    for i in range(m):
        for j in range(n):
            temp = [int(i) for i in dec_to_bin(image[i, j])]
            temp1 = (temp[1]*(pow(2, (a-1)))) + (temp[2]*(pow(2, (b-1))))
            image[i, j] = temp1
    display_image(f'Bit {a} and {b} image', image)


def main():                   # Main Function
    img = cv.imread("rog.jpg")
    display_image('Original Image', img)
    grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    display_image('Greyscale Image', grey_img)
    while True:
        print("Press 1. For Bit Conversion\n\t  2. To Zooming")
        print("\t  3. To Shrink\n\t  4. For gamma transformation\n\t  5. Histogram Equalization")
        print("\t  6. Bit Plane conversion\n\t  0. To Exit\n")
        user_input = int(input())
        if user_input == 1:
            bit_conversion(grey_img.copy())
        elif user_input == 2:
            zooming(grey_img.copy())
        elif user_input == 3:
            shrink(grey_img.copy())
        elif user_input == 4:
            gamma_correction(grey_img.copy())
        elif user_input == 5:
            histogram_equalizer(grey_img.copy())
        elif user_input == 6:
            bit_plane(grey_img.copy())
        elif user_input == 0:
            break
        else:
            print("Invalid input\n")

        cv.destroyWindow('Grey Image')


if __name__ == '__main__':
    main()
