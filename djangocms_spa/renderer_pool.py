from .cms_plugins import SPAPluginMixin
from .renderer import BaseSPARenderer, MixinPluginRenderer


class RendererPool(object):
    def __init__(self):
        self.renderers = {}

    def register_renderer(self, renderer):
        self._register_renderer(renderer())
    register_renderer.__annotations__ = {'renderer': BaseSPARenderer.__class__}

    def _register_renderer(self, renderer):
        self.renderers[renderer.plugin_class.__name__] = renderer
    _register_renderer.__annotations__ = {'renderer': BaseSPARenderer}

    def register_plugin(self, plugin_class):
        if not issubclass(plugin_class, SPAPluginMixin):
            raise TypeError()

        renderer = MixinPluginRenderer(plugin_class)
        self._register_renderer(renderer)
        return renderer
    register_plugin.__annotations__ = {'plugin_class': 'SPAPluginMixin'}

    def renderer_for_plugin(self, plugin):
        plugin_class = plugin.__class__
        renderer = self.renderers.get(plugin_class.__name__, None)
        if not renderer:
            try:
                renderer = self.register_plugin(plugin_class)
            except TypeError:
                pass

        return renderer
    renderer_for_plugin.__annotations__ = {'return': BaseSPARenderer}

renderer_pool = RendererPool()
