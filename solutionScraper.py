# -*- coding: utf-8 -*-
"""
@author: C-3PBro

"""

#%% Imports
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

#%% Classes
# Class for processing the website with Selenium
class SEI_Selenium():
    # Website object is initialized
    def __init__(self):
        self.soup = self.callAndPrepareSEIQuiz()
        self.start = self.getStart()
        self.obstacles = self.getObstacles()
        self.letters = self.getLetters()        
        
    def callAndPrepareSEIQuiz(self):
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
        self.driver.get('http://www.holdirdeinenvertrag.de/')
        return BeautifulSoup(self.driver.page_source, "html.parser")
        
    # Methods for retrieving Start, Obstacles and Letters
    def getStart(self):
        self.start = [re.sub("[^0-9]","",str(self.soup.find_all('p')[-2]).splitlines()[1]).split()[0][0],re.sub("[^0-9]","",str(self.soup.find_all('p')[-2]).splitlines()[1]).split()[0][1]]
        return [float(x) for x in self.start]
    def getObstacles(self):
        self.obst = [re.sub("[^0-9]","",str(self.soup.find_all('p')[-2]).splitlines()[3])]
        self.obst_list = []
        for i in range(0,11,2):
            self.obst_list.append([float(self.obst[0][i]),float(self.obst[0][i+1])])
        return self.obst_list
    def getLetters(self):
        self.let = [re.sub("[^0-9]","",str(self.soup.find_all('p')[-2]).splitlines()[2])]
        self.let_list = []
        for i in range(0,9,2):
            self.let_list.append([float(self.let[0][i]),float(self.let[0][i+1])])
        return self.let_list

# SEI solver class   
class SEI_quiz(SEI_Selenium):
    # Start is is initialized using the SEI_Selenium class
    def __init__(self):
        self.instance = SEI_Selenium()
        self.start = self.instance.start
        self.driver = self.instance.driver
        self.move(self.start[0], self.start[1])
        self.currentPosition = [self.x,self.y]
        
        # Define all forbidden positions including the space outside and already
        # visited positions:
        
        # Borders:
        self.outside = []
        for i in range(0,7):
            self.outside.append([-1,i]) # left border
            self.outside.append([7,i])  # right border
            self.outside.append([i,-1]) # top border
            self.outside.append([i,7])  # bottom border
            
        # Obstacles:
        self.obstacles = self.instance.obstacles
        
        # Visited areas:
        self.visited = []
        
        # Input letters:
        self.letters = self.instance.letters
        self.letter_dict = {'L':self.letters[0],
                            'A':self.letters[1],
                            'I':self.letters[2],
                            'O':self.letters[3],
                            'S':self.letters[4]
                            }
        # Container of collected letters:
        self.collection = []
    
    # Concatenates letters in self.collection
    def solution(self):
        try:
            if len(self.collection) == 0:
                print("Execute moveIter method to get a solution!")
            elif len(self.collection) >= 1:
                self.solution = ''.join(self.collection)
                print(self.solution)
            else:
                print("Ooops! Something went wrong.")
        except:
            pass
    
    def getLetter(self,x,y):
        try:
            return list(self.letter_dict.keys())[list(self.letter_dict.values()).index([x,y])]
        except:
            pass
    
    # New x- and y-coordinates are assigned to the point. If no coordinates are
    # supplied to the method, random values are generated.
    def move(self, x, y):
        self.x = x
        self.y = y
        
    def reset(self):
        self.move(0, 0)
    
    # Algorithm for solving the maze.
    def moveIter(self,x,y):        
        self.move(x,y)
        
        # Check if position is good or not good:
        if [x,y] in self.outside or [x,y] in self.obstacles or [x,y] in self.visited:
            return
        
        # Check if position has letter. If so, letter is printed:
        self.collection.append(self.getLetter(x,y))
        self.collection = [x for x in self.collection if x is not None]
        self.visited.append([x,y])
        
        # The algorithm as depicted in 'https://www.holdirdeinenvertrag.de/':
        self.moveIter(x+1,y)           # go to right
        self.moveIter(x,y+1)           # go to down
        self.moveIter(x-1,y)           # go to left
        self.moveIter(x,y-1)           # go to up   
        
    def callSolutionPage(self,solution):
        self.solutionInputField = self.driver.find_element_by_id('input-solution')
        self.solutionInputField.send_keys(solution)
        self.solutionInputField.submit()


#%% Main
if __name__ == '__main__':
    # Scraping data
    solutions = np.asarray([])
    for i in range(100):
        person = SEI_quiz()
        person.moveIter(person.start[0],person.start[1])
        person.solution()
        time.sleep(1)
        solutions = np.concatenate((solutions,person.solution), axis=None)
        person.driver.quit()
        print('Iteration '+ str(i+1) +' done!')

    # Save data
    solutions2DataFrame = pd.DataFrame(solutions)
    fileList = glob.glob('*.csv')
    if fileList.count('scrapedSolutionData.csv') >= 1:
        print('Append scraped solutions to solution file...')
        dataFrame = pd.read_pickle('scrapedSolutionData.csv')
        dataFrame = dataFrame.append(solutions2DataFrame, ignore_index=True)
        dataFrame.to_pickle('scrapedSolutionData.csv')
    else:
        print('Creating solution file...')
        print('Append scraped solutions to solution file...')
        solutions2DataFrame.to_pickle('scrapedSolutionData.csv')
    
    # Plotting data in a histogram
    solutionsDataFrame = pd.read_pickle('scrapedSolutionData.csv')
    solutionsDataFrame.columns = ['Solutions']
    solutionArray = np.asarray(solutionsDataFrame['Solutions']).astype('<U32')
    with plt.style.context(('seaborn')):
        plt.figure(figsize=[16,9])
        bins = np.arange(len(np.unique(solutionArray))+1)-0.5
        plt.hist(solutionArray, bins, width=0.95, edgecolor='black',linewidth=1.2)
        plt.xticks(rotation=90)
        plt.title(r'\textbf{Frequency of different solutions}'
                  + '\nTotal trials: ' + str(len(solutionArray))
                  + '\nNumber of different solutions: ' + str(len(np.unique(solutionArray))))
    
    









