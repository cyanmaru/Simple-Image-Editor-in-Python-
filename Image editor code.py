import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os 


def menu():

    #initialise image and mask as empty arrays to ensure they exist before user starts editing
    image = np.array([])
    mask = np.array([])

    #Loop to continuosuly prompt user til they choose to exit
    while True:
        if image.size == 0: 
            #only show limited options if user hasn't loaded their image
            print("\n\nWelcome! What do you want to do?")
            print("e - exit")
            print("l - load an image")
            print("You must load an image before accessing other options!^-^")
            choice = input("\nYour choice: ").strip().lower()  #ensure any capitalised inputs or inputs with spaces are accepted too
            
        else: 
            #full menu once image is loaded
            print("Okay, what do you want to do next?")
            print("e - exit")
            print("l - load an image")
            print("s - save this picture")
            print("1 - adjust brightness")
            print("2 - adjust contrast")
            print("3 - apply grayscale")
            print("4 - apply blur")
            print("5 - edge detection")
            print("6 - embossed effect")
            print("7 - rectangle select")
            print("8 - magic wand select")
            choice = input("\nYour choice: ").strip().lower()
       
        #if user wants to exit program
        if choice == 'e':
            print("Goodbye!")
            break
        
        #load image & display it
        elif choice == 'l':
            filename = input("What is the name of the image file to upload?: ").strip()
            image, mask = load_image(filename)
            display_image(image,mask)
            print("\n\nImage loaded successfully!")

        #saving of edited image   
        elif choice == 's':
                filename = input("Name this image: ").strip()
                save_image(filename,image)
                print(f"\n\nSaved as {filename}!")
        
        #brightness editing
        elif choice == '1':
            value = int(input("\nEnter a number between -255 and 255\n(Positive number for higher brightness, Negative number for lower brightness): "))
              
            try:
                if value < -255 or value > 255:
                    print("\n\nInvalid input. Value must be between -255 and 255!")
                else: 
                    edited_image = change_brightness(image, value)
                    image = np.where( mask[:, :, None]==1, edited_image, image) #to ensure it's applying brightness to only masked area
                    display_image(image, mask)
                    print(f"\n\nBrightness changed by {value}!")
              
            except ValueError:
                print("\n\nInvalid input. Please enter a number...")

       #contrast editing 
        elif choice == '2':
            value = int(input("\nEnter a number between -255 and 255\n(Positive number for higher contrast, Negative number for lower contrast): "))
        
            try:
                if value < -255 or value > 255:
                    print("\n\nInvalid input. Value must be between -255 and 255!")
                else:
                    edited_image = change_contrast(image, value)
                    image = np.where( mask[:, :, None]==1, edited_image, image)
                    display_image(image, mask)
                    print(f"\n\nContrast changed by {value}!")
                    
            except ValueError:
                print("\n\nInvalid input. Please enter a number.")

        #grayscale effect       
        elif choice == '3':
            edited_image = grayscale(image)
            image = np.where( mask[:, :, None]==1, edited_image, image)
            display_image(image, mask)
            print("\n\nGrayscale Effect applied!")

        #blur effect   
        elif choice == '4':
            edited_image = blur_effect(image)
            image = np.where( mask[:, :, None]==1, edited_image, image)
            display_image(image, mask)
            print("\n\nBlurred Effect applied!")
        
        #edging :)
        elif choice == '5':
            edited_image = edge_detection(image)
            image = np.where( mask[:, :, None]==1, edited_image, image)
            display_image(image, mask)
            print("\n\nEdge Detection applied!")

        #emBOSS effect
        elif choice == '6':
            edited_image = embossed(image)
            image = np.where( mask[:, :, None]==1, edited_image, image)
            display_image(image, mask)
            print("\n\nEmbossed Effect applied!")

        #rectangle select      
        elif choice == '7':
            try:
                #choosing coords for the rectangle select boundaries
                x1 = int(input("\nEnter the top left x-coordinate: "))
                y1 = int(input("Enter the top left y-coordinate: "))
                x2 = int(input("Enter the bottom right x-coordinate: "))
                y2 = int(input("Enter the bottom right y-coordinate: "))

                top_left = (x1, y1)
                bottom_right = (x2, y2)
                
                #ensure coordinates are within image bounds 
                if (0 <= x1 < image.shape[1] and 0 <= y1 < image.shape[0] and
                    0 <= x2 < image.shape[1] and 0 <= y2 < image.shape[0]):
                    mask = rectangle_select(image, top_left, bottom_right) 
                    
                    display_image(image, mask)
                    print(f"\n\nRectangle selected from ({x1}, {y1}) to ({x2}, {y2}).")
                
                else:
                    print("\nCoordinates out of bounds of image! Try again.")
                   
                    
            except ValueError:
                print("\nInvalid input. Please enter number coordinates.")
              

        #magic wand     
        elif choice == '8':
            try:
                x = int(input("\nEnter the x-coordinate of the starting pixel: "))
                y = int(input("Enter the y-coordinate of the starting pixel: "))
                thres = float(input("Enter the threshold value (e.g., 200): "))
            
                #ensure starting coords are within image bounds
                if (0 <= x < image.shape[1] and 0 <= y < image.shape[0]):
                    mask = magic_wand_select(image, (x, y), thres)  #apply magic wand 
                    print(f"\n\nMagic wand selection done with threshold {thres} at pixel ({x}, {y}).")
                    display_image(image, mask)  #display image with the selection
            
                else:
                    print("\n\nCoordinates out of image bounds. Try again.") #error handling for out of bounds
                
            except ValueError:
                print("\n\nInvalid input. Please enter integer coordinates and a valid threshold.")
  
              
        else: 
            print("\n\n\nInvalid choice. Please try again.\n")
            
            

