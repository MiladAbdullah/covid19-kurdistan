# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:12:20 2020

@author: Milad
"""

import numpy as np
from PIL import Image
from random import randint, random
import random as rnd
import math


PLACES = {
        'Road':[0,0,0],             #black
        'Mosque':[12,114,68],       #Dark Green
        'Market':[245,122,122],     #Meduim Coral
        'Home':[255,235,175],       #Topaz Sand
        'School':[255,211,127],     #Mango
        'Garden':[85,255,0],        #Meduim Apple
        'Blank':[255,255,255],      #White
        }

COLORS = {tuple(PLACES[key]):key for key in PLACES}

"""
    this function finds the closest color match of the map to the 
    list of colors we have. Each Color represents a location.
"""

def find_closest_color (previous_color):
    tollerance = 50
    difference = {sum([abs(previous_color[i]-PLACES[k][i]) for i in range(3)]):k for k in PLACES}
    result = min(difference.keys())
    if result<tollerance:
        min_diff = difference[result]
        return PLACES[min_diff]
    else:
        return PLACES['Road']

"""
    for each cell the color is refined to leave the ambigituy of various colors
    the following function shows the color in better prespectives
    the clean dirt method also removes lonely cells
"""

def refine_colors(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i,j]=find_closest_color(image[i,j])
    return image

def clean_dirt (array):

    def refine_point (dirty_array,i,j):
        neighbours = extract_sides((i,j))
        value = dirty_array[i,j]
        similar = 0
        example = value
        for neighbour in neighbours:
            
            diff = dirty_array[neighbour[0],neighbour[1]]==value
            #print (diff)
            if all(diff):
                similar=similar+1
            else:
                example = dirty_array[neighbour[0],neighbour[1]]
        
        if similar<3:
            dirty_array[i,j] = example
    for i in range(1,len(array)-1):
        for j in range(1,len(array[i])-1):
                refine_point(array,i,j)
    return array
        

""" a method that will extracts the eight sides of a point
    point (y,x)    
    point[0] -> on y axis from top
    point[1] -> on x axis from left
"""

def extract_sides(point):
        return [
                (point[0],point[1]+1),      #east
                (point[0],point[1]-1),      #west
                (point[0]+1,point[1]),      #south
                (point[0]+1,point[1]+1),    #south east
                (point[0]+1,point[1]-1),    #south west
                (point[0]-1,point[1]),      #north
                (point[0]-1,point[1]+1),    #north east
                (point[0]-1,point[1]-1),    #north west
            ] 

"""
    a class that represents the locations
"""

def identify_places(array):
    h = len(array)
    w= len(array[0])
    place_ids = np.zeros((h,w),dtype=np.uint8)
    
    #start point
    current_id = 1
    place_types = {0:'Blank', 1:'Road'}
    place_points = {}
    for i in range(h):
        for j in range(w):
            if place_ids[i,j]>=1:
                continue
            
            key = tuple(array[i,j])
            style = COLORS[key]
            if style=='Blank':
                continue
            
            if style=='Road':
                place_ids[i,j]=1
                continue
            # wave from here
            current_id= current_id +1
            place_ids[i,j]=current_id
            place_points[current_id] = [(i,j)]
            # new style
            place_types[current_id]=style

            queue = [(i,j)]
            while len(queue)>0:
                target = queue.pop(0)
                sides = extract_sides(target)
                for side in sides:

                    side_i =side[0]
                    side_j = side[1]
                    if place_ids[side_i,side_j]>=1:
                        continue
                    side_key = tuple(array[side_i,side_j])
                    side_style = COLORS[side_key]
                    if side_style=='Blank' or side_style=='Road':
                        continue
                    place_ids[side_i,side_j]=current_id
                    queue.append((side_i,side_j))
                    place_points[current_id].append((side_i,side_j))
                
                 
    return place_ids,place_types,place_points
                 
            


class Place:
    points = []
    p_type = 'Garden'
    p_id = 0
    p_name = ''
    def __init__ (self,p_id,p_type,points,minimap):
        self.p_id = p_id
        self.p_type = p_type        
        self.p_name = '%s-%d'%(p_type,p_id)
        self.points = points
        self.minimap = minimap
    
    def settle(self,current_position):
        sides = extract_sides(current_position)
        new_p = rnd.choice(sides)
        if self.minimap.place_ids[new_p[0],new_p[1]]==self.p_id:
            return new_p
        else:
            return rnd.choice(self.points)

    
""" 
    a type that represents a map for the world
