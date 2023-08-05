import jax.numpy as jnp
from typing import Tuple
from jaxson.utils import clamp


class Canvas:
    def __init__(self, width=100, height=100):
        self.x_shape = width
        self.y_shape = height

    def zeros(self) -> jnp.ndarray:
        return jnp.zeros(())

    def xy(self):
        return (
            jnp.linspace(0.0, 1.0, self.x_shape),
            jnp.reshape(jnp.linspace(0.0, 1.0, self.y_shape), (self.y_shape, 1)),
        )

    def apply_brightness(self, input: jnp.array, brightness: float):
        return input * brightness

    def apply_color(self, input: jnp.array, rgb: jnp.array):
        input = input.reshape(400, 400, 1)
        return input * rgb

    def gradient(self):
        x, y = self.xy()
        grad = x * y
        return grad

    def smooth_circle(
        self,
        width=0.1,
        height=0.1,
        center_x=0.5,
        center_y=0.5,
        brightness=1.0,
        color=[1.0, 1.0, 1.0],
    ) -> jnp.ndarray:
        x, y = self.xy()
        img = 1 - (
            (1 / (width ** 2)) * (x - center_x) ** 2
            + (1 / (height ** 2)) * (y - center_y) ** 2
        )
        img = self.apply_brightness(img, brightness)
        img = self.apply_color(img, jnp.array(color))
        return clamp(img)

    def circle(
        self,
        width=0.1,
        height=0.1,
        center_x=0.5,
        center_y=0.5,
        brightness=1.0,
        color=[1.0, 1.0, 1.0],
    ) -> jnp.ndarray:
        x, y = self.xy()
        img = (1 / width) * (x - center_x) ** 2 + (1 / height) * (y - center_y) ** 2
        img = img <= 0.1
        img = self.apply_brightness(img, brightness)
        img = self.apply_color(img, jnp.array(color))
        return clamp(img)

    def smooth_square(
        self,
        width=0.2,
        height=0.2,
        center_x=0.5,
        center_y=0.5,
        brightness=1.0,
        color=[1.0, 1.0, 1.0],
    ) -> jnp.ndarray:
        x = jnp.linspace(0.0, 1.0, self.shape[0])
        y = jnp.reshape(jnp.linspace(0.0, 1.0, self.shape[1]), (self.shape[1], 1))
        img = 1 - (
            (1 / (width ** 2)) * abs(x - center_x)
            + (1 / (height ** 2)) * abs(y - center_y)
        )
        img = self.apply_brightness(img, brightness)
        img = self.apply_color(img, jnp.array(color))
        return img

    def square(
        self,
        width=0.2,
        height=0.2,
        center_x=0.5,
        center_y=0.5,
        brightness=1.0,
        color=[1.0, 1.0, 1.0],
    ):
        x, y = self.xy()
        x = abs(x - center_x) < width * 0.5
        y = abs(y - center_y) < height * 0.5
        img = x * y
        img = self.apply_brightness(img, brightness)
        img = self.apply_color(img, jnp.array(color))
        return clamp(img)

    def wave(
        self, frequency: float, offset: float, brightness=1.0, color=[1.0, 1.0, 1.0]
    ):
        x, y = self.xy()
        img = jnp.sin(
            offset
            + frequency * x * jnp.reshape(jnp.ones(self.y_shape), (self.y_shape, 1))
        )
        img = self.apply_brightness(img, brightness)
        img = self.apply_color(img, jnp.array(color))
        return img

    def scaled_background(self, intensity: float):
        return intensity * jnp.reshape(jnp.ones(self.y_shape), (self.y_shape, 1))
