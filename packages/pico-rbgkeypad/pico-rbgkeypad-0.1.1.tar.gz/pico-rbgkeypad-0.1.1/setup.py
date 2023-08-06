from setuptools import setup

setup(
    name="pico-rbgkeypad",
    version="0.1.1",
    description="A Python class for controlling the Pimoroni RGB Keypad for the Raspberry Pi Pico.",
    long_description="""A Python class for controlling the [Pimoroni RGB Keypad](https://shop.pimoroni.com/products/pico-rgb-keypad-base) for the [Raspberry Pi Pico](https://www.raspberrypi.org/documentation/pico/getting-started/).

Compatible with MicroPython and CircuitPython.

```python
keypad = RGBKeypad()

# make all the keys red
keypad.color = (255, 0, 0)

# turn a key blue when pressed
while True:
    for key in keypad.keys:
        if key.is_pressed():
            key.color = (0, 0, 255)
```

![pimoroni rgb keypad](https://cdn.shopify.com/s/files/1/0174/1800/products/pico-addons-2_1024x1024.jpg?v=1611177905)""",
    long_description_content_type="text/markdown",
    url="https://github.com/martinohanlon/pico-rbgkeypad",
    author="Martin O'Hanlon",
    author_email="martin@ohanlonweb.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
    keywords="raspberry pi pico rgb keypad pimoroni",
    packages=["rgbkeypad"],
)