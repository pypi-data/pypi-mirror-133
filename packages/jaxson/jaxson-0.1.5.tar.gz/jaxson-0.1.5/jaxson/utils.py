import jax.numpy as jnp


def clamp(array: jnp.ndarray) -> jnp.ndarray:
    array = jnp.maximum(array, jnp.zeros(array.shape))
    array = jnp.minimum(array, jnp.ones(array.shape))
    return array
