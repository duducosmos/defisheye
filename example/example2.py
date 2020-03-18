from defisheye import Defisheye

dtypes = ['linear', 'equalarea', 'orthographic', 'stereographic']
formats = ['circular', 'fullframe']
fov = 180
img = "./images/example3.jpg"
for format in formats:
    for dtype in dtypes:
        pfov = 120
        img_out = f"./images/out/example3_{dtype}_{format}_{pfov}.jpg"

        obj = Defisheye(img, dtype=dtype, format=format, fov=fov, pfov=pfov)
        obj.convert(img_out)
