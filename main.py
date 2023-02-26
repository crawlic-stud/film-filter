from PIL import Image
import numpy as np

from pathlib import Path
import math 


def apply_hald_clut(hald_img: Image.Image, img: Image.Image):
    clut_size = int(round(math.pow(hald_img.width, 1/3)))
    # We square the clut_size because a 12-bit HaldCLUT has the same amount of information as a 144-bit 3D CLUT
    scale = (clut_size * clut_size - 1) / 255
    # Convert the PIL image to numpy array
    img = np.asarray(img)
    # We are reshaping to (144 * 144 * 144, 3) - it helps with indexing
    hald_img = np.asarray(hald_img).reshape(clut_size ** 6, 3)
    # Figure out the 3D CLUT indexes corresponding to the pixels in our image
    clut_r = np.rint(img[:, :, 0] * scale).astype(int)
    clut_g = np.rint(img[:, :, 1] * scale).astype(int)
    clut_b = np.rint(img[:, :, 2] * scale).astype(int)
    filtered_image = np.zeros((img.shape))
    # Convert the 3D CLUT indexes into indexes for our HaldCLUT numpy array and copy over the colors to the new image
    filtered_image[:, :] = hald_img[clut_r + clut_size ** 2 * clut_g + clut_size ** 4 * clut_b]
    filtered_image = Image.fromarray(filtered_image.astype('uint8'), 'RGB')
    return filtered_image


img = Image.open(Path.cwd() / "input.jpg") 
identites = Path.cwd() / "identities"
polaroid_identites = identites / "Polaroid"
kodak_identites = identites / "Kodak"
fuji_identites = identites / "Fuji"
clut_identites = fuji_identites.glob("*.png")

identites_i_like = []
for identity in clut_identites:
    print("CLUT name:", identity.name)
    hald_clut = Image.open(identity)
    transformed_img = apply_hald_clut(hald_clut, img)
    transformed_img.save("output.png")
    key = input("add filter [+] or skip [ENTER]:")
    if key == "+":
        identites_i_like.append(identity.name)
print(identites_i_like)
