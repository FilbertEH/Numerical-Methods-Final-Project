import numpy as np
from PIL import Image
 
#load test image
def loadImage():
    img = Image.open("original.png").convert("L")
    return np.array(img, dtype=np.float64)
 
#add salt and pepper noise
def addNoise(img, prob=0.05):
    noise = img.copy()
    rand = np.random.default_rng(1)
    map = rand.random(img.shape)
    noise[map < prob / 2] = 0
    noise[map > 1 - prob / 2] = 255
    return noise
 
#quadratic interpolation (newton polynomial)
def quadInterp(x0, y0, x1, y1, x2, y2, x):
    diff10 = (y1 - y0) / (x1 - x0)
    diff21 = (y2 - y1) / (x2 - x1)
    c = y0
    b = diff10
    a = (diff21 - diff10) / (x2 - x0)
    return a*(x - x1)*(x - x0) + b*(x - x0) + c
 
#removes noise
def deNoise(img, pepper=5, salt=250):
    denoised = img.copy()
    rows, cols = img.shape
 
    for r in range(rows):
        row = img[r]
        clean = (row > pepper) & (row < salt)
        position = np.where(clean)[0]
 
        for c in range(cols):
            if clean[c]:
                continue
 
            distance = np.abs(position - c)
 
            if len(position) < 3:
                denoised[r, c] = np.mean(row[position]) if len(position) > 0 else 128
                continue
 
            near3 = np.sort(position[np.argsort(distance)[:3]])
            x0, x1, x2 = near3
            val = quadInterp(x0, row[x0], x1, row[x1], x2, row[x2], c)
            denoised[r, c] = np.clip(val, 0, 255)
 
    return denoised

#PSNR algorithm to compare original and processed image
def PSNR(original, denoised):
    mse = np.mean((original - denoised) ** 2)
    if mse == 0:
        return float('inf')
    psnr = 20 * np.log10(255 / np.sqrt(mse))
    return psnr

#save noised and denoised images
def saveImages(imgN, imgD):
    Image.fromarray(imgN.astype(np.uint8)).save("noisy.png")
    Image.fromarray(imgD.astype(np.uint8)).save("restored.png")

#loads original image
#adds Salt and Pepper noise
#removes noise using Quadratic Interpolation
#compares Noisy and Restored images using PSNR
def main():
    original = loadImage()
    noisy = addNoise(original)
    restored = deNoise(noisy)

    psnrNoisy = PSNR(original, noisy)
    psnrRestored = PSNR(original, restored)

    print("PSNR Noisy    :", psnrNoisy, "dB")
    print("PSNR Restored :", psnrRestored, "dB")
    print("Improvement   :", psnrRestored - psnrNoisy, "dB")
    
    saveImages(noisy, restored)

if __name__ == "__main__":
    main()