"""


class MiniMap:
    height = 0
    width = 0
    
    def __init__ (self, filename):
        self.raw_image = Image.open(filename)
        self.height = self.raw_image.height
        self.width= self.raw_image.width
        
        # convert image to array
        self.raw_array = np.array(self.raw_image)
        
        #refine themap and save it as numpy and image both
        self.refine_array = refine_colors(np.copy(self.raw_array))
        self.refine_array = clean_dirt(self.refine_array)
        self.refine_image = Image.fromarray(self.refine_array, 'RGB')
        
        # create places
        self.places = {}
       
        self.place_ids , self.place_types,self.place_points= identify_places(self.refine_array)
        for p_id in self.place_types:
            if p_id<2:
                continue
            new_place = Place(p_id,self.place_types[p_id],self.place_points[p_id],self)
            self.places[p_id]=new_place

ecu_dist= lambda a,b : math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))
class Person:
    size = 4    #pixels
    person_colors = {'male healthy':[72, 15, 105] , 
                     'female healthy':[171, 44, 245],
                     'male infected': [153, 52, 86],
                     'female infected':[240, 81, 135],
                     'male recovered':[142, 191, 184],
                     'female recovered':[140, 212, 201]
                     }
    conditions=[
            'healthy',
            'infected',
            'recovered',
            'death']
    
    #standard distance
    minimum_distance = 10
    infection_rate = 0.9
    
    h_id = 0 #human id
    #eculdean distance
    
    def __init__ (self,h_id, age,home,world,status=0):
        self.gender = rnd.choice(['male','female'])
        self.location = rnd.choice(home.points)
        self.status = self.conditions[status]
        self.home = home
        self.age = age
        self.world = world
        self.h_id= h_id
        self.power = 3
        
    def render(self):
        style = {
                'x1':int(self.location[1]-(self.size/2)),
                'y1':int(self.location[0]-(self.size/2)),
                'x2':int(self.location[1]+(self.size/2)),
                'y2':int(self.location[0]+(self.size/2)),
                'color':self.person_colors['%s %s'%(self.gender,self.status)]
                }
                
        return style
    def stay_home (self):
        self.location = self.home.settle(self.location)
        if self.status=='infected':
            other_people = {p.h_id:ecu_dist(p.location,self.location) for p in self.world.people if p!=self and p.status=='healthy'}
            close_people = [p for p in  other_people if other_people[p]<self.minimum_distance]
            while len(close_people)>0:
                target = self.world.people[close_people.pop()]
                infection_power = self.infection_rate * self.power
                # possible cantor sets
                self.power -= 1
                fate = random()
                if fate<infection_power:
                    target.infect(self)
                    
            
    def infect (self,source):
        self.status=self.conditions[1]
        self.world.report_infection(self,source)

class World:
    
    
    Settings = {'Population':120,'Min Age':18, 'Max Age':85, 
                'Infected':0.04,'Infection Probability':0.9,'Recovery Period':(10,15)}
    
    WeekDays = [
            'Saturday',
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday']
    
    
    def __init__ (self):
        self.current_map = MiniMap('Karezan/map1_editted.jpg')
        self.homes = [x for x in self.current_map.place_types if self.current_map.place_types[x]=='Home' ]
        
        self.Day = 1
        rand_day = randint(0,6)
        for i in range(rand_day):
            self.WeekDays.append( self.WeekDays.pop(0))
        
        self.WeekDay =self.WeekDays[6]
        
        #reports
        self.people_conditions = {
                'healthy':{},
                'infected':{},
                'recovery':{},
                'dead':{},
                }
        
        
        
        self.people = []
        total_infected = int(self.Settings['Infected']*self.Settings['Population'])
        infected_counter = total_infected
        for i in range(self.Settings['Population']):
            rand_age = randint(self.Settings['Min Age'],self.Settings['Max Age'])
            home = rnd.choice(self.homes)
            health_status = 0       #health
            if infected_counter>0:
                health_status=1
                infected_counter= infected_counter-1
            person = Person(i,rand_age,self.current_map.places[home],self,health_status)
            self.people_conditions[person.status][i]=person
            self.people.append(person)
            
        self.daily_report = {
                'Week Day':[self.WeekDay],
                'Day':[1],
                'New Infected':[total_infected],
                'Total Infected':[total_infected],
                'New Recovered':[0],
                'Total Recovered':[0],
                'New Death':[0],
                'Total Death':[0],
                'Active Cases':[total_infected],}
        
        self.infected_log ={
                'ID':[self.people_conditions['infected'][d].h_id for d in self.people_conditions['infected']],
                'age':[self.people_conditions['infected'][d].age for d in self.people_conditions['infected']],
                'gender':[self.people_conditions['infected'][d].gender for d in self.people_conditions['infected']],
                # ugly
                'date':[int(self.people_conditions['infected'][d].age/self.people_conditions['infected'][d].age) for d in self.people_conditions['infected']],
                'infected_from':[self.people_conditions['infected'][d].h_id for d in self.people_conditions['infected']],
                'house_id':[self.people_conditions['infected'][d].home.p_id for d in self.people_conditions['infected']],
                    }  
        self.recovery_log ={
                'ID':[],
                'age':[],
                'gender':[],
                'date':[],
                'house_id':[],
                    }
        self.death_log ={
                'ID':[],
                'age':[],
                'gender':[],
                'date':[],
                'house_id':[],
                    } 
        
    def add_daily_report(self,new_case, new_recoverd,new_death):
        index = self.Day - 1
        self.daily_report['New Infected'][index] +=new_case
        self.daily_report['Total Infected'][index] = self.daily_report['Total Infected'][index-1]+self.daily_report['New Infected'][index]
        self.daily_report['New Recovered'][index] +=new_recoverd
        self.daily_report['Total Recovered'][index] = self.daily_report['Total Recovered'][index-1]+self.daily_report['New Recovered'][index]
        self.daily_report['New Death'][index] +=new_death
        self.daily_report['Total Death'][index] = self.daily_report['Total Death'][index-1]+self.daily_report['New Death'][index]
        self.daily_report['Active Cases'][index] = self.daily_report['Total Infected'][index]-(self.daily_report['Total Death'][index]+self.daily_report['Total Recovered'][index])
        
        

    def report_infection (self,person,source):
        self.infected_log['ID'].append(person.h_id)
        self.infected_log['age'].append(person.age)
        self.infected_log['gender'].append(person.gender)
        self.infected_log['date'].append(self.Day)
        self.infected_log['infected_from'].append(source.h_id)
        self.infected_log['house_id'].append(person.home.p_id)
        self.add_daily_report(1,0,0)
        
        
        
    def report_recover (self,person):
        self.recovery_log['ID'].append(person.h_id)
        self.recovery_log['age'].append(person.age)
        self.recovery_log['gender'].append(person.gender)
        self.recovery_log['date'].append(self.Day)
        self.recovery_log['house_id'].append(person.home.p_id)
        self.add_daily_report(0,1,0)
      
    def report_death (self,person):
        self.death_log['ID'].append(person.h_id)
        self.death_log['age'].append(person.age)
        self.death_log['gender'].append(person.gender)
        self.death_log['date'].append(self.Day)
        self.death_log['house_id'].append(person.home.p_id) 
        self.add_daily_report(0,0,1)
        
    def list_poeple (self,age='all',gender='all'):
        pass
        
    def next_day (self):
        self.Day = self.Day+1
        self.WeekDays.append( self.WeekDays.pop(0))
        self.WeekDay =self.WeekDays[6]
        self.daily_report['Week Day'].append(self.WeekDay)
        self.daily_report['Day'].append(self.Day)
        self.daily_report['New Infected'].append(0)
        # one day ago
        self.daily_report['Total Infected'].append(self.daily_report['Total Infected'][self.Day-2])
        self.daily_report['New Recovered'].append(0)
        self.daily_report['Total Recovered'].append(self.daily_report['Total Recovered'][self.Day-2])
        self.daily_report['New Death'].append(0)
        self.daily_report['Total Death'].append(self.daily_report['Total Death'][self.Day-2])
        self.daily_report['Active Cases'].append(0)
        
    
    def show_world(self):
        base_map = np.copy(self.current_map.raw_array)
        for person in self.people:
            person.stay_home()
            style = person.render()
            base_map[style['y1']:style['y2'],style['x1']:style['x2']]=style['color']
        self.next_day()
        return Image.fromarray(base_map, 'RGB')

