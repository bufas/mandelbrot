from setuptools import setup

setup(
    name='mandelbrot',
    version='0.1.0',
    description='Generate images of the Mandelbrot fractal',
    packages=['mandelbrot'],
    entry_points={
        'console_scripts': ['mandelbrot = mandelbrot.main:mandelbrot']
    }
)