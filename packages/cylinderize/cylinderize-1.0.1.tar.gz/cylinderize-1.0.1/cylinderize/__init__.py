from matplotlib.pyplot import figure, show
from PIL import ImageDraw
from numpy import array, linspace, meshgrid, pi, cos, sin
def cylinderize(text:str) -> None:
    w,h = (len(max(text.split("\n"), key=len))+1)*6,(text.count("\n")+1)*15
    im=ImageDraw.Image.new("L",(w,h))
    ImageDraw.Draw(im).text((0,0),text,fill=1)
    THETA, Z = meshgrid(linspace(0, 2 * pi, w), linspace(0, 1, h))
    figure().add_subplot(projection="3d").plot_surface(cos(THETA), sin(THETA), Z, facecolors=[[[i]*3 for i in j] for j in array(im)[::-1]], rstride=1, cstride=1)
    show()