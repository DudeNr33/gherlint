# pylint: disable=too-few-public-methods
"""Modules without ``register_checker`` function must not lead to a crash of ``gherlint``"""


class Dummy:
    pass
