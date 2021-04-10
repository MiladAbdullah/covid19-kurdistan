# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:12:20 2020

@author: Milad
"""

import numpy as np
from PIL import Image,ImageDraw, ImageFont
from random import randint, random
#from collections.abc import Sequence
import pandas as pn
import random as rnd
import math
"""
    recovery function
    0 < age  < 1 .. means the min age is 0 and max age is 1
    0 < disease < 1 having a lot of disease means 1 and healthies is 0
    
    recovery is a number less than 1, means how probable that is the patient will be recovered
    
"""
Recovery = lambda age,disease: (disease+age)/10

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

            # a loop that will search through whole area
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
                 
            
def move_to_point(p1,p2):
    x_m = 0
    y_m = 0
    if p1[0]!=p2[0]:
        x_m = int((p2[0]-p1[0])/abs(p2[0]-p1[0]))
    if p1[1]!=p2[1]:
        y_m = int((p2[1]-p1[1])/abs(p2[1]-p1[1]))
    return x_m,y_m

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
    def __getitem__(self, i):
        if i==0 or i==1:
            return self.points[0][i]
        else:
            return 0
    
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
    sizes = {'healthy':5,
             'infected':7,
             'recovered':4,
             'dead':2
             }#pixels
    
    disease_scores= {
                'Cardiovascular disease':0.8,
                'Diabetes':0.7,
                'Chronic respiratory disease':0.6,
                'Hypertension':0.5,
                'Cancer':0.4,
                
            }

    person_colors = {'male healthy':[139, 31, 255] , 
                     'female healthy':[139, 31, 255],
                     'male infected': [255, 34, 0],
                     'female infected':[255, 34, 0],
                     'male recovered':[25, 247, 77],
                     'female recovered':[25, 247, 77],
                     'male dead':[181, 154, 152],
                     'female dead':[181, 154, 152]
                     }
    conditions=[
            'healthy',
            'infected',
            'recovered',
            'dead']
    
    #standard distance
    minimum_distance = 2
    infection_rate = 0.9
    effected_day = 0
    h_id = 0 #human id
    #eculdean distance
    
    def __init__ (self,h_id, age,world,status=0):
        self.gender = rnd.choice(['male','female'])
        self.status = self.conditions[status]
        self.home = rnd.choice(world.homes)
        self.location = rnd.choice(self.home.points)
        self.age = age
        self.world = world
        self.h_id= h_id
        self.power = 3
        self.next_place = self.home 
        self.current_place = self.home 
        if status!=1:
            self.effected_day = 1
        
        self.disease = 0.1
        if self.age>55:
            self.disease = random()/1.5
        age_rate =(self.age-world.Settings['Min Age'])/(world.Settings['Max Age']-world.Settings['Min Age'])
        self.recovery_rate = 1-Recovery(age_rate,self.disease)
        rec_period = world.Settings['Recovery Period']
        self.fate_day = randint(rec_period[0],rec_period[1])
        self.target = self.home
        
    def render(self):
        self.size = self.sizes[self.status]
        style = {
                'x1':int(self.location[1]-(self.size/2)),
                'y1':int(self.location[0]-(self.size/2)),
                'x2':int(self.location[1]+(self.size/2)),
                'y2':int(self.location[0]+(self.size/2)),
                'color':self.person_colors['%s %s'%(self.gender,self.status)]
                }
                
        return style

    def move (self,point_to_get):

        mover_a, mover_b= move_to_point(self.location,point_to_get)
        self.location= (self.location[0]+mover_a,self.location[1]+mover_b)
        
    def live (self,minute,day,action):
        
        if self.status=='dead':
            return
        
        if self.location in self.target.points:
            
            self.location = self.target.settle(self.location)
                
            self.target = action(self)
        else:
            self.move(self.target)
        

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
                    target.infect(self,self.location,day)
            
            if self.fate_day==day:
                fate = random()
                if self.recovery_rate>fate:
                    self.recover()
                else:
                    self.die()
                    
        
                
                
        
                    
            
    def infect (self,source,location,day):
        self.effected_day = day
        self.status=self.conditions[1]
        place= self.world.current_map.place_ids[location[0],location[1]]
        self.world.report_infection(self,source,place)
        
    def die (self):
        self.status=self.conditions[3]
        self.world.report_death(self)
    
    def recover(self):
        self.status=self.conditions[2]
        self.world.report_recover(self)

class Report():
    title = ''
    data = {}    
    def __init__ (self,title,data):
        self.title = title
        self.data = data
        super().__init__()
    
    def __getitem__(self, i):
        return self.data[i]
    
    def __len__(self):
        try:
            k=max([len(self.data[t]) for t in self.data ])
            return k
        except:
            return 0
    
    def append (self,new):
        for col in new:
            self.data[col].append(new[col])
    
    def update (self,index,eddited):
        
        for col in eddited:
            self.data[col][index] =eddited[col] 

    def csv(self,subfolder=""):
        dataFrame = pn.DataFrame(self.data)
        dataFrame.to_csv('%s/%s.csv'%(subfolder,self.title))
        
    


class World: 
    Settings = {'Population':100,'Min Age':5, 'Max Age':80, 
                'Infected':0.01,'Recovery Period':(5,15),
                'Iteration Time':3, 'Entire Day':900,'Start Day':0}
    
    WeekDays = [
            'Saturday',
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday']
    
    world_hour_minutes= int(60/Settings['Iteration Time'])
    
    #less randomized world
    def __init__(self,map_address):
        
        self.current_map = MiniMap(map_address)
        self.homes = [self.current_map.places[x] for x in self.current_map.place_types if self.current_map.place_types[x]=='Home' ]
        self.Minute = 0
        self.Day = 1       
        for i in range(self.Settings['Start Day']):
            self.WeekDays.append( self.WeekDays.pop(0))
        self.WeekDay =self.WeekDays[6]
        self.people = []
        self.initialy_infected_people = []
        total_infected = int(self.Settings['Infected']*self.Settings['Population'])
        infected_counter = total_infected
        for i in range(self.Settings['Population']):
            rand_age = randint(self.Settings['Min Age'],self.Settings['Max Age'])
            health_status = 0       #health
            if infected_counter>0:
                health_status=1
                infected_counter= infected_counter-1
            person = Person(i,rand_age,self,health_status)
            if health_status==1:
                self.initialy_infected_people.append(person)
            self.people.append(person)
        
                #reports
        self.reports = {
                'Daily Report':Report('Daily Report',{
                                        'Week Day':[self.WeekDay], 'Day':[self.Day],
                                        'New Infected':[len(self.initialy_infected_people)],  'Total Infected':[len(self.initialy_infected_people)],
                                        'New Recovered':[0], 'Total Recovered':[0],
                                        'New Death':[0],  'Total Death':[0],   'Active Cases':[len(self.initialy_infected_people)]}),
        
                'Event Report':Report('Event Report',{
                                        'Week Day':[0], 'Day':[0], 'Time':['0:0'],'Person ID':[-1],
                                        'New Infected':[0],  'Total Infected':[0],
                                        'New Recovered':[0], 'Total Recovered':[0],
                                        'New Death':[0],  'Total Death':[0],   'Active Cases':[0]}),
        
                'Infected Log':Report('Infected Log',{ 'ID':[], 'Age':[], 'Gender':[],'Date':[],'Infected from':[], 'Home ID':[], 'Infected location id':[] }),
        
                'Recovery Log':Report('Recovery Log',{'ID':[],'Age':[],'Gender':[],'Date':[],'Home ID':[]}),
        
                'Death Log':Report('Death Log',{ 'ID':[], 'Age':[], 'Gender':[],'Date':[],'Home ID':[],'Disease danger rate':[]}),
        
                'Population':Report('Population',{'ID':[],'Age':[],'Gender':[],'Home ID':[],'Disease danger rate':[]}),
        
                'Places':Report('Places',{'ID':[],'Type':[],'Habitants':[],})
        }
                
    
                
        for infected in self.initialy_infected_people:
            self.reports['Infected Log'].append({
                'ID':infected.h_id, 
                'Age':infected.age,
                'Gender':infected.gender,
                'Date':self.Day,
                'Infected from':-1, 
                'Home ID':infected.home.p_id, 
                'Infected location id': infected.home.p_id})
            self.add_event_report(1,0,0,infected.h_id)

    def add_event_report(self,new_case, new_recoverd,new_death,h_id):
        index = len(self.reports['Event Report'])
        total_inf = new_case+ self.reports['Event Report']['Total Infected'][index-1]
        total_rec = new_recoverd+ self.reports['Event Report']['Total Recovered'][index-1]
        total_de = new_death+ self.reports['Event Report']['Total Death'][index-1]
        
        active_case = total_inf-(total_rec+total_de)
        
        current_hour = 9+math.floor(self.Minute/self.world_hour_minutes)
        current_minute = np.mod(self.Minute,self.world_hour_minutes)
        
        self.reports['Event Report'].append({
                    'Week Day':self.WeekDay, 
                    'Day':self.Day,
                    'Time':'%d:%d'%(current_hour,current_minute),
                    'Person ID':h_id,
                    'New Infected':new_case,  
                    'Total Infected':total_inf,
                    'New Recovered':new_recoverd, 
                    'Total Recovered':total_rec,
                    'New Death':new_death,
                    'Total Death':total_de,
                    'Active Cases':active_case})
        
    def add_daily_report(self,new_case, new_recoverd,new_death):
        index = self.Day - 1
        new_inf = new_case+self.reports['Daily Report']['New Infected'][index]
        total_inf = new_inf+ self.reports['Daily Report']['Total Infected'][index-1]
        
        new_rec = new_recoverd+self.reports['Daily Report']['New Recovered'][index]
        total_rec = new_rec+ self.reports['Daily Report']['Total Recovered'][index-1]
        
        new_de = new_death+self.reports['Daily Report']['New Death'][index]
        total_de = new_de+ self.reports['Daily Report']['Total Death'][index-1]
        
        active_case = total_inf-(total_rec+total_de)
        self.reports['Daily Report'].update(index,{
                            'New Infected':new_inf,
                            'Total Infected':total_inf,
                            'New Recovered':new_rec,
                            'Total Recovered':total_rec,
                            'New Death':new_de,
                            'Total Death':total_de,
                            'Active Cases':active_case })
        

    def report_infection (self,person,source,place):
        self.reports['Infected Log'].append({
                'ID':person.h_id, 
                'Age':person.age,
                'Gender':person.gender,
                'Date':self.Day,
                'Infected from':source.h_id, 
                'Home ID':person.home.p_id, 
                'Infected location id': place})
        
        self.add_daily_report(1,0,0)
        self.add_event_report(1,0,0,person.h_id)
        
        
    def report_recover (self,person):
        self.reports['Recovery Log'].append({
                'ID':person.h_id,
                'Age':person.age,
                'Gender':person.gender,
                'Date':self.Day,
                'Home ID':person.home.p_id})
    
        self.add_daily_report(0,1,0)
        self.add_event_report(0,1,0,person.h_id)
      
    def report_death (self,person):
        self.reports['Death Log'].append({
                'ID':person.h_id, 
                'Age':person.age, 
                'Gender':person.gender,
                'Date':self.Day,
                'Home ID':person.home.p_id,
                'Disease danger rate':person.disease})
        self.add_daily_report(0,0,1)
        self.add_event_report(0,0,1,person.h_id)
        
    def new_day (self):
        self.Day = self.Day+1
        self.WeekDays.append( self.WeekDays.pop(0))
        self.WeekDay =self.WeekDays[6]
        
        self.reports['Daily Report'].append({
                    'Week Day':self.WeekDay, 'Day':self.Day,
                    'New Infected':0,  
                    'Total Infected':self.reports['Daily Report']['Total Infected'][self.Day-2],
                    'New Recovered':0, 
                    'Total Recovered':self.reports['Daily Report']['Total Recovered'][self.Day-2],
                    'New Death':0,
                    'Total Death':self.reports['Daily Report']['Total Death'][self.Day-2],
                    'Active Cases':self.reports['Daily Report']['Active Cases'][self.Day-2] })
        
        
    def show_world(self,action):
        base_map = np.copy(self.current_map.raw_array)
        for person in self.people:
            
            person.live(self.Minute,self.Day,action)
            style = person.render()
            base_map[style['y1']:style['y2'],style['x1']:style['x2']]=style['color']
        img = Image.fromarray(base_map, 'RGB')
        text_area = ImageDraw.Draw(img)
        

        current_hour = 9+math.floor(self.Minute/self.world_hour_minutes)
        current_minute = np.mod(self.Minute,self.world_hour_minutes)*3
        text_area.text((200,270), 
                       "Day %d . Time %d:%d"%(self.Day,current_hour,current_minute),
                       font=ImageFont.truetype("arial.ttf", 18) ,
                       fill=(0,0,0))
        
        text_area.text((200,290), 
                       "Total Infected:%d"%(self.reports['Event Report']['Total Infected'][-1]),
                       font=ImageFont.truetype("arial.ttf", 16) ,
                       fill=(0,0,0))
        text_area.text((200,310), 
                       "Total Recovered:%d"%(self.reports['Event Report']['Total Recovered'][-1]),
                       font=ImageFont.truetype("arial.ttf", 16) ,
                       fill=(0,0,0))
        text_area.text((200,330), 
                       "Total Death:%d"%(self.reports['Event Report']['Total Death'][-1]),
                       font=ImageFont.truetype("arial.ttf", 16) ,
                       fill=(0,0,0))  
        return img

    # an active day is 900 Minutes
    """
         from 9:00 AM - 12 PM there are 900 Minutes
         each iteration by default is 3 minutes, and
         therefore, a whole day is 900/3 iterations 
    """
    
    def save_reports(self,subfolder=""):
        for report in self.reports:
            self.reports[report].csv(subfolder)
    
    def save_report(self,report,subfolder=""):
        for report in self.reports:
            report.csv(subfolder)
    
    def run_day (self, behavior):
        self.new_day()
        whole_day = int(self.Settings['Entire Day']/self.Settings['Iteration Time'])
        frames = []
        action = rnd.choice(behavior.actions())
        for minute in range(whole_day):            
            self.Minute = minute
            frame = self.show_world(action)
            frames.append(frame)

        return frames

class Behavior:
    
    def __init__ (self,world,freedom_level=0):
        self.world = world
        self.places = world.current_map.places
        self.families = {
                home:[individual for individual in self.world.people if individual.home==home]
                for home in world.homes}
        self.freedom_level=freedom_level

    def actions(self):
        
        acts= [
                self.stay_at_home,
                self.one_person_per_family,
                self.from_9_18,
                self.go_anywhere]
        return acts[:self.freedom_level]
   
    def go_anywhere(self,person):
        min_p = min([p for p in self.places])
        max_p = max([p for p in self.places])
        rand_plc = randint(min_p,max_p)
        return self.places[rand_plc]
        
    def from_9_18 (self,person):
        current_hour = 9+math.floor(self.world.Minute/self.world.world_hour_minutes)
        if current_hour<9 or current_hour>18:
            return self.stay_at_home(person)
        else:
            return self.go_anywhere(person)
        
    def one_person_per_family (self,person):
        if person==self.families[person.home][0] and len(self.families[person.home])>1:
            return self.go_anywhere(person)
        else:
            return self.stay_at_home(person)
        
    def stay_at_home(self,person):
        return person.home
        
        
