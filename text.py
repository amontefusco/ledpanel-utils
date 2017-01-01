#!/usr/bin/python
# Show a sliding text on RGB led panel
# (c) 2014 Sergio Tanzilli - sergio@tanzilli.com 
# multiple panel capability added by A.Montefusco 2017, 
# requires ledpanel.ko 2.0

import time
import sys
import os
from datetime import datetime
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import StringIO
import probe

if len(sys.argv)<6 or len(sys.argv)>6:
	print "Syntax:"
	print "  %s text r g b loop" % (sys.argv[0])
	print
	print  "loop=0 forever loop"
	
	quit()
	
print "Panel size: %d x %d\n" % (probe.panel_w, probe.panel_h)

font = ImageFont.truetype('fonts/Ubuntu-B.ttf', probe.panel_h)

text=sys.argv[1]
r=int(sys.argv[2])
g=int(sys.argv[3])
b=int(sys.argv[4])
loops=int(sys.argv[5])
	
im = Image.new("RGB", (probe.panel_w, probe.panel_h), "black")
draw = ImageDraw.Draw(im)
draw.fontmode="1" #No antialias
width, height = font.getsize(sys.argv[1])
  
out_file = open("/sys/class/ledpanel/rgb_buffer","w")
output = StringIO.StringIO()

x = probe.panel_w

while True:
	x=x-1
	
	if x < -(width):
		if loops==0:
			x = probe.panel_w
			continue
		else: 
			if loops==1:
				break
			else:
				loops=loops-1	
				x = probe.panel_w
				continue
		
	draw.rectangle((0, 0, probe.panel_w - 1, height), outline=0, fill=0)
	draw.text((x, -1), text, (r,g,b), font=font)

	output.truncate(0)
	im.save(output, format='PPM')
	buf=output.getvalue()

	out_file.seek(0)
	out_file.write(buf[13:])

out_file.close()
