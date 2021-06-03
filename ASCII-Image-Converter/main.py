from PIL import Image, ImageDraw, ImageFont
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

print("Save Image Name: ")
imgName = input()
outImg.save("output_images/" + imgName + ".jpg")
print("!--- Conversion Complete ---!")
