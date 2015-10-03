Mandelbrot image generator
==========================

Start out by running

```
virtualenv --prompt="(mandelbrot) " env
. env/bin/activate
pip install -r requirements.txt
python setup.py develop
```

You will now be able to run the `mandelbrot` program.

```
mandelbrot --help
```

There are three commands, `calc-x`, `merge-rows`, and `gen-image`. To generate an image you first need to calculate the X values, and then generate an image based on these.


Image generation example
------------------------
To generate an image, run the following commands (note: it might take several minutes)

```
mandelbrot calc-x 2 350 0 350 x_f2_w350.json
mandelbrot gen-image 1 x_f2_w350.json
```

A new file will magically appear in the `out` folder.

![Example 1](http://i57.tinypic.com/2cyl2qe.jpg)
![Example 2](http://i61.tinypic.com/23m25ax.jpg)

Calculate X values
------------------
This command will generate the X values for each pixel in the image. The X value of a pixel is used to determine its color. The row parameters (`start_row` and `end_row`) can be used to split up the computation of a large image. This can be very useful for parallelization of the computations.

```
mandelbrot calc-x --help
```


Merging rows
------------
Merging rows is only necessary if you used `calc-x` multiple times to parallelize the computation. It simply merges the output from all the `calc-x` executions into a single file which can be fed into `gen-image`.

```
mandelbrot merge-rows --help
```


Generating the image
--------------------
When you have calculated the X values using `calc-x`, `gen-image` can be used to transform it into a .bmp image file. The reason that these two tasks are split up is because the same output from `calc-x` can be used to generate multiple images with different colors (i.e. no need to wait for the X computation to try out different colors).

```
mandelbrot gen-image --help
```


TODO
====
  - Improve performance of `calc-x`
  - Improve performance of `gen-image`
  - Remove Pillow dependency
  - Take a frame as parameter to `calc-x`
  - Take color palettes as parameter `gen-image`
  - Document the command parameters
  - Implement bezier transforms between colors in color palettes
  - Implement more smoothing techniques