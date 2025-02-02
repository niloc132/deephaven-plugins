from __future__ import annotations
import logging
from typing import Callable, Optional
from .Element import Element, PropsType
from .._internal import RenderContext, get_context, set_context, NoContextException

logger = logging.getLogger(__name__)


class FunctionElement(Element):
    def __init__(self, name: str, render: Callable[[], list[Element]]):
        """
        Create an element that takes a function to render.

        Args:
            name: Name of the component. Typically, the module joined with the name of the function.
            render: The render function to call when the component needs to be rendered.
        """
        self._name = name
        self._render = render

    @property
    def name(self):
        return self._name

    def render(self, context: RenderContext) -> PropsType:
        """
        Render the component. Should only be called when actually rendering the component, e.g. exporting it to the client.

        Args:
            context: Context to render the component in

        Returns:
            The props of this element.
        """
        old_context: Optional[RenderContext] = None
        try:
            old_context = get_context()
        except NoContextException:
            pass
        logger.debug("old context is %s and new context is %s", old_context, context)

        set_context(context)

        with context:
            children = self._render()

        logger.debug("Resetting to old context %s", old_context)
        set_context(old_context)

        return {"children": children}
