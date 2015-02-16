""" Creates random functions for 'R', 'G' and 'B' 
    and uses those functions to make a picture """

from PIL import Image
import random
import math


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    ops = ['x', 'y', 'prod', 'avg', 'cos_pi', 'sin_pi', 'cos_7', 'fun_func']
    if max_depth <= 0:
        ops = ops[:2]
    elif min_depth > 0:
        ops = ops[2:]
    this_op = random.choice(ops)
    func = [this_op]

    if this_op not in ['x', 'y']:
        func.append(build_random_function(min_depth-1, max_depth-1))
        if this_op in ['prod', 'avg', 'fun_func']:
            func.append(build_random_function(min_depth-1, max_depth-1))
    return func


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y (both floats)
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['prod',['x'],['y']],2,3)
        6
        >>> evaluate_random_function(['avg',['x'],['y']],1,3)
        2
    """
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'cos_pi':
        return math.cos(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi':
        return math.sin(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'cos_7':
        return math.cos(7*evaluate_random_function(f[1], x, y))
    elif f[0] == 'prod':
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == 'avg':
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y)) / 2
    elif f[0] == 'fun_func':
        a = evaluate_random_function(f[1], x, y)
        b = evaluate_random_function(f[2], x, y)
        return math.exp(-50 * (a + 1)) - math.exp(-1 * (b + 1))
    return 'Error: not a valid function'


def remap_interval(val, in_start, in_end, out_start, out_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    val = float(val)  # stupid python
    percent = (val - in_start) / (in_end - in_start)
    return percent * (out_end - out_start) + out_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    return int(remap_interval(val, -1, 1, 0, 255))


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    red_function = build_random_function(3, 5)
    green_function = build_random_function(3, 5)
    blue_function = build_random_function(3, 5)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    for i in range(31, 51):
        generate_art("picture%d.png" %i)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
