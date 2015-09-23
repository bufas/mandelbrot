from PIL import Image, ImageDraw
import math


def output(matrix, histogram, maxIter, ranges, colors, inside):
  height = len(matrix)
  width = len(matrix[0])

  im = Image.new('RGB', (width, height), color=inside)
  canvas = ImageDraw.Draw(im)

  pixelsOutsideSet = float(histogram[-2])

  for x in xrange(width):
    for y in xrange(height):
      if matrix[y][x] < maxIter:
        fracPart = matrix[y][x] - int(matrix[y][x])
        n1 = histogram[int(matrix[y][x]) - 1] / pixelsOutsideSet
        n2 = histogram[int(matrix[y][x])] / pixelsOutsideSet
        dist = n2 - n1
        n = n1 + (dist * fracPart)
        canvas.point((x,y), fill=getColor(n, ranges, colors))

  return im


def getColor(n, ranges, colors):
  for i in xrange(len(ranges)):
    if n < ranges[i]:
      # Normalize n
      fracSpan = ranges[i] - ranges[i - 1]
      n = (n - ranges[i - 1]) / fracSpan

      # Figure out the color by linear interpolation
      startColor = colors[i - 1]
      endColor = colors[i]
      r = startColor[0] + ((endColor[0] - startColor[0]) * n)
      g = startColor[1] + ((endColor[1] - startColor[1]) * n)
      b = startColor[2] + ((endColor[2] - startColor[2]) * n)
      return int(r), int(g), int(b)