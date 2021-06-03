from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math

# these are the characters that make up the image, can do many combinations for different effects

chars = "$@B%8&WM#*oahkbdpqwmZO0GQLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
#chars = list(".,/\[]{}()OQPHZNRGKBMX")

charArr = list(chars)
charLen = len(charArr)
intvl = charLen / 256  # index normalizer


# max val of input is 255
# multiplying by len/256 gives seminormalized value within chars (ratio * length of list)
def grey2char(idx):
    return charArr[math.floor(idx * intvl)]


print("Enter Image Name: ")
inImg = input()

# open image, get size
image = Image.open("input_images/" + inImg + ".jpg")
w, h = image.size

# get scale factor,
# scale image to try to match original
print("Enter scale delta:\n"
      "0-8: Pixelated\n"
      "8-15: Low Res\n"
      "15-25: Starting to get pretty large\n"
      "25+: Pushing the limits of your processing abilities"
      )
print("WARNING: Large Scale Deltas will take a while to process and files become quite large rather quickly")
delta = float(input())
delta = delta / 10  # make a bit more reasonable

print("--- ASCII-ifying ---")
# avg ratio of char size
W = 6
H = 9

# init output text file
out = open("out.txt", "w")

# usually need to squash characters bc theyre not square
image = image.resize((int(w * delta), int(h * delta * (W / H))), Image.NEAREST)
w, h = image.size

pix = image.load()

# create output image

#blank black background
outImg = Image.new('RGB', (W * w, H * h), color=(0, 0, 0))
ddraw = ImageDraw.Draw(outImg)

# for each pixel,
# convert to greyscale
# greyscale char index correspond
# write char to img/txt
# once end of row, need to write newline it doesnt know
for i in range(h):
    for j in range(w):
        (r, g, b) = pix[j, i]
        h = int((r + g + b) / 3)
        pix[j, i] = (h, h, h)

        out.write(grey2char(h))
        ddraw.text((j * W, i * H), grey2char(h), fill=(r, g, b))

    out.write('\n')

print("--- Edit Image ---")
print("100 = default")

bright = ImageEnhance.Brightness(outImg)

print("Brightness %: ")
Bd = float(input())
Bd = Bd / 100.0
B = bright.enhance(Bd)
#B.save("brightness-change.jpg")

###########################################
###pipe brightness image into contrast filter

contrast = ImageEnhance.Contrast(B)

print("Contrast %:")
Cd = float(input())
Cd = Cd / 100.0
C = contrast.enhance(Cd)
#C.save('contrast-change.jpg')

###########################################
###pipe contrast image into sharpest filter

sharp = ImageEnhance.Sharpness(C)

print("Sharpness %:")
Sd = float(input())
Sd = Sd / 100.0
S = sharp.enhance(Sd)
#S.save("brightness-change.jpg")

print("Save Image Name: ")
imgName = input()
S.save("output_images/" + imgName + ".jpg")
print("!--- Conversion Complete ---!")
