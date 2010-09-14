#! /usr/bin/env python
# -*- coding: utf-8 -*-

renderhtml_page_header_template = """
<html>
<head>
	<style type="text/css">
		table.parts {
			border-width: 1px;
			border-spacing: 3px;
			border-style: outset;
			border-color: black;
			background-color: white;
		}
		table.parts th {
			border-width: 1px;
			padding: 3px;
			border-style: outset;
			border-color: black;
			background-color: white;
		}
		table.parts td {
			border-width: 1px;
			padding: 3px;
			border-style: outset;
			border-color: black;
			background-color: white;
			text-align: center;
		}
	</style>
	<title>%EAGLE3D% - %TITLE%</title>
</head>
<body>
<center><h3>%EAGLE3D% - %TITLE%</h3></center>
<center>
	<table class="parts">
		<tr>"""

renderhtml_page_body_template = """
			<td width="%CELL_SIZE_X%" height="%CELL_SIZE_Y%" title="%THUMB_TEXT%" >
				<a href="%THUMB_A_HREF%" >
					<img width="%THUMB_SIZE_X%" height="%THUMB_SIZE_Y%" src="%THUMB_IMG_SRC%" />
				</a>
			</td>"""

renderhtml_page_footer_template = """
		</tr>
	</table>
</center>
<center>
	<p>%TOC%</p>
	<p></p>
	<p></p>
	<p>%EAGLE3D%</p>
</center>
</body>
</html>
"""


renderhtml_index_header_template = """
<html>
<head>
	<style type="text/css">
		table.parts {
			border-width: 1px;
			border-spacing: 3px;
			border-style: outset;
			border-color: black;
			background-color: white;
		}
		table.parts th {
			border-width: 1px;
			padding: 3px;
			border-style: outset;
			border-color: black;
			background-color: white;
		}
		table.parts td {
			border-width: 1px;
			padding: 3px;
			border-style: outset;
			border-color: black;
			background-color: white;
			text-align: center;
		}
	</style>
	<title>%EAGLE3D% - Index</title>
</head>
<body>
<center><h3>%EAGLE3D% - Index</h3></center>
<center>
	<table class="parts">"""

renderhtml_index_body_template = """
		</tr>
		<tr>
			<td title="%INDEX_TITLE%" >
				<a href="%INDEX_HREF%" >%INDEX_NAME%</a>
			</td>
		</tr>"""

renderhtml_index_footer_template = """
		</tr>
	</table>
</center>
<center>
	<p></p>
	<p>%EAGLE3D%</p>
</center>
</body>
</html>
"""
