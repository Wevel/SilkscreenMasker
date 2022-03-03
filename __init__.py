try:
	from .SilkscreenMasker import SilkscreenMaskerPlugin
	SilkscreenMasker = SilkscreenMaskerPlugin()
	SilkscreenMasker.register()
except Exception as e:
	import logging
	root = logging.getLogger()
	root.debug(repr(e))