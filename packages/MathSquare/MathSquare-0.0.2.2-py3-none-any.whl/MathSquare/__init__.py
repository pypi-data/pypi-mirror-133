#Area
def area_rectangle(a, b):
    if a and b > 0:
        result = a * b
        return result
    if a or b < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def area_quadrate(a):
    if a > 0:
        result = a * a
        return result
    if a < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def area_trapezoid(a, b, h):
    if a and b and h > 0:
        result = (1/2 * h * (a + b))
        return result
    if a or b or h < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def area_triangle(a, h):
    if a and h > 0:
        result = (1/2 * (a * h))
        return result
    if a or h < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def area_parallellogram(a, h):
    if a and h > 0:
        result = a * h
        return result
    if a or h < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def area_romb(a, h):
    if a and h > 0:
        result = a * h
        return result
    if a or h < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

#Pythagorean theorem
def pythagorean_hypotenuse(cathet, cathet1):
    if cathet and cathet1 > 0:
        hypotenuse = cathet**2 + cathet1**2
        result = hypotenuse ** (0.5)
        return result
    if cathet or cathet1 < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def pythagorean_cathet(hypotenuse, cathet):
    if hypotenuse and cathet > 0:
        cathet1 = hypotenuse**2 - cathet**2
        result = cathet1 ** (0.5)
        return result
    if hypotenuse or cathet < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

#Heron
def heron_area_triangle(a, b, c):
    if a and b and c > 0:
        p = 1/2 * (a + b + c)
        s = p * (p - a) * (p-b) * (p-c)
        result = s ** (0.5)
        return result
    if a or b or c < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

# joke
def lenin_area(l, h):
    if l and h > 0:
        result = l * h
        result = "Площадь вождя: " + str(result)
        return result
    if l or h < 0:
        return "Товарищ! Площадь вождя не может быть отрицательной!"

# circle
def radius(d):
    if d > 0:
        result = d / 2
        return result
    if d < 0:
        return "MathSquare: Sorry but the length can't have a negative value"

def diameter(r):
    if r > 0:
        result = r * 2
        return result
    if r < 0:
        return "MathSquare: Sorry but the length can't have a negative value"