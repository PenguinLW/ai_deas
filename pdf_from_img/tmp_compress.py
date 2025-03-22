import img2pdf
with open("output.pdf", "wb") as file:
    file.write(img2pdf.convert("image.png"))
#import img2pdf
#with open("output.pdf", "wb") as file:
#    file.write(img2pdf.convert("image1.png", "image2.png"))
