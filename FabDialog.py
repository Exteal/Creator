# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class HierarchyFrame
###########################################################################

class HierarchyFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Hierarchy creator", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainBox = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		groupBoxPcbGeneral = wx.FlexGridSizer( 0, 3, 0, 0 )
		groupBoxPcbGeneral.SetFlexibleDirection( wx.BOTH )
		groupBoxPcbGeneral.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.labelCardNumber = wx.StaticText( self, wx.ID_ANY, u"Card number :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCardNumber.Wrap( -1 )

		groupBoxPcbGeneral.Add( self.labelCardNumber, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelCardName = wx.StaticText( self, wx.ID_ANY, u"Card name :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCardName.Wrap( -1 )

		groupBoxPcbGeneral.Add( self.labelCardName, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelProjectName = wx.StaticText( self, wx.ID_ANY, u"Project name :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelProjectName.Wrap( -1 )

		groupBoxPcbGeneral.Add( self.labelProjectName, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.lineEditCardNumber = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditCardNumber.SetMaxLength( 20 )
		groupBoxPcbGeneral.Add( self.lineEditCardNumber, 0, wx.ALL, 5 )

		self.lineEditCardName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		groupBoxPcbGeneral.Add( self.lineEditCardName, 0, wx.ALL, 5 )

		self.lineEditProjectName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		groupBoxPcbGeneral.Add( self.lineEditProjectName, 0, wx.ALL, 5 )

		self.labelClaimer = wx.StaticText( self, wx.ID_ANY, u"Claimer :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelClaimer.Wrap( -1 )

		groupBoxPcbGeneral.Add( self.labelClaimer, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelRouter = wx.StaticText( self, wx.ID_ANY, u"Router :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelRouter.Wrap( -1 )

		groupBoxPcbGeneral.Add( self.labelRouter, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelCreation = wx.StaticText( self, wx.ID_ANY, u"Creation date :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCreation.Wrap( -1 )

		groupBoxPcbGeneral.Add( self.labelCreation, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.lineEditClaimer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		groupBoxPcbGeneral.Add( self.lineEditClaimer, 0, wx.ALL, 5 )

		self.lineEditRouter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		groupBoxPcbGeneral.Add( self.lineEditRouter, 0, wx.ALL, 5 )

		self.editDateCreation = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT|wx.adv.DP_DROPDOWN )
		groupBoxPcbGeneral.Add( self.editDateCreation, 0, wx.ALL, 5 )


		bSizer6.Add( groupBoxPcbGeneral, 0, wx.EXPAND, 1 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer181 = wx.BoxSizer( wx.VERTICAL )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.pushButtonAutoPcbNumber = wx.Button( self, wx.ID_ANY, u"Auto Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.pushButtonAutoPcbNumber, 0, wx.ALL, 5 )


		bSizer20.Add( ( 70, 0), 0, 0, 5 )

		self.checkBoxExistingpcb = wx.CheckBox( self, wx.ID_ANY, u"Archived PCB", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.checkBoxExistingpcb, 0, wx.ALL, 5 )


		bSizer20.Add( ( 40, 0), 1, wx.EXPAND, 5 )

		self.pushButtonLoadFromFile = wx.Button( self, wx.ID_ANY, u"Load from file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.pushButtonLoadFromFile, 0, wx.ALL, 5 )


		bSizer181.Add( bSizer20, 1, wx.EXPAND, 5 )

		comboBoxExistingPcbChoices = []
		self.comboBoxExistingPcb = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBoxExistingPcbChoices, wx.CB_READONLY )
		self.comboBoxExistingPcb.Enable( False )

		bSizer181.Add( self.comboBoxExistingPcb, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer7.Add( bSizer181, 1, wx.EXPAND, 5 )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		self.pushButtonLoadPcb = wx.Button( self, wx.ID_ANY, u"Load PCB", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pushButtonLoadPcb.Enable( False )

		bSizer19.Add( self.pushButtonLoadPcb, 1, wx.ALL|wx.EXPAND, 5 )

		self.pushButtonPcbVersionning = wx.Button( self, wx.ID_ANY, u"PCB Versionning", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pushButtonPcbVersionning.Enable( False )

		bSizer19.Add( self.pushButtonPcbVersionning, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer7.Add( bSizer19, 1, wx.EXPAND, 5 )


		bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )


		mainBox.Add( bSizer6, 0, wx.EXPAND, 5 )

		groupBoxPcb = wx.BoxSizer( wx.HORIZONTAL )

		groupBoxPcbClassChoice = wx.FlexGridSizer( 2, 2, 0, 0 )
		groupBoxPcbClassChoice.SetFlexibleDirection( wx.BOTH )
		groupBoxPcbClassChoice.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.labelClassNumber = wx.StaticText( self, wx.ID_ANY, u"Class number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelClassNumber.Wrap( -1 )

		gSizer2.Add( self.labelClassNumber, 0, wx.ALL, 5 )

		self.labelClassDrill = wx.StaticText( self, wx.ID_ANY, u"Class drill", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelClassDrill.Wrap( -1 )

		gSizer2.Add( self.labelClassDrill, 0, wx.ALL, 5 )

		comboBoxClassNumberChoices = [ u"3", u"4", u"5", u"6", u"7", u"8", u"9" ]
		self.comboBoxClassNumber = wx.ComboBox( self, wx.ID_ANY, u"9", wx.DefaultPosition, wx.DefaultSize, comboBoxClassNumberChoices, wx.CB_READONLY )
		self.comboBoxClassNumber.SetSelection( 6 )
		gSizer2.Add( self.comboBoxClassNumber, 0, wx.ALL, 5 )

		comboBoxClassDrillChoices = [ u"A", u"B", u"C", u"D", u"E" ]
		self.comboBoxClassDrill = wx.ComboBox( self, wx.ID_ANY, u"D", wx.DefaultPosition, wx.DefaultSize, comboBoxClassDrillChoices, wx.CB_READONLY )
		self.comboBoxClassDrill.SetSelection( 3 )
		gSizer2.Add( self.comboBoxClassDrill, 0, wx.ALL, 5 )


		groupBoxPcbClassChoice.Add( gSizer2, 1, wx.EXPAND, 5 )


		groupBoxPcb.Add( groupBoxPcbClassChoice, 0, wx.EXPAND, 5 )

		groupBoxPcbInfoResult = wx.BoxSizer( wx.VERTICAL )

		gSizer1 = wx.GridSizer( 2, 5, 0, 0 )

		self.labelTrackWidth = wx.StaticText( self, wx.ID_ANY, u"Track width", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelTrackWidth.Wrap( -1 )

		gSizer1.Add( self.labelTrackWidth, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelTracktoTrackSpace = wx.StaticText( self, wx.ID_ANY, u"Track to track space", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelTracktoTrackSpace.Wrap( -1 )

		gSizer1.Add( self.labelTracktoTrackSpace, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelViaDrillDiameter = wx.StaticText( self, wx.ID_ANY, u"Via drill diameter", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelViaDrillDiameter.Wrap( -1 )

		gSizer1.Add( self.labelViaDrillDiameter, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelViaDiameter = wx.StaticText( self, wx.ID_ANY, u"Via diameter", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelViaDiameter.Wrap( -1 )

		gSizer1.Add( self.labelViaDiameter, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelHoleToHole = wx.StaticText( self, wx.ID_ANY, u"Hole to hole", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelHoleToHole.Wrap( -1 )

		gSizer1.Add( self.labelHoleToHole, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.lineEditTrackWidth = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.lineEditTrackWidth.Enable( False )
		self.lineEditTrackWidth.SetToolTip( u"unit : mm" )

		gSizer1.Add( self.lineEditTrackWidth, 0, wx.ALL, 5 )

		self.lineEditTrackToTrackSpace = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditTrackToTrackSpace.Enable( False )
		self.lineEditTrackToTrackSpace.SetToolTip( u"unit : mm" )

		gSizer1.Add( self.lineEditTrackToTrackSpace, 0, wx.ALL, 5 )

		self.lineEditViaDrillDiameter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditViaDrillDiameter.Enable( False )
		self.lineEditViaDrillDiameter.SetToolTip( u"unit : mm" )

		gSizer1.Add( self.lineEditViaDrillDiameter, 0, wx.ALL, 5 )

		self.lineEditViaDiameter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditViaDiameter.Enable( False )
		self.lineEditViaDiameter.SetToolTip( u"unit : mm" )

		gSizer1.Add( self.lineEditViaDiameter, 0, wx.ALL, 5 )

		self.lineEditHoleToHole = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditHoleToHole.Enable( False )
		self.lineEditHoleToHole.SetToolTip( u"unit : mm" )

		gSizer1.Add( self.lineEditHoleToHole, 0, wx.ALL, 5 )


		groupBoxPcbInfoResult.Add( gSizer1, 1, wx.EXPAND, 5 )


		groupBoxPcb.Add( groupBoxPcbInfoResult, 1, wx.EXPAND, 5 )


		mainBox.Add( groupBoxPcb, 0, wx.EXPAND, 0 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )

		self.checkBoxCustomPcb = wx.CheckBox( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Custom", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer4.Add( self.checkBoxCustomPcb, 0, wx.ALL, 5 )


		bSizer8.Add( sbSizer4, 0, wx.ALL, 5 )


		mainBox.Add( bSizer8, 0, wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.checkBoxCadence = wx.CheckBox( self, wx.ID_ANY, u"Cadence", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.checkBoxCadence, 0, wx.ALL, 5 )

		self.checkBoxAllowBuriedVia = wx.CheckBox( self, wx.ID_ANY, u"Sub Via", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.checkBoxAllowBuriedVia, 0, wx.ALL, 5 )

		self.checkBoxAllowMicroVia = wx.CheckBox( self, wx.ID_ANY, u"Micro Via", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.checkBoxAllowMicroVia, 0, wx.ALL, 5 )

		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer25 = wx.BoxSizer( wx.VERTICAL )

		self.labelUViaDiameter = wx.StaticText( self, wx.ID_ANY, u"Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelUViaDiameter.Wrap( -1 )

		self.labelUViaDiameter.Hide()

		bSizer25.Add( self.labelUViaDiameter, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		self.lineEditUViaDiameter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditUViaDiameter.Hide()
		self.lineEditUViaDiameter.SetToolTip( u"unit : mm" )
		self.lineEditUViaDiameter.SetMaxSize( wx.Size( 80,-1 ) )

		bSizer25.Add( self.lineEditUViaDiameter, 0, wx.ALL, 5 )


		bSizer24.Add( bSizer25, 0, 0, 5 )

		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.labelUViaDrillDiameter = wx.StaticText( self, wx.ID_ANY, u"Drill diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelUViaDrillDiameter.Wrap( -1 )

		self.labelUViaDrillDiameter.Hide()

		bSizer27.Add( self.labelUViaDrillDiameter, 0, wx.ALL, 5 )

		self.lineEditUViaDrillDiameter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditUViaDrillDiameter.Hide()
		self.lineEditUViaDrillDiameter.SetToolTip( u"unit : mm" )
		self.lineEditUViaDrillDiameter.SetMaxSize( wx.Size( 80,-1 ) )

		bSizer27.Add( self.lineEditUViaDrillDiameter, 0, wx.ALL, 5 )


		bSizer24.Add( bSizer27, 0, 0, 5 )


		bSizer14.Add( bSizer24, 0, 0, 5 )


		bSizer15.Add( bSizer14, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer15.Add( ( 75, 0), 0, 0, 5 )

		bSizer17 = wx.BoxSizer( wx.VERTICAL )

		self.labelLayers = wx.StaticText( self, wx.ID_ANY, u"Layers :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelLayers.Wrap( -1 )

		bSizer17.Add( self.labelLayers, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		comboBoxLayersChoices = [ u"2", u"4", u"6", u"8", u"10", u"12", u"14", u"16", u"18", u"20", u"22", u"24", u"26", u"28", u"30", u"32" ]
		self.comboBoxLayers = wx.ComboBox( self, wx.ID_ANY, u"14", wx.DefaultPosition, wx.DefaultSize, comboBoxLayersChoices, wx.CB_READONLY )
		self.comboBoxLayers.SetSelection( 0 )
		bSizer17.Add( self.comboBoxLayers, 0, wx.ALL, 5 )


		bSizer15.Add( bSizer17, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

		bSizer18 = wx.BoxSizer( wx.VERTICAL )

		self.labelThickness = wx.StaticText( self, wx.ID_ANY, u"Thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelThickness.Wrap( -1 )

		bSizer18.Add( self.labelThickness, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.lineEditThickness = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditThickness.SetToolTip( u"unit : mm" )

		bSizer18.Add( self.lineEditThickness, 0, wx.ALL, 5 )


		bSizer15.Add( bSizer18, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer28 = wx.BoxSizer( wx.VERTICAL )

		self.labelCopperInnerThickness = wx.StaticText( self, wx.ID_ANY, u"Copper inner thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCopperInnerThickness.Wrap( -1 )

		bSizer28.Add( self.labelCopperInnerThickness, 0, wx.ALL, 5 )

		self.lineEditCopperInnerThickness = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditCopperInnerThickness.SetToolTip( u"unit : um" )

		bSizer28.Add( self.lineEditCopperInnerThickness, 0, wx.EXPAND|wx.ALL, 5 )


		bSizer15.Add( bSizer28, 0, wx.ALIGN_CENTER, 5 )

		bSizer281 = wx.BoxSizer( wx.VERTICAL )

		self.labelCopperOuterThickness = wx.StaticText( self, wx.ID_ANY, u"Copper outer  thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCopperOuterThickness.Wrap( -1 )

		bSizer281.Add( self.labelCopperOuterThickness, 0, wx.ALL, 5 )

		self.lineEditCopperOuterThickness = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lineEditCopperOuterThickness.SetToolTip( u"unit : um" )

		bSizer281.Add( self.lineEditCopperOuterThickness, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer15.Add( bSizer281, 0, wx.ALIGN_CENTER, 5 )


		bSizer13.Add( bSizer15, 1, wx.EXPAND, 5 )


		mainBox.Add( bSizer13, 0, wx.EXPAND, 5 )

		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		groupBoxPcbInfoResult1 = wx.BoxSizer( wx.VERTICAL )

		gSizer11 = wx.GridSizer( 2, 4, 0, 0 )

		self.labelFinish = wx.StaticText( self, wx.ID_ANY, u"Finish", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelFinish.Wrap( -1 )

		gSizer11.Add( self.labelFinish, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelSolderMask = wx.StaticText( self, wx.ID_ANY, u"Solder mask", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelSolderMask.Wrap( -1 )

		gSizer11.Add( self.labelSolderMask, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelSilkscreen = wx.StaticText( self, wx.ID_ANY, u"Silkscreen", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelSilkscreen.Wrap( -1 )

		gSizer11.Add( self.labelSilkscreen, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.labelElectricalTest = wx.StaticText( self, wx.ID_ANY, u"Electrical test", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.labelElectricalTest.Wrap( -1 )

		gSizer11.Add( self.labelElectricalTest, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		comboBoxFinishChoices = [ u"Not specified", u"ENIG", u"ENEPIG", u"HAL SnPb", u"HAL lead-free", u"Hard gold", u"Immersion tin", u"Immersion nickel", u"Immersion gold", u"Immersion silver", u"HT_OSP", u"OSP", u"None" ]
		self.comboBoxFinish = wx.ComboBox( self, wx.ID_ANY, u"Not specified", wx.DefaultPosition, wx.DefaultSize, comboBoxFinishChoices, wx.CB_READONLY )
		self.comboBoxFinish.SetSelection( 0 )
		gSizer11.Add( self.comboBoxFinish, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		comboBoxSolderMaskChoices = [ u"Top", u"Bottom", u"Both", u"None" ]
		self.comboBoxSolderMask = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBoxSolderMaskChoices, wx.CB_READONLY )
		gSizer11.Add( self.comboBoxSolderMask, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		comboBoxSilkscreenChoices = [ u"Top", u"Bottom", u"Both", u"None" ]
		self.comboBoxSilkscreen = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBoxSilkscreenChoices, wx.CB_READONLY )
		gSizer11.Add( self.comboBoxSilkscreen, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		comboBoxElectricalTestChoices = [ u"Yes", u"No" ]
		self.comboBoxElectricalTest = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBoxElectricalTestChoices, wx.CB_READONLY )
		gSizer11.Add( self.comboBoxElectricalTest, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		groupBoxPcbInfoResult1.Add( gSizer11, 0, wx.EXPAND|wx.TOP, 5 )


		bSizer30.Add( groupBoxPcbInfoResult1, 1, wx.EXPAND, 5 )


		mainBox.Add( bSizer30, 1, wx.EXPAND, 5 )


		mainBox.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.labelArchivePath = wx.StaticText( self, wx.ID_ANY, u"Path selected :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelArchivePath.Wrap( -1 )

		bSizer10.Add( self.labelArchivePath, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.lineEditHierarchyPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.lineEditHierarchyPath, 0, wx.ALL, 5 )

		self.pushButtonHierarchyPath = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.pushButtonHierarchyPath.SetBitmap( wx.Bitmap( u"C:\\Users\\rh270862\\Downloads\\3994350_click_cursor_mouse_pointer_select_icon (1).png", wx.BITMAP_TYPE_ANY ) )
		bSizer35.Add( self.pushButtonHierarchyPath, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( bSizer35, 1, wx.EXPAND, 5 )


		bSizer9.Add( bSizer10, 0, 0, 5 )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.labelCommentary = wx.StaticText( self, wx.ID_ANY, u"Commentary :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCommentary.Wrap( -1 )

		bSizer11.Add( self.labelCommentary, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.lineEditCommentary = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.lineEditCommentary, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer9.Add( bSizer11, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.progressBarValidation = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.progressBarValidation.SetValue( 0 )
		self.progressBarValidation.Enable( False )
		self.progressBarValidation.Hide()

		bSizer12.Add( self.progressBarValidation, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.buttonValidation = wx.Button( self, wx.ID_ANY, u"Generation", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.buttonValidation, 1, wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )


		bSizer9.Add( bSizer12, 0, wx.EXPAND, 5 )


		mainBox.Add( bSizer9, 0, wx.EXPAND, 5 )


		self.SetSizer( mainBox )
		self.Layout()
		mainBox.Fit( self )
		self.navBar = wx.MenuBar( 0 )
		self.navMenuNav = wx.Menu()
		self.navItemHome = wx.MenuItem( self.navMenuNav, wx.ID_ANY, u"Home", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuNav.Append( self.navItemHome )

		self.navItemArchiver = wx.MenuItem( self.navMenuNav, wx.ID_ANY, u"Archive PCB", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuNav.Append( self.navItemArchiver )

		self.navBar.Append( self.navMenuNav, u"Nav" )

		self.navMenuHelp = wx.Menu()
		self.navItemHelp = wx.MenuItem( self.navMenuHelp, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuHelp.Append( self.navItemHelp )

		self.navItemAbout = wx.MenuItem( self.navMenuHelp, wx.ID_ANY, u"About ", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuHelp.Append( self.navItemAbout )

		self.navBar.Append( self.navMenuHelp, u"Help" )

		self.SetMenuBar( self.navBar )


		self.Centre( wx.BOTH )

		# Connect Events
		self.lineEditCardNumber.Bind( wx.EVT_CHAR, self.capitalize_letters )
		self.pushButtonAutoPcbNumber.Bind( wx.EVT_BUTTON, self.AutoPcbNumber )
		self.checkBoxExistingpcb.Bind( wx.EVT_CHECKBOX, self.ExistingPcb )
		self.pushButtonLoadFromFile.Bind( wx.EVT_BUTTON, self.load_from_file )
		self.pushButtonLoadPcb.Bind( wx.EVT_BUTTON, self.LoadPcb )
		self.pushButtonPcbVersionning.Bind( wx.EVT_BUTTON, self.PcbVersionning )
		self.comboBoxClassNumber.Bind( wx.EVT_COMBOBOX, self.selectClassNumber )
		self.comboBoxClassDrill.Bind( wx.EVT_COMBOBOX, self.selectDrill )
		self.lineEditTrackWidth.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditTrackToTrackSpace.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditViaDrillDiameter.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditViaDiameter.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditHoleToHole.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.checkBoxCustomPcb.Bind( wx.EVT_CHECKBOX, self.toggleCustomKicadProData )
		self.checkBoxAllowMicroVia.Bind( wx.EVT_CHECKBOX, self.toggle_micro_via )
		self.lineEditUViaDiameter.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditUViaDrillDiameter.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditThickness.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditCopperInnerThickness.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditCopperOuterThickness.Bind( wx.EVT_CHAR, self.block_non_numbers )
		self.lineEditHierarchyPath.Bind( wx.EVT_CHAR, self.char )
		self.pushButtonHierarchyPath.Bind( wx.EVT_BUTTON, self.dir_picker_hierarchy )
		self.buttonValidation.Bind( wx.EVT_BUTTON, self.generate_hierarchy )
		self.Bind( wx.EVT_MENU, self.nav_home, id = self.navItemHome.GetId() )
		self.Bind( wx.EVT_MENU, self.nav_archiver, id = self.navItemArchiver.GetId() )
		self.Bind( wx.EVT_MENU, self.display_help, id = self.navItemHelp.GetId() )
		self.Bind( wx.EVT_MENU, self.display_about, id = self.navItemAbout.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def capitalize_letters( self, event ):
		event.Skip()

	def AutoPcbNumber( self, event ):
		event.Skip()

	def ExistingPcb( self, event ):
		event.Skip()

	def load_from_file( self, event ):
		event.Skip()

	def LoadPcb( self, event ):
		event.Skip()

	def PcbVersionning( self, event ):
		event.Skip()

	def selectClassNumber( self, event ):
		event.Skip()

	def selectDrill( self, event ):
		event.Skip()

	def block_non_numbers( self, event ):
		event.Skip()





	def toggleCustomKicadProData( self, event ):
		event.Skip()

	def toggle_micro_via( self, event ):
		event.Skip()






	def char( self, event ):
		event.Skip()

	def dir_picker_hierarchy( self, event ):
		event.Skip()

	def generate_hierarchy( self, event ):
		event.Skip()

	def nav_home( self, event ):
		event.Skip()

	def nav_archiver( self, event ):
		event.Skip()

	def display_help( self, event ):
		event.Skip()

	def display_about( self, event ):
		event.Skip()


###########################################################################
## Class ArchiveFrame
###########################################################################

class ArchiveFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Archiver", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer27 = wx.BoxSizer( wx.VERTICAL )


		bSizer27.Add( ( 0, 0), 2, 0, 5 )

		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

		self.labelArchiverPath = wx.StaticText( self, wx.ID_ANY, u"Path selected : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelArchiverPath.Wrap( -1 )

		bSizer30.Add( self.labelArchiverPath, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )

		self.lineEditArchiverPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer30.Add( self.lineEditArchiverPath, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )

		self.m_bpButton2 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton2.SetBitmap( wx.Bitmap( u"C:\\Users\\rh270862\\Downloads\\3994350_click_cursor_mouse_pointer_select_icon (1).png", wx.BITMAP_TYPE_ANY ) )
		bSizer30.Add( self.m_bpButton2, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer32 = wx.BoxSizer( wx.VERTICAL )

		self.pushButtonArchivePcb = wx.Button( self, wx.ID_ANY, u"Archive PCB", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer32.Add( self.pushButtonArchivePcb, 1, wx.ALL|wx.EXPAND, 5 )

		self.progressBarArchive = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.progressBarArchive.SetValue( 0 )
		self.progressBarArchive.Enable( False )
		self.progressBarArchive.Hide()

		bSizer32.Add( self.progressBarArchive, 1, wx.ALL, 5 )


		bSizer30.Add( bSizer32, 1, wx.EXPAND, 5 )


		bSizer27.Add( bSizer30, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer27 )
		self.Layout()
		self.navBar = wx.MenuBar( 0 )
		self.navMenuNav = wx.Menu()
		self.navItemHome = wx.MenuItem( self.navMenuNav, wx.ID_ANY, u"Home", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuNav.Append( self.navItemHome )

		self.navItemHierarchy = wx.MenuItem( self.navMenuNav, wx.ID_ANY, u"Generate hierarchy", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuNav.Append( self.navItemHierarchy )

		self.navBar.Append( self.navMenuNav, u"Nav" )

		self.navMenuHelp = wx.Menu()
		self.navItemHelp = wx.MenuItem( self.navMenuHelp, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuHelp.Append( self.navItemHelp )

		self.navItemAbout = wx.MenuItem( self.navMenuHelp, wx.ID_ANY, u"About ", wx.EmptyString, wx.ITEM_NORMAL )
		self.navMenuHelp.Append( self.navItemAbout )

		self.navBar.Append( self.navMenuHelp, u"Help" )

		self.SetMenuBar( self.navBar )


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_bpButton2.Bind( wx.EVT_BUTTON, self.dir_picker_path_archiver )
		self.pushButtonArchivePcb.Bind( wx.EVT_BUTTON, self.archive_pcb )
		self.Bind( wx.EVT_MENU, self.nav_home, id = self.navItemHome.GetId() )
		self.Bind( wx.EVT_MENU, self.nav_hierarchy, id = self.navItemHierarchy.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def dir_picker_path_archiver( self, event ):
		event.Skip()

	def archive_pcb( self, event ):
		event.Skip()

	def nav_home( self, event ):
		event.Skip()

	def nav_hierarchy( self, event ):
		event.Skip()


###########################################################################
## Class HomeFrame
###########################################################################

class HomeFrame ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Home", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( 300,100 ), wx.DefaultSize )

		bSizer32 = wx.BoxSizer( wx.VERTICAL )

		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Fast Generation Plugin", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )

		bSizer33.Add( self.m_staticText25, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


		bSizer32.Add( bSizer33, 1, wx.EXPAND, 5 )

		bSizer34 = wx.BoxSizer( wx.HORIZONTAL )

		self.pushButtonHomeCreateHierarchy = wx.Button( self, wx.ID_ANY, u"Create hierarchy", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer34.Add( self.pushButtonHomeCreateHierarchy, 0, wx.ALL, 5 )


		bSizer34.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.pushButtonHomeArchivePcb = wx.Button( self, wx.ID_ANY, u"Archive PCB", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer34.Add( self.pushButtonHomeArchivePcb, 0, wx.ALL, 5 )


		bSizer32.Add( bSizer34, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer32 )
		self.Layout()
		bSizer32.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.pushButtonHomeCreateHierarchy.Bind( wx.EVT_BUTTON, self.nav_hierarchy )
		self.pushButtonHomeArchivePcb.Bind( wx.EVT_BUTTON, self.nav_archiver )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def nav_hierarchy( self, event ):
		event.Skip()

	def nav_archiver( self, event ):
		event.Skip()


