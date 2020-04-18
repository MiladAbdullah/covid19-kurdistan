# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:33:47 2020

@author: Milad
"""

#import matplotlib.pyplot as plt
from PIL import Image
import io

import numpy
 
#def fig2data ( fig ):
#    """
#    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
#    @param fig a matplotlib figure
#    @return a numpy 3D array of RGBA values
#    """
#    # draw the renderer
#    fig.canvas.draw ( )
# 
#    # Get the RGBA buffer from the figure
#    w,h = fig.canvas.get_width_height()
#    buf = numpy.frombuffer ( fig.canvas.tostring_argb(), dtype=numpy.uint8 )
#    buf.shape = ( w, h,4 )
# 
#    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
#    buf = numpy.roll ( buf, 3, axis = 2 )
#    return buf
#
#
#def fig2img ( fig ):
#    """
#    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
#    @param fig a matplotlib figure
#    @return a Python Imaging Library ( PIL ) image
#    """
#    # put the figure pixmap into a numpy array
#    buf = fig2data ( fig )
#    w, h, d = buf.shape
#    return Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

# equivalent to rcParams['animation.html'] = 'html5'

import life
myw = life.World()

images=[]
#
#def animate(minutes):
#    figure=  plt.figure(num=None, figsize=(2,2), dpi=200)
#    figure.patch.set_alpha(0)
#    ax1 = myw.draw_places(figure)
#    figure.add_axes(ax1)
#    for i in range(minutes):
#        myw.move_people()
#        ax2 = myw.show_people(figure)
#        figure.add_axes(ax2)
#        #im = fig2img ( figure )
#        images.append(im)
#        #plt.savefig('../life/test/p%s'%i)
#        plt.cla()
#
#
def animate(minutes):
    temp = myw.draw_places()
    for i in range(minutes):
        new_d = myvw.show_people()
        myw.move_people()
        img = Image.fromarray(new_d, 'RGB')
        images.append(img)
animate(1410)


images[0].save('../life/test/pillow_imagedraw.gif',
               save_all=True, append_images=images[1:], optimize=True, duration=100, loop=0)