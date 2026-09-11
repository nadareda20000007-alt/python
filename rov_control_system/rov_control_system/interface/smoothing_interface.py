from zope.interface import Interface, Attribute


class SmoothingFunction(Interface):
    """
    Contract every smoothing function must satisfy.
    Any function matching this signature can be registered in SMOOTHING_FUNCTIONS
    in smoothing.py — no inheritance required.
    """

    def __call__(self, current: float, target: float, **kwargs) -> float:
        ...