def change_brightness(image, value):
    copyofimage = np.copy(image)  #make copy to not modify original input directly
    return np.clip(copyofimage + value, 0, 255)  #adjust brightness by add or subtracting fixed value to or from each pixel


def change_contrast(image, value):
    F = (259 * (value + 255)) / (255 * (259 - value))
    copyofimage = np.copy(image)
    return np.clip(F*(copyofimage-128) + 128, 0, 255)  #adjust contrast based on scaling factor



#convert each pixel to grayscale using a weighted average of the RGB channels
def grayscale(image):
    copyofimage = np.copy(image)
    grayed_image = np.zeros_like(copyofimage)  #initialize new array with the same shape as the original
    
    for r in range(copyofimage.shape[0]):  #loop over every row of pixels
        for c in range(copyofimage.shape[1]):  #loop over every column of pixels
            gray_value = int(0.3 * copyofimage[r, c, 0] + 0.59 * copyofimage[r, c, 1] + 0.11 * copyofimage[r, c, 2])
            grayed_image[r, c] = [gray_value, gray_value, gray_value]
    
    return grayed_image


#apply blur effect using kernel given by averaging values of neighbouring pixels
def blur_effect(image):
   copyofimage = np.copy(image)
   
   kernel = np.array([[0.0625, 0.125, 0.0625],
                       [0.125, 0.25, 0.125],
                       [0.0625, 0.125, 0.0625]]) #kernel as given by prof
                      
   height, width, channels = copyofimage.shape 
   
   blurred_image = np.copy(copyofimage) #initialize new image to store blurred result
   
   for r in range(1, height-1):  #loop over each pixel, avoiding the edges
        for c in range(1, width-1):  
            for channel in range(channels):  #apply the kernel to each colour channel
                region = copyofimage[r-1:r+2, c-1:c+2, channel]
                blurred_value = np.sum(region * kernel) 
                blurred_image[r, c, channel] = np.clip(blurred_value, 0, 255) 

   return blurred_image



def edge_detection(image):
    K = np.array([[-1, -1, -1],
                  [-1,  8, -1],
                  [-1, -1, -1]]) #kernel as given by prof

    copyofimage = np.copy(image)
    
    height, width, channels = copyofimage.shape
    edged_image = np.copy(copyofimage)

    for r in range(1, height - 1):  #loop over each pixel, avoiding the edges
        for c in range(1, width - 1):
            for channel in range(channels):  #apply the edge detection filter to each color channel
                region = copyofimage[r-1:r+2, c-1:c+2, channel]
                
                edged_value = np.sum(region * K)
                
                edged_image[r, c, channel] = np.clip(edged_value + 128, 0, 255) #increase brightness by 128 since it would be way too dark w/o

    return edged_image

   

