# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:03:17 2020

@author: Milad
"""

# the models
from matplotlib.axes import Axes 
import matplotlib.patches as patches
import random as rnd
from random import randint,random
from matplotlib import pyplot as plt
import matplotlib

from PIL import Image
import numpy as np


HRes = 3
WRes = 3

#class Road:
#    def __init__ (self,x=2):
#        self.size = x
#        self.location = (0,0)
#    # find a random location within the house
#    def settle (self):
#        new_x = self.location[0]-(self.size/2)+(random()*self.size)
#        new_y = self.location[1]-(self.size/2)+(random()*self.size)
#        return (new_x,new_y)
#   
#    def __str__ (self):
#        return 'Road at %d,%d'%(self.location[0],self.location[1])

class Place:
#    colors= {'Home' :'#9be36b','School' : '#9abde6','University' : '#5b728c','Park' : '#3c6b46',
#            'Cafe' : '#b08348','Market' : '#d5de9e', 'Sport' : '#c8e026', 'Community' : '#ddf065',
#            'Office' : '#535d69','Hospital' : '#f03756' , 'Closed':'#5855c54' }
#    
    colors= {'Home' :[60, 140, 56],'School' :[116, 155, 179],'University' : [77, 100, 115],
             'Park' : [56, 99, 31],'Cafe' :[91, 99, 31],'Market' : [168, 184, 53], 
             'Sport' : [184, 138, 53], 'Community' :[112, 86, 37],'Office' : [51, 144, 214],
             'Hospital' : [171, 12, 38] , 'Closed':[122, 111, 105] }
    
    def __init__ (self,name,x=5):
        self.size = x*2
        self.location = (0,0)
        self.name= name
    # find a random location within the house
    def settle (self):
        new_x = self.location[0]+(random()*self.size)
        new_y = self.location[1]+(random()*self.size)
        return (new_x,new_y)
    def __str__ (self):
        return '%s at %d,%d'%(self.name,self.location[0],self.location[1])
    
#    def draw(self):
#        rect = patches.Rectangle(self.location,0.1,0.1,linewidth=0,facecolor=self.colors[self.name],edgecolor=None,in_layout=None,color=None)
#        return rect
    
    def draw(self,my_location,data):
        self.location = my_location
        start_x = int(self.location[0]*WRes)
        start_y= int(self.location[1]*HRes)
        end_x = int(start_x+self.size*HRes)
        end_y = int(start_y+self.size*HRes)
        
        data[start_y:end_y, start_x:end_x] = self.colors[self.name]
        return data
    
class Person:
    size = 0.01
    person_colors = {'male healthy':[72, 15, 105] , 
                     'female healthy':[171, 44, 245],
                     'male infected': [153, 52, 86],
                     'female infected':[240, 81, 135],
                     'male recovered':[142, 191, 184],
                     'female recovered':[140, 212, 201]
                     }
    
    def __init__ (self, home, work,age,occupation):
        self.gender = rnd.choice(['male','female'])
        self.location = home.settle()
        self.status = 'healthy'
        self.home = home
        self.work = work
        self.occupation = occupation
        self.age = age
        self.normal_behavior = Behavior(self)
    def random_move (self):
        new_x = self.location[0]+rnd.choice([-0.01,0.01])
        new_y = self.location[1]+rnd.choice([-0.01,0.01])
        if min(new_x,new_y)<=0 or max(new_x,new_y)>=1:
            new_x=0.5
            new_y=0.5
        
        self.location = (new_x,new_y)
    
    def style(self):
        return [self.location, self.person_colors["%s %s"%(self.gender,self.status)]]
    
    def render(self):
        if self.status == 'dead':
            return None
        start_x = int(self.location[0]*WRes)
        start_y= int(self.location[1]*HRes)
        end_x = int(start_x+self.size*WRes)
        end_y = int(start_y+self.size*WRes)
        
        info ={
                'start_x':start_x,
                'start_y':start_y,
                'end_x':end_x,
                'end_y':end_y,
                'color': self.person_colors["%s %s"%(self.gender,self.status)]}
        return info
class World:
    
    total_places= {'Home' : 10,'School' : 2,'University' : 1,'Park' : 1,
            'Cafe' : 2,'Market' : 2, 'Sport' : 1, 'Community' : 2,
            'Office' : 2,'Hospital' : 2 }
    
    work_names = ['School','University','Office','Market']
    fun_places = ['Sport','Community','Park','Cafe','Market']    
    configuration = {'Block Size':5, 'Infected':0.05, 'Recovery Days Range':(10,15),
                     'Death Rate': 0.01, 'Male Female Rate':(1,1), 'Max Age':90,  'Min Age':10,
                     'Adult Age':18, 'Retired Age':65, 'Population':100}
    
    
    def __init__ (self):
               
        self.people = []
        self.places = []
        self.categories ={}
        self.map_dict = {}
        self.map = np.zeros((HRes*100, WRes*100, 3), dtype=np.uint8)
        self.map[:,:]=[255,255,255]
        self.wave_map = {}
        self.road_map = np.zeros((100,100),dtype=np.uint8)
        """
        creates the places and their related sizes 
        """
            
        for place in self.total_places:
            for i in range(0,self.total_places[place]):
                pl = Place(place,self.configuration['Block Size'])
                self.places.append(pl)
                if place not in self.categories:
                    self.categories[place]=[]
                self.categories[place].append(pl)
             
        
        
        """
        this loop shuffles the places 20 times
        """
        # shuffling 20 times   
        for i in range(20):
            loc_a = randint(0,len(self.places)-1)
            loc_b = randint(0,len(self.places)-1)
            var = self.places[loc_a]
            self.places[loc_a] = self.places[loc_b]
            self.places[loc_b] = var
        """
        this loop generate the map (max_height by max_width),
        fills it with random places and roads
        each block consist of a place and a road from its right and top
        """
        
        total= len(self.places)-1
        for i in range(5,100,self.configuration['Block Size']*4):
            for j in range(5,100,self.configuration['Block Size']*4):
                if total>=0:
                    self.map_dict[(i,j)]= self.places[total]
                    self.places[total].location = (i,j)
                    total = total-1
        """
        apply wave algorithm for each place, for direction finding for people
        """
        for i in range(100):
            for j in range(100):
                    self.road_map[i,j]=self.is_road((i,j))
        for place in self.places:
            self.wave_map[place]=self.wave(place)
        
                    
        """
        the following create the individauls of the world
        
        """
        self.work_places= []
        for wplace in self.work_names:
            for p in self.categories[wplace]:
                self.work_places.append(p)
        
        population= self.configuration['Population']
        for p in range(population):
            home = rnd.choice(self.categories['Home'])
            occupation = 'Student'
            age = randint(self.configuration['Min Age'],self.configuration['Max Age'])
            if age>=self.configuration['Adult Age'] and age<self.configuration['Retired Age']:
                work = rnd.choice(self.work_places)
                occupation = 'Worker'
            else:
                work = None
                if age<6:
                    occupation = 'Child'
                else:
                    if age>=self.configuration['Retired Age']:
                        occupation = 'Retired'
                    else:
                        occupation = 'Student'
                        work = rnd.choice(self.categories['School'])
                        
            person = Person(home,work,age,occupation)
            self.people.append(person)


    """
    determine if there is road ,1-> road, 0->no road
    """
    def is_road(self,location):
        road_ranges = [(i*5,(i*5)+9) for i in range(1,20,4)]
        x_c = location[1]
        y_c = location[0]
        
        for x_ranges in road_ranges:
            for y_ranges in road_ranges: 
                if x_c>=x_ranges[0] and  x_c<=x_ranges[1] and y_c>=y_ranges[0] and y_c<=y_ranges[1]:
                    return 0
        return 1
    
    def what_is (self,location):
        if min(location[0],location[1])<0:
            return None
    
        if location[0]>=100 or location[1]>=100 :
          return None
      
        return self.road_map[location[1],location[0]]
      

    def wave(self, place):
        res = np.zeros((100,100), dtype=np.uint8)
        
        def extract_sides(point):
            return [
                    (point[0]+1,point[1]),      #east
                    (point[0]+1,point[1]+1),    #north east
                    (point[0]+1,point[1]-1),    #south east
                    (point[0],point[1]+1),      #north
                    (point[0],point[1]-1),      #south
                    (point[0]-1,point[1]),      #west
                    (point[0]-1,point[1]+1),    #north west
                    (point[0]-1,point[1]-1),    #south west
                    ]
       
            
        stack = [place.location]
        res[place.location[0],place.location[1]]=1
        
        while len(stack)>0:
            target = stack.pop(0)
            map_v = res[target[0],target[1]]
            new_list = extract_sides(target)
            for point in new_list:
                v = self.what_is (point)
                if v==None:
                    continue
                if v==1: #road
                    current_v = res[point[0],point[1]]
                    if current_v == 0 or current_v>map_v+1:
                        res[point[0],point[1]]=map_v+1
                        stack.append(point)
        return res
    """
        finds the content of the location, a house, a road ....
    """            
    
    
    def draw_places (self):
        for place in self.map_dict:
            self.map = self.map_dict[place].draw(place,self.map)
        return self.map

    def move_people(self):
        for person in self.people:
            person.random_move() 
    
#        
    def show_people(self):
        people_map = np.copy(self.map)
        for person in self.people:
            style = person.render()
            if style==None:
                continue
            people_map[style['start_x']:style['end_x'],style['start_y']:style['end_y']]=style['color']
        return people_map

class Behavior:
    

    def __init__ (self,person):
        Adult_Life_Work_Day = {
                                (0,8):'Home',
                                (8,13):'Work',
                                (13,14):'Food',
                                (14,19):'Fun',
                                (19,20):'Food',
                                (20,23):'Fun',
                                (23,24):'Home'}
        
        self.fate = None
        if person.occupation=='Worker':
            self.fate = Adult_Life_Work_Day
        