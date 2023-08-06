# informartion

__author__ = "Zedikon"
__maintainer__ = "Zedikon"
__email__ = "mrzedikon@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__version__ = "0.0.7"
__copyright__ = "Copyright Zedikon 2022"

# MathSquare

# triangle
class triangle():
    def area(a, h):
        if a and h > 0:
            result = (1/2 * (a * h))
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"
    
    def perimetr(a, b, c):
        if a and b and c > 0:
            result = a + b + c
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"
    
# rectangle
class rectangle():
    def area(a, b):
        if a and b > 0:
            result = a * b
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"
    
    def perimetr(a, b):
        if a and b > 0:
            result = 2 * (a + b)
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# quadrate
class quadrate():
    def area(a):
        if a > 0:
            result = a * a
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"
    def perimetr(a):
        if a > 0:
            result = 4 * a
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# trapezoid
class trapezoid():
     def trapezoid(a, b, h):
        if a and b and h > 0:
            result = (1/2 * h * (a + b))
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

     def trapezoid(a, b, c, d):
        if a and b and c and d > 0:
            result = a + b + c + d
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# parallellogram      
class parallellogram():
    def area(a, h):
        if a and h > 0:
            result = a * h
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"
 
    def perimetr(a, b):
        if a and b > 0:
            result = 2 * (a + b)
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# romb
class romb():
    def area(a, h):
        if a and h > 0:
            result = a * h
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

    def perimetr(a):
        if a > 0:
            result = 4 * a
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# Pythagorean theorem
class pythagorean():
    def hypotenuse(cathet, cathet1):
        if cathet and cathet1 > 0:
            hypotenuse = cathet**2 + cathet1**2
            result = hypotenuse ** (0.5)
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

    def cathet(hypotenuse, cathet):
        if hypotenuse and cathet > 0:
            cathet1 = hypotenuse**2 - cathet**2
            result = cathet1 ** (0.5)
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# Heron
class heron():
    def area_triangle(a, b, c):
        if a and b and c > 0:
            p = 1/2 * (a + b + c)
            s = p * (p - a) * (p-b) * (p-c)
            result = s ** (0.5)
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

# joke
def lenin_area(l, h):
    if l and h > 0:
        result = l * h
        result = "Площадь вождя: " + str(result)
        return result
    else:
        return "Товарищ! Площадь вождя не может быть отрицательной!"

# sin, cos, tg triangle
class sin():
    def angle(cathet, hypotenuse):
        if cathet and hypotenuse > 0:
            result = cathet / hypotenuse
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

class cos():
    def angle(cathet, hypotenuse):
        if cathet and hypotenuse > 0:
            result = cathet / hypotenuse
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

class tg():
    def angle(cathet, cathet1):
        if cathet and cathet1 > 0:
            result = cathet / cathet1
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"


# circle
class circle():
    def radius(d):
        if d > 0:
            result = d / 2
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

    def diameter(r):
        if r > 0:
            result = r * 2
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

    def area(r):
        if r > 0:
            result = 3.141592653589793 * (r**2)
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

    def perimetr(r):
        if r > 0:
            result = 2 * 3.141592653589793 * r
            return result
        else: 
            "MathSquare: Sorry but the length can't have a negative value"

# tetrahedron
class tetrahedron():
    def area(a):
        if a > 0:
            result = (a ** 2) * (3 ** 0.5)
            return result
    
    def height(a):
        if a > 0:
            result = a * (6 ** 0.5) / 3
            return result

    def volume(a):
        if a > 0:
            result = (a ** 3) * (2 ** 0.5) / 12 
            return result
        else:
            return "MathSquare: Sorry but the length can't have a negative value"

    class radius():
        def described_sphere(a):
            if a > 0:
                result = a * (6 ** 0.5) / 4
                return result
            else:
                return "MathSquare: Sorry but the length can't have a negative value"

        def inscribed_sphere(a):
            if a > 0:
                result = a * (6 ** 0.5) / 12
                return result
            else:
                return "MathSquare: Sorry but the length can't have a negative value"

    

# Copyright Zedikon 2022
# All rights reserved