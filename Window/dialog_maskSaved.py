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
## Class dialogMaskSaved
###########################################################################

class dialogMaskSaved ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Silkscreen Mask Creator", pos = wx.DefaultPosition, size = wx.Size( 200,128 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer7 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )

		self.m_staticTextSaved = wx.StaticText( self, wx.ID_ANY, u"\nMask Saved", wx.DefaultPosition, wx.Size( 180,45 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticTextSaved.Wrap( -1 )

		fgSizer7.Add( self.m_staticTextSaved, 0, wx.ALL, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		m_sdbSizer2.Realize()

		fgSizer7.Add( m_sdbSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL, 10 )


		self.SetSizer( fgSizer7 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


