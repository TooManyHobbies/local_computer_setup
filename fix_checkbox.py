# Macro to fix checkbox sheet reference when a sheet is duplicated.
# To use this macro, copy the file to /usr/lib/libreoffice/share/Scripts/python

import uno

def checkboxBindCurrentSheet ( ):


	# get the uno component context from the PyUNO runtime
#	localContext = uno.getComponentContext()

	# create the UnoUrlResolver
#	resolver = localContext.ServiceManager.createInstanceWithContext(
#					"com.sun.star.bridge.UnoUrlResolver", localContext )

	# connect to the running office
#	ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
#	smgr = ctx.ServiceManager

	# get the central desktop object
#	desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
	# The lines above were used when developing this macro to get a desktop object.  When run
	# inside LibreOffice as a macro, the line below replaced them.
	desktop = XSCRIPTCONTEXT.getDesktop()


	# access the current writer document
	model = desktop.getCurrentComponent()


	# access the active sheet
	active_sheet = model.CurrentController.ActiveSheet

	# access cell C4
	#cell1 = active_sheet.getCellRangeByName("C4")

	# set text inside
	#cell1.String = "Hello world"

	# other example with a value
	#cell2 = active_sheet.getCellRangeByName("E6")
	#cell2.Value = cell2.Value + 1

	sheetName = active_sheet.Name 
	#print(sheetName)
	#cell1.String = sheetName
	#active_sheet.drawpage.hasElements

	#oSheets = model.getSheets()
	#oSheets.getByName("NewCopy").DrawPage.Forms
	if active_sheet.DrawPage.hasElements:
		elementCount = active_sheet.DrawPage.Count
		for i in range (elementCount):
			oShape = active_sheet.DrawPage.getByIndex(i)
			# print (i)
			control_name = oShape.Control.Name
			if oShape.Control.ValueBinding:
				oBoundCell = oShape.Control.ValueBinding.BoundCell
				oLinkedCell = uno.createUnoStruct("com.sun.star.table.CellAddress")
				oLinkedCell.Sheet = active_sheet.getRangeAddress().Sheet
				oLinkedCell.Column = oBoundCell.Column
				oLinkedCell.Row = oBoundCell.Row

				oNamedValue = uno.createUnoStruct("com.sun.star.beans.NamedValue")
				oNamedValue.Name  = "BoundCell"
				oNamedValue.Value = oLinkedCell
				oCVB = model.createInstance("com.sun.star.table.CellValueBinding")
				oCVB.initialize( (oNamedValue, ) )
				oShape.Control.setValueBinding(oCVB) 	
