def text_circle(rad, ch='*'):
    xscale = 4

    #Maximum diameter, plus a little padding
    width = 12 + int(0.5 + xscale * rad)

    rad2 = rad ** 2
    for y in range(-rad, rad + 1):
        #Find width at this height
        x = int(round(0.5 + xscale * (rad2 - y ** 2) ** 0.5))
        s = ch * x
        print( s.center(width))

for i in range(1, 10):
    text_circle(i)