# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:33:47 2020

@author: Milad
"""

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.pyplot import figure
import numpy as np
 
def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.frombuffer ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

#
def fig2img ( fig ):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data ( fig )
    w, h, d = buf.shape
    return Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )


def animate(world,behavior,days):
    images=[]
    for i in range(days):
        img= world.run_day(behavior)
        images.extend(img)
    return images


def show_plots(world):
    plots=[]
    plt.ioff()
    xlim = len(world.reports['Daily Report'])
    for i in range(1,xlim):

        x= figure(num=None, figsize=(6, 5), dpi=100, facecolor='w', edgecolor='k')
        a= world.reports['Daily Report']['Active Cases'][0:i]
        b= world.reports['Daily Report']['Total Recovered'][0:i]
        c= world.reports['Daily Report']['Total Death'][0:i]
        d= world.reports['Daily Report']['Total Infected'][0:i]
        x1 = [i for i in range(0,i)]
        # plotting the line 1 points 
        plt.plot(x1, a,color='blue', label = "Active Cases")
        plt.plot(x1, b,color='green', label = "Total Recovered")
        plt.plot(x1, c,color='red', label = "Total Death")
        plt.fill_between(x1,d ,color='yellow', label = "Total Cases")
        plt.xlim([0,xlim])
        plt.xticks(x1)
        plt.ylim([0,world.Settings['Population']])
        plt.xlabel('Day')
        # Set the y axis label of the current axis.
        plt.ylabel('Cases')
        # Set a title of the current axes.
        plt.title('COVID-19 Event Reports ')
        # show a legend on the plot
        plt.legend()
        # Display a figure.
        plots.append(fig2img(x))
        plt.cla()   # Clear axis
        plt.clf()   # Clear figure
        plt.close()
    return plots


def make_video(images, filename, fps):
    """
    Create a video from a list of images.
 
    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
 
    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    import cv2
    size = None
    vid = None
    for img in images:
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        if vid is None:
            if size is None:
                frame_height,frame_width = frame.shape[:2]
            vid = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))
        vid.write(frame)
    vid.release()
    return vid
        
def create_animation(world,behavior,days,folder):
    images = animate(world,behavior,days)

    frame_per_second = 300
    make_video(images,'%s/world.avi'%folder,frame_per_second)

    plots = show_plots(world)
    world.save_reports(folder)

    make_video(plots,'%s/chart.avi'%folder,1)