def embossed(image):
    K = np.array([[-1, -1, 0],
                  [-1,  0, 1],
                  [0, 1, 1]])  #kernel as given by prof
                  
    copyofimage = np.copy(image)
    
    height, width, channels = copyofimage.shape
    embossed_image = np.copy(copyofimage)

    for r in range(1, height - 1):  #loop over each pixel, avoiding the edges
        for c in range(1, width - 1):
            for channel in range(channels):   #apply the emboss effect on each color channel
                region = copyofimage[r-1:r+2, c-1:c+2, channel]
                
                embossed_value = np.sum(region * K)
                
                embossed_image[r, c, channel] = np.clip(embossed_value + 128, 0, 255) #similar to edge

    return embossed_image



def rectangle_select(image, start, end):
    mask = np.zeros((image.shape[0], image.shape[1]), dtype=float)  #initialise mask with same shape, filled with 0s. selected rectangle will have value of 1.
    mask[start[0]:end[0]+1, start[1]:end[1]+1] = 1  

    return mask


def colour_distance(pixel1, pixel2):
    delta_R = pixel1[0] - pixel2[0]
    delta_G = pixel1[1] - pixel2[1]
    delta_B = pixel1[2] - pixel2[2]
    
    avg_R = (pixel1[0] + pixel2[0]) / 2
    
    distance = np.sqrt((2 + avg_R/256) * delta_R**2 + 4 * delta_G**2 + (2 + (255 - avg_R)/ 256) * delta_B**2)
    
    return distance


def magic_wand_select(image, x, thres):   
    height, width, _ = image.shape  
    mask = np.zeros((height, width))
    start_pixel = image[x[1], x[0]]  

    #initialize a stack to hold the pixels to check for similarity based on the threshold
    stack = [(x[1], x[0])]
    mask[x[1], x[0]] = 1  

    while stack:
        r, c = stack.pop()  #pop a pixel position from the stack

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  #check neighbouring pixels from up below left right
            r_new, c_new = r + dr, c + dc
            if 0 <= r_new < height and 0 <= c_new < width and mask[r_new, c_new] == 0:  #ensure the neighbour is within image bounds and hasn't been selected already
                neighbour_pixel = image[r_new, c_new]  #calculate the colour distance between start pixel and the neighbouring pixel.
                dist = colour_distance(start_pixel, neighbour_pixel)

                if dist <= thres:  #if the distance is within the threshold, mark neighbour pixel as selected
                    mask[r_new, c_new] = 1
                    stack.append((r_new, c_new))

    return mask


def compute_edge(mask):           
    rsize, csize = len(mask), len(mask[0]) 
    edge = np.zeros((rsize, csize))
    if np.all((mask == 1)): return edge        
    for r in range(rsize):
        for c in range(csize):
            if mask[r][c] != 0:
                if r == 0 or c == 0 or r == len(mask) - 1 or c == len(mask[0]) - 1:
                    edge[r][c] = 1
                    continue
                
                is_edge = False                
                for var in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    r_temp = r + var[0]
                    c_temp = c + var[1]
                    if 0 <= r_temp < rsize and 0 <= c_temp < csize:
                        if mask[r_temp][c_temp] == 0:
                            is_edge = True
                            break
    
                if is_edge == True:
                    edge[r][c] = 1
            
    return edge


def save_image(filename, image):
    try:
        img = image.astype(np.uint8) 
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        mpimg.imsave(filename, img)
    except Exception as e:
        print(f"Problem occured while saving image: {e}")


def load_image(filename):
    img = mpimg.imread(filename)
    if len(img[0][0]) == 4:  # if png file
        img = np.delete(img, 3, 2)
    if type(img[0][0][0]) == np.float32:  # if stored as float in [0, .., 1] instead of integers in [0, .., 255]
        img = img * 255
        img = img.astype(np.uint8)
    mask = np.ones((len(img), len(img[0])))  # create a mask full of "1" of the same size of the loaded image
    img = img.astype(np.int32)
    return img, mask


def display_image(image, mask):
    tmp_img = image.copy()

    edge = compute_edge(mask)
    for r in range(len(image)):
        for c in range(len(image[0])):
            if edge[r][c] == 1:
                tmp_img[r][c][0] = 255
                tmp_img[r][c][1] = 0
                tmp_img[r][c][2] = 0

    plt.imshow(tmp_img)
    plt.axis('off')
    plt.draw() 
    plt.show() 


def check_image_loaded(image):
    if image is None:
        print("\n\nThere's no image! Please load an image first... \n")
        return False
    return True




if __name__ == "__main__":
    plt.ion()  # Interactive mode
    menu()

 