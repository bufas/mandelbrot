import click
import fileinput
import json
import math
import plotter
import sys

from datetime import datetime

def calculate(c_re, c_im, maxIter, bailout):
  z_re = 0.0
  z_im = 0.0

  iterCnt = 1
  while iterCnt < maxIter:
    z_re_sq = z_re * z_re
    z_im_sq = z_im * z_im
    z_sq = z_re_sq + z_im_sq

    if z_sq >= bailout:
      break

    z_im = (2 * z_re * z_im) + c_im
    z_re = z_re_sq - z_im_sq + c_re

    iterCnt += 1

  if iterCnt < maxIter:
    zn = math.sqrt(z_sq)
    nu = math.log(math.log(zn, 2), 2)
    iterCnt = iterCnt + 1 - nu

  return iterCnt


def cumulativeHist(matrix, buckets):
  width = len(matrix)
  height = len(matrix[0])

  # Calculate histogram
  histogram = [0 for _ in xrange(buckets)]
  for x in xrange(width):
    for y in xrange(height):
      histogram[int(matrix[x][y]) - 1] += 1

  # Make cumulative
  for i in xrange(1, buckets):
    histogram[i] += histogram[i - 1]

  return histogram


def get_cs(frame, width, startrow, endrow):
  (xmin, ymin, xmax, ymax) = frame

  # Calc height of image
  xdist = xmax - xmin
  ydist = ymax - ymin
  height = int((ydist * width) / xdist)

  xstepsize = (xmax - xmin) / width
  ystepsize = (ymax - ymin) / height

  # Create the result matrix
  rows = min(endrow, height) - startrow
  result = [[None for _ in xrange(width)] for _ in xrange(rows)]

  for py in xrange(startrow, min(endrow, height)):
    for px in xrange(width):
      result[py - startrow][px] = xmin + (px * xstepsize), ymin + (py * ystepsize)

  return result


frames = [
  (-0.20141350000000002, 0.6478721249999999, -0.19029962500000003, 0.6552813749999999),    # Seahorse
  (-0.7671643, -0.09465555000000009, -0.7662004000000001, -0.09401295000000008),           # 1 arm  (ratio 3/2)
  (-0.7458228152069135,0.10508519377204056,-0.7458224376648389,0.10508544546675697),       # 2 arms (ratio 3/2)
  (-0.7272900479135964,-0.19095194276607555,-0.7272900057591827,-0.19095191466313305),     # 4 arms (ratio 3/2)
]

std_palette = [
  [(15, 15, 15), (15, 15, 15), (51, 0, 51), (211, 200, 211), (211, 200, 211)],  # Purple
  [(15, 15, 15), (15, 15, 15), (0, 51, 51), (200, 211, 211), (200, 211, 211)],  # Green
  [(15, 15, 15), (15, 15, 15), (0, 51, 102), (200, 222, 222), (200, 222, 222)]  # Blue
]


@click.group()
def mandelbrot():
  pass;


@mandelbrot.command(name='calc-x')
@click.argument('frame', type=click.INT)
@click.argument('width', type=click.INT)
@click.argument('startrow', type=click.INT)
@click.argument('endrow', type=click.INT)
@click.argument('outputfile', type=click.File('w'))
@click.option('--iterations', type=click.INT, default=4096)
@click.option('--bailout', type=click.INT, default=4)
def claculate_x(frame, width, startrow, endrow, outputfile, iterations, bailout):
  data = get_cs(frames[frame], width, startrow, endrow)
  result = [0 for _ in xrange(len(data))]
  for row, c_row in enumerate(data):
    result[row] = map(lambda c: calculate(c[0], c[1], iterations, bailout), c_row)
  json.dump(result, outputfile)


@mandelbrot.command(name='merge-rows')
@click.argument('inputfiles', nargs=-1, type=click.File('r'))
@click.argument('outputfile', type=click.File('w'))
def merge_rows(inputfiles, outputfile):
  result = []
  for inputfile in inputfiles:
    result.extend(json.load(inputfile))
  json.dump(result, outputfile)


@mandelbrot.command(name='gen-image')
@click.argument('palette', type=click.INT)
@click.argument('inputfile', type=click.File('r'))
@click.option('--iterations', type=click.INT, default=4096)
def generate_image(palette, inputfile, iterations):
  matrix = json.load(inputfile)

  histogram = cumulativeHist(matrix, iterations)
  ranges = [0.0, 0.5, 0.7, 0.92, 1.0]
  colors = std_palette[palette]
  inside = colors[-1]
  image = plotter.output(matrix, histogram, iterations, ranges, colors, inside)
  col = colors[2]
  end = colors[-1]
  filename = '{}x{}_{:%y-%m-%d_%H-%M-%S}'.format(len(matrix[0]), len(matrix), datetime.now())
  image.save('out/' + filename + '.bmp')


if __name__ == '__main__':
  mandelbrot()
