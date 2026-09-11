# Simple-Image-Editor-in-Python-



# Image Editor Code

This project is a Python-based, interactive command-line image editor. It utilizes a terminal menu to let users load images, apply various visual transformations, and save their edited results.

## Dependencies
To run `Image editor code.py`, you will need the following Python libraries installed:
* `numpy`
* `matplotlib`
* `os`


## Features & Usage
When you run the script, you are greeted with a continuous loop menu that prompts you for inputs. You must load an image first before accessing the main editing features.

### Core Image Operations
* **Load an Image (`l`)**: Prompts the user for a filename to open and display the image.
* **Save the Picture (`s`)**: Allows the user to save the currently edited image to a specified file name and directory.
* **Exit (`e`)**: Safely breaks the loop and exits the program.

### Image Adjustments & Filters
Once an image is loaded, you can apply several effects. If a mask (selection) is active, these effects only apply to the selected area.

* **Brightness (`1`)**: Adjusts the image brightness based on a user-provided integer between -255 and 255.
* **Contrast (`2`)**: Alters the image contrast using a scaling factor, accepting a value between -255 and 255.
* **Grayscale (`3`)**: Converts the image or selection to black and white using a weighted average calculation of the RGB color channels.
* **Blur (`4`)**: Softens the image by applying a 3x3 averaging kernel to the pixels.
* **Edge Detection (`5`)**: Highlights the edges in the image using a specific convolution kernel, automatically adding brightness so the result is visible.
* **Embossed Effect (`6`)**: Applies a 3x3 directional kernel to give the image a 3D shadow or embossed appearance.



### Selection Tools
The program allows for selective editing through a masking system. The active selection boundary is highlighted on the display with a red outline.
* **Rectangle Select (`7`)**: Creates a selection mask based on top-left and bottom-right X/Y coordinates provided by the user.
* **Magic Wand Select (`8`)**: Selects a contiguous area of similar colors. The user inputs a starting X/Y coordinate and a color distance threshold, and the program uses a region-growing algorithm to select matching neighboring pixels.



## How to Run

Simply execute the Python script in your terminal. The program uses `matplotlib`'s interactive mode (`plt.ion()`) to continuously update and display the image as you make edits.
