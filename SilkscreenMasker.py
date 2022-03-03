import os
import sys
import time
import tempfile
import logging
import wx
from wx import FileConfig

import pcbnew

from .Window import Dialog

class SilkscreenMaskerPlugin(pcbnew.ActionPlugin, object):
	def __init__(self):
		super(SilkscreenMaskerPlugin, self).__init__()

		self.config_file = os.path.join(os.path.dirname(__file__), "..", "config.ini")
		self.InitLogger()
		self.logger = logging.getLogger(__name__)

		self.name = "Mask Images for Silkscreens"
		self.category = "Modify PCB"
		self.description = "Create masked imaged for use on silkscreens"

		self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
		self.show_toolbar_button = True
		icon_dir = os.path.dirname(__file__)
		self.icon_file_name = os.path.join(icon_dir, "icon.png")
		self.config = FileConfig(localFilename=self.config_file)
        
		self._pcbnew_frame = None

		self.dlg = None

	def Run(self):
		if self._pcbnew_frame is None:
			try:
				self._pcbnew_frame = [x for x in wx.GetTopLevelWindows() if ('pcbnew' in x.GetTitle().lower() and not 'python' in x.GetTitle().lower()) or ('pcb editor' in x.GetTitle().lower())]
				if len(self._pcbnew_frame) == 1:
					self._pcbnew_frame = self._pcbnew_frame[0]
				else:
					self._pcbnew_frame = None
			except:
				pass
		
		def onWindowClose():
			self.dlg = None

		if self.dlg == None:
			self.dlg = Dialog(self._pcbnew_frame, self.config, pcbnew.GetBoard(), onWindowClose)
			self.dlg.Show()
		else:
			self.dlg.Iconize(False)
			self.dlg.Raise()

	def InitLogger(self):
		root = logging.getLogger()
		root.setLevel(logging.DEBUG)

		# Log to stderr
		handler1 = logging.StreamHandler(sys.stderr)
		handler1.setLevel(logging.DEBUG)

		log_path = os.path.dirname(__file__)
		log_file = os.path.join(log_path, "..", "silkscreenMasker.log")

		# and to our error file
		# Check logging file permissions, if fails, move log file to tmp folder
		handler2 = None
		try:
			handler2 = logging.FileHandler(log_file)
		except PermissionError:
			log_path = os.path.join(tempfile.mkdtemp())
			try: # Use try/except here because python 2.7 doesn't support exist_ok
				os.makedirs(log_path)
			except:
				pass

			log_file = os.path.join(log_path, "silkscreenMasker.log")
			handler2 = logging.FileHandler(log_file)

			# Also move config file
			self.config_file = os.path.join(log_path, "config.ini")
			self.config = FileConfig(localFilename=self.config_file)

		handler2.setLevel(logging.DEBUG)
		formatter = logging.Formatter("%(asctime)s %(name)s %(lineno)d:%(message)s", datefmt="%m-%d %H:%M:%S")
		handler1.setFormatter(formatter)
		handler2.setFormatter(formatter)
		root.addHandler(handler1)
		root.addHandler(handler2)
		
