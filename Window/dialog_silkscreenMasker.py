# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frameSilkscreenMasker
###########################################################################

class frameSilkscreenMasker ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Silkscreen Mask Creator", pos = wx.DefaultPosition, size = wx.Size( 370,623 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		fgSizerBase = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizerBase.SetFlexibleDirection( wx.BOTH )
		fgSizerBase.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textPreview = wx.StaticText( self, wx.ID_ANY, u"Preview", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textPreview.Wrap( -1 )

		fgSizerBase.Add( self.m_textPreview, 0, wx.ALL, 5 )

		self.m_panelPreview = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 350,350 ), wx.TAB_TRAVERSAL )
		fgSizerBase.Add( self.m_panelPreview, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticlineSettings = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.LI_HORIZONTAL )
		fgSizerBase.Add( self.m_staticlineSettings, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_textSettings = wx.StaticText( self, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSettings.Wrap( -1 )

		fgSizerBase.Add( self.m_textSettings, 0, wx.ALL, 5 )

		fgSizerSettings = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizerSettings.SetFlexibleDirection( wx.BOTH )
		fgSizerSettings.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		fgSizerSettings.Add( ( 20, 0), 1, wx.EXPAND, 5 )

		self.m_staticTextFileName = wx.StaticText( self, wx.ID_ANY, u"Base Image:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextFileName.Wrap( -1 )

		fgSizerSettings.Add( self.m_staticTextFileName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_filePickerBaseImage = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"JPEG files (*.jpg *.jpeg)|*.jpg;*.jpeg|PNG files (*.png)|*.png|BMP (*.bmp)|*.bmp|Other (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		fgSizerSettings.Add( self.m_filePickerBaseImage, 0, wx.ALL, 5 )


		fgSizerSettings.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticTextBack = wx.StaticText( self, wx.ID_ANY, u"Mask Layer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBack.Wrap( -1 )

		fgSizerSettings.Add( self.m_staticTextBack, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		m_choiceMaskLayerChoices = []
		self.m_choiceMaskLayer = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceMaskLayerChoices, 0 )
		self.m_choiceMaskLayer.SetSelection( 0 )
		fgSizerSettings.Add( self.m_choiceMaskLayer, 0, wx.ALL, 5 )


		fgSizerSettings.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticTextNegative = wx.StaticText( self, wx.ID_ANY, u"Nagative Mask:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextNegative.Wrap( -1 )

		fgSizerSettings.Add( self.m_staticTextNegative, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_checkBoxNegative = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerSettings.Add( self.m_checkBoxNegative, 0, wx.ALL, 5 )


		fgSizerSettings.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticTextFlip = wx.StaticText( self, wx.ID_ANY, u"Flip Mask", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextFlip.Wrap( -1 )

		fgSizerSettings.Add( self.m_staticTextFlip, 0, wx.ALL, 5 )

		self.m_checkBoxFlip = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerSettings.Add( self.m_checkBoxFlip, 0, wx.ALL, 5 )


		fgSizerBase.Add( fgSizerSettings, 1, wx.EXPAND, 5 )

		self.m_staticlineButtons = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizerBase.Add( self.m_staticlineButtons, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizerButtons = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizerButtons.SetFlexibleDirection( wx.BOTH )
		fgSizerButtons.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonSaveImage = wx.Button( self, wx.ID_ANY, u"Save Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerButtons.Add( self.m_buttonSaveImage, 0, wx.ALL, 5 )

		self.m_buttonClose = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerButtons.Add( self.m_buttonClose, 0, wx.ALL, 5 )


		fgSizerBase.Add( fgSizerButtons, 1, wx.ALIGN_RIGHT|wx.EXPAND, 5 )


		self.SetSizer( fgSizerBase )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.m_panelPreview.Bind( wx.EVT_PAINT, self.OnPaintPreview )
		self.m_filePickerBaseImage.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnSettingsChanged )
		self.m_choiceMaskLayer.Bind( wx.EVT_CHOICE, self.OnSettingsChanged )
		self.m_checkBoxNegative.Bind( wx.EVT_CHECKBOX, self.OnSettingsChanged )
		self.m_checkBoxFlip.Bind( wx.EVT_CHECKBOX, self.OnSettingsChanged )
		self.m_buttonSaveImage.Bind( wx.EVT_BUTTON, self.OnSaveImage )
		self.m_buttonClose.Bind( wx.EVT_BUTTON, self.OnCloseClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def OnPaintPreview( self, event ):
		event.Skip()

	def OnSettingsChanged( self, event ):
		event.Skip()




	def OnSaveImage( self, event ):
		event.Skip()

	def OnCloseClick( self, event ):
		event.Skip()


