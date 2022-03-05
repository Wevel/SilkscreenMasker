import os

import wx
import pcbnew

from . import dialog_silkscreenMasker
#from . import dialog_maskSaved

class Dialog(dialog_silkscreenMasker.frameSilkscreenMasker):
	def __init__(self, parent, config, board, onWindowClose):
		dialog_silkscreenMasker.frameSilkscreenMasker.__init__(self, parent)
		
		self.config = config
		self.board = board
		self.onWindowClose = onWindowClose

		self.ClearError()

		self.defaultBaseImageSize = 1000
		self.pixelsPerCMX = 100
		self.pixelsPerCMY = 100
		self.currentPath = ""
		self.baseImage = None
		self.maskedImage = None
		self.drawImage = None
		
		self.UpdateLayerChoiceOptions()

		self.loadConfig()
		self.RegenerateMaskedImage()
	
	def CreateDefaultBaseImage(self):
		self.currentPath = ""
		self.baseImage = wx.Bitmap(self.defaultBaseImageSize, self.defaultBaseImageSize)
		imageWidth, imageHeight = self.baseImage.GetSize()

		# Start drawing
		dc = wx.MemoryDC()
		dc.SelectObject(self.baseImage)

		# Set base image colour (will be oposite of mask)
		if self.m_checkBoxNegative.IsChecked():
			dc.SetPen(wx.Pen("#FFFFFF", width=1))
			dc.SetBrush(wx.Brush("#FFFFFF"))
		else:
			dc.SetPen(wx.Pen("#000000", width=1))
			dc.SetBrush(wx.Brush("#000000"))

		dc.DrawRectangle(0, 0, imageWidth, imageHeight)

		# Finish drawing
		dc.SelectObject(wx.NullBitmap)

	def CreateMaskedImage(self):
		if self.baseImage == None:
			self.maskedImage = None
		else:
			imageBaseWidth, imageBaseHeight = self.baseImage.GetSize()
			self.maskedImage = None

			selectionIndex = self.m_choiceMaskLayer.GetCurrentSelection()
			if selectionIndex != wx.NOT_FOUND:
				layerName = self.m_choiceMaskLayer.GetString(selectionIndex)
			else:
				layerName = ""

			layerBounds = None

			drawings = self.board.GetDrawings()
			layerShapes = []
			for shape in drawings:
				if shape.GetLayerName() == layerName:
					layerShapes.append(shape)
					shapeBounds = shape.GetBoundingBox()

					if layerBounds == None:
						layerBounds = pcbnew.EDA_RECT(shapeBounds.GetPosition(), shapeBounds.GetSize())
					else:
						layerBounds.Merge(shapeBounds)
		
			if len(layerShapes) > 0 and layerBounds != None:
				left = pcbnew.ToMM(layerBounds.GetLeft())
				right = pcbnew.ToMM(layerBounds.GetRight())
				top = pcbnew.ToMM(layerBounds.GetTop())
				bottom = pcbnew.ToMM(layerBounds.GetBottom())
				physicalWidth = right - left
				physicalHeight = bottom - top
				physicalAspect = physicalWidth / physicalHeight

				imageCroppedHeight = imageBaseHeight
				imageCroppedWidth = imageCroppedHeight * physicalAspect
				cropTop = False

				if imageCroppedWidth > imageCroppedWidth:
					imageCroppedWidth = imageBaseWidth
					imageCroppedHeight = imageCroppedWidth / physicalAspect
					cropTop = True

				self.pixelsPerCMX = float(imageCroppedWidth) / (physicalWidth / 10)
				self.pixelsPerCMY = float(imageCroppedHeight) / (physicalHeight / 10)
				self.maskedImage = self.baseImage.GetSubBitmap(wx.Rect((imageBaseWidth - imageCroppedWidth) // 2, (imageBaseHeight - imageCroppedHeight) // 2, imageCroppedWidth, imageCroppedHeight))

				flipped = self.m_checkBoxFlip.IsChecked()

				# Start drawing
				dc = wx.MemoryDC()
				dc.SelectObject(self.maskedImage)

				# Set mask colour
				maskColour = "#000000" if self.m_checkBoxNegative.IsChecked() else "#FFFFFF"
				defaultPen = wx.Pen(maskColour, width=1)
				defaultBrush = wx.Brush(maskColour)
				transparentBrush = wx.Brush(maskColour, style=wx.TRANSPARENT)

				dc.SetPen(defaultPen)
				dc.SetBrush(defaultBrush)

				def pointToPixelCoordinates(pos):
					return wx.Point((pcbnew.ToMM(pos.x) - left) * float(imageCroppedWidth) / physicalWidth, (pcbnew.ToMM(pos.y) - top) * float(imageCroppedHeight) / physicalHeight)

				def widthToCoordinates(width):
					if cropTop:
						return pcbnew.ToMM(width) * float(imageCroppedWidth) / physicalWidth
					else:
						return pcbnew.ToMM(width) * float(imageCroppedHeight) / physicalHeight

				for shape in layerShapes:
					shapeType = shape.GetShape()
					if shapeType == pcbnew.S_SEGMENT:
						start = pointToPixelCoordinates(shape.GetStart())
						end = pointToPixelCoordinates(shape.GetEnd())
						width = widthToCoordinates(shape.GetWidth())

						dc.SetPen(wx.Pen(maskColour, width=width))

						dc.DrawLine(start, end)
					elif shapeType == pcbnew.S_RECT:
						start = pointToPixelCoordinates(shape.GetStart())
						end = pointToPixelCoordinates(shape.GetEnd())
						width = widthToCoordinates(shape.GetWidth())
						
						dc.SetPen(wx.Pen(maskColour, width=width))
						dc.SetBrush(defaultBrush if shape.IsFilled() else transparentBrush)

						dc.DrawRectangle(start, wx.Size(end.x - start.x, end.y - start.y))
					elif shapeType == pcbnew.S_ARC:
						start = pointToPixelCoordinates(shape.GetStart())
						center = pointToPixelCoordinates(shape.GetCenter())
						end = pointToPixelCoordinates(shape.GetEnd())
						width = widthToCoordinates(shape.GetWidth())

						dc.SetPen(wx.Pen(maskColour, width=width))
						dc.SetBrush(transparentBrush)

						dc.DrawArc(end, start, center)
					elif shapeType == pcbnew.S_CIRCLE:
						center = pointToPixelCoordinates(shape.GetCenter())
						radius = widthToCoordinates(shape.GetRadius())
						width = widthToCoordinates(shape.GetWidth())

						dc.SetPen(wx.Pen(maskColour, width=width))
						dc.SetBrush(defaultBrush if shape.IsFilled() else transparentBrush)

						dc.DrawCircle(center, radius)
					elif shapeType == pcbnew.S_POLYGON:
						width = widthToCoordinates(shape.GetWidth())

						polys = []
						corners = shape.GetCorners()
						for c in corners:
							polys.append(pointToPixelCoordinates(c))

						dc.SetPen(wx.Pen(maskColour, width=width))
						dc.SetBrush(defaultBrush if shape.IsFilled() else transparentBrush)

						dc.DrawPolygon(polys)
					elif shapeType == pcbnew.S_CURVE:
						self.AddError(f"Unimplemented shape type '{shape.SHAPE_T_asString()}'")
					else:
						self.AddError(f"Unknown shape type '{shape.SHAPE_T_asString()}'")

				# Finish drawing
				dc.SelectObject(wx.NullBitmap)

				if flipped:
					image = self.maskedImage.ConvertToImage()
					image = image.Mirror(horizontally=True)
					self.maskedImage = wx.Bitmap(image)

			else:
				self.pixelsPerCMX = float(imageBaseWidth) / 10
				self.pixelsPerCMY = float(imageBaseHeight) / 10
				self.maskedImage = self.baseImage.GetSubBitmap(wx.Rect(0, 0, imageBaseWidth, imageBaseHeight))

			self.CreateDrawImage()

	def CreateDrawImage(self):
		if self.maskedImage == None:
			self.drawImage = None
		else:
			previewWidth, previewHeight = self.m_panelPreview.GetSize()
			imageWidth, imageHeight = self.maskedImage.GetSize()
			imageAspect = float(imageWidth) / float(imageHeight)

			drawHeight = previewHeight
			drawWidth = drawHeight * imageAspect

			if drawWidth > previewWidth:
				drawWidth = previewWidth
				drawHeight = drawWidth * imageAspect

			image = self.maskedImage.ConvertToImage()
			image = image.Scale(drawWidth, drawHeight, wx.IMAGE_QUALITY_HIGH)
			self.drawImage = wx.Bitmap(image)

	def ClearError(self):
		self.error = None

	def AddError(self, newError):
		if type(newError) is not str:
			newError = str(newError)

		print(newError)
		if self.error == None:
			self.error = newError
		else:
			self.error += f"\n{newError}"

	def SaveMaskedImage(self, savePath):
		if self.maskedImage != None:
			image = self.maskedImage.ConvertToImage()
			image.SetOption(wx.IMAGE_OPTION_RESOLUTIONUNIT, wx.IMAGE_RESOLUTION_CENTIMETRES)
			image.SetOption(wx.IMAGE_OPTION_RESOLUTIONX, self.pixelsPerCMX)
			image.SetOption(wx.IMAGE_OPTION_RESOLUTIONY, self.pixelsPerCMY)
			image.SetOption(wx.IMAGE_OPTION_QUALITY, 100)
			image.SaveFile(savePath, wx.BITMAP_TYPE_JPEG)

	def UpdateLayerChoiceOptions(self):
		self.layers = []

		for i in range(pcbnew.PCBNEW_LAYER_ID_START, pcbnew.PCBNEW_LAYER_ID_START + pcbnew.PCB_LAYER_ID_COUNT):
			layerName = self.board.GetLayerName(i)
			self.layers.append(layerName)
		
		self.m_choiceMaskLayer.Clear()
		self.m_choiceMaskLayer.Append("")
		self.m_choiceMaskLayer.AppendItems(self.layers)

	def ParseFloat(self, inputStr, defaultValue=0.0, valueName="float"):
		value = defaultValue
		if inputStr != "":
			try:
				value = float(inputStr)
			except ValueError:
				self.AddError(f"Invalid {valueName} '{inputStr}'")
		return value

	def loadConfig(self):
		try:
			self.config.SetPath('/')
			self.defaultBaseImageSize = self.config.ReadInt("default-base-image-size", 1000)
			self.m_filePickerBaseImage.SetPath(self.config.Read("last-base-image", ""))
			self.m_choiceMaskLayer.SetStringSelection(self.config.Read("mask-layer", ""))
			self.m_checkBoxNegative.SetValue(self.config.Read("mask-negative", "False") == "True")
			self.m_checkBoxFlip.SetValue(self.config.Read("mask-flip", "False") == "True")

		except:
			import traceback
			self.AddError(traceback.format_exc())
		
	def saveConfig(self):
		try:
			self.config.SetPath('/')
			self.config.WriteInt("default-base-image-size", self.defaultBaseImageSize)
			self.config.Write("last-base-image", self.m_filePickerBaseImage.GetPath())
			self.config.Write("mask-layer", self.m_choiceMaskLayer.GetStringSelection())
			self.config.Write("mask-negative", "True" if self.m_checkBoxNegative.IsChecked() else "False")
			self.config.Write("mask-flip", "True" if self.m_checkBoxFlip.IsChecked() else "False")

			self.config.Flush()
		except:
			import traceback
			self.AddError(traceback.format_exc())
		
	def RePaint(self, e=None):
		self.Layout()
		self.Refresh()
		self.Update()

	def RegenerateMaskedImage(self):
		self.ClearError()

		path = self.m_filePickerBaseImage.GetPath()
		if path != "":
			if os.path.isfile(path):
				try:
					self.currentPath = path
					self.baseImage = wx.Bitmap()
					self.baseImage.LoadFile(path)

					if not(self.baseImage.IsOk()):
						self.CreateDefaultBaseImage()
						self.AddError("Failed to load file")
				except:
					self.CreateDefaultBaseImage()
					import traceback
					self.AddError(traceback.format_exc())
			else:
				self.CreateDefaultBaseImage()
				self.AddError(f"Can't find file '{path}'")
		else:
			self.CreateDefaultBaseImage()

		self.CreateMaskedImage()
		self.RePaint()

	def OnPaintPreview(self, e):
		dc = wx.PaintDC(self.m_panelPreview)
		previewWidth, previewHeight = self.m_panelPreview.GetSize()
			
		if self.baseImage == None:
			if self.m_checkBoxNegative.IsChecked():
				dc.SetPen(wx.Pen("#000000", width=1))
				dc.SetBrush(wx.Brush("#000000"))
			else:
				dc.SetPen(wx.Pen("#FFFFFF", width=1))
				dc.SetBrush(wx.Brush("#FFFFFF"))

			dc.DrawRectangle(0, 0, previewWidth, previewHeight)
		else:
			if self.drawImage == None:
				self.AddError("No draw image, even though a base image is set")
			else:
				imageWidth, imageHeight = self.drawImage.GetSize()
				dc.DrawBitmap(self.drawImage, (previewWidth - imageWidth) // 2, (previewHeight - imageHeight) // 2)

		if self.error is not None:
			font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
			dc.SetFont(font)
			dc.SetTextForeground("#FF0000")

			rect = wx.Rect(0, 0, previewWidth, previewHeight)
			dc.DrawLabel(self.error, rect, wx.ALIGN_LEFT)

	def OnSettingsChanged(self, event):
		self.RegenerateMaskedImage()

	def OnSaveImage(self, event):
		self.RegenerateMaskedImage()
		
		with wx.FileDialog(self, "Save Mask", wildcard=u"JPEG files (*.jpg *.jpeg)|*.jpg;*.jpeg|PNG files (*.png)|*.png|BMP (*.bmp)|*.bmp|Other (*.*)|*.*", style=wx.FD_SAVE) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return     # the user changed their mind

			self.SaveMaskedImage(fileDialog.GetPath())

			#dialog_maskSaved.dialogMaskSaved(self).ShowModal()

	def OnCloseClick(self, event):
		self.saveConfig()
		self.Close()

	def OnClose(self, event):
		self.saveConfig()
		self.currentPath = ""
		self.baseImage = None
		self.onWindowClose()

		event.Skip()
