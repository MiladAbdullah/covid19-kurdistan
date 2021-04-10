# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 22:06:00 2020

@author: Milad
"""

import real
import animator

freedom_level = 4
days = 20
world = real.World('map.jpg')
folder =  "sc4"
behavior = real.Behavior(world,freedom_level)
vid = animator.create_animation(world,behavior,days,folder)



    