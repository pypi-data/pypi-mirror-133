import jax.numpy as jnp
from typing import Tuple
from jaxson.utils import clamp


class Canvas:
    def __init__(self, shape: Tuple[int, int, int]):
        self.shape = shape
        self.x_shape = shape[1]
        self.y_shape = shape[2]

    def zeros(self) -> jnp.ndarray:
        return jnp.zeros(())

    def xy(self):
        return (
            jnp.linspace(0.0, 1.0, self.x_shape),
            jnp.reshape(jnp.linspace(0.0, 1.0, self.y_shape), (self.y_shape, 1)),
        )

    def gradient(self):
        x, y = self.xy()
        grad = x * y
        return grad

    def smooth_circle(
        self, width=0.1, height=0.1, center_x=0.5, center_y=0.5
    ) -> jnp.ndarray:
        x, y = self.xy()
        img = 1 - (
            (1 / (width ** 2)) * (x - center_x) ** 2
            + (1 / (height ** 2)) * (y - center_y) ** 2
        )
        # img = jnp.reshape(img, self.shape)
        return clamp(img)

    def circle(
        self, width=0.1, height=0.1, center_x=0.5, center_y=0.5, brightness=1.0
    ) -> jnp.ndarray:
        x, y = self.xy()
        img = (1 / width) * (x - center_x) ** 2 + (1 / height) * (y - center_y) ** 2
        img = img <= 0.1
        img = img * brightness
        return clamp(img)

    def square(self, width=0.2, height=0.2, center_x=0.5, center_y=0.5) -> jnp.ndarray:
        x = jnp.linspace(0.0, 1.0, self.shape[0])
        y = jnp.reshape(jnp.linspace(0.0, 1.0, self.shape[1]), (self.shape[1], 1))
        img = 1 - (
            (1 / (width ** 2)) * abs(x - center_x)
            + (1 / (height ** 2)) * abs(y - center_y)
        )
        return img

    def wave(self, frequency: float, offset: float):
        x, y = self.xy()
        img = jnp.sin(
            offset
            + frequency * x * jnp.reshape(jnp.ones(self.y_shape), (self.y_shape, 1))
        )
        return img

    def scaled_background(self, intensity: float):
        return intensity * jnp.reshape(jnp.ones(self.y_shape), (self.y_shape, 1))
