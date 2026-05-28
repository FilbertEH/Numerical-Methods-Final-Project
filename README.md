# Image Denoising using Quadratic Interpolation

Final project for Numerical Methods. The goal is to take an image, add Salt and Pepper noise to it, and then remove the noise using Newton's Quadratic Interpolation.

## What it does

1. Loads an image (grayscaled)
2. Adds Salt and Pepper noise to it (randomly sets some pixels to black or white)
3. Detects the noisy pixels and replaces them using Quadratic Interpolation
4. Compares the noisy and restored image using PSNR to measure how well it worked
5. Saves the noisy and restored images

## How it works

### Salt and Pepper Noise
Salt and pepper noise randomly corrupts pixels by setting them to either 0 (black/pepper) or 255 (white/salt). The script corrupts 5% of the image by default.

### Quadratic Interpolation
For each noisy pixel, the script finds the 3 nearest clean pixels in the same row and uses Newton's divided differences formula to estimate what the pixel value should be.

The formula used is:

P(x) = a(x - x1)(x - x0) + b(x - x0) + c

where a, b, c are the Newton coefficients calculated from the 3 nearest clean neighbors.

### PSNR
PSNR (Peak Signal-to-Noise Ratio) is used to measure image quality. Higher dB means the restored image is closer to the original. Anything above 30 dB is generally considered good.

## How to run

1. Place your image in the same folder as denoise.py and rename it to original.png
2. Install dependencies
```
pip install numpy pillow
```
3. Run the script
```
python denoise.py
```

## Output

After running, the folder will have:

- noisy.png     : the image with noise added
- restored.png  : the image after denoising

The terminal will also print the PSNR values before and after denoising.

## Requirements

- Python 3
- numpy
- pillow
