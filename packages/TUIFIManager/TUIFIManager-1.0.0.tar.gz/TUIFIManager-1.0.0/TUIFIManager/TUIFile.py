from      unicurses import *
from .TUIFIProfile import *
 
 
 
class TUIFIMenu:    
    def __init__(self,menu_pad,h,w,y,x):
        pass


 
class TUIFile:
    profile = DEFAULT_PROFILE
    #h,w = 4,11 # 10        
    x,y         = 0,0
    name_height = 1  
    is_selected = False
    is_cut      = False # This is pointless for now, until i find a way of efficiently drawing/managing cuted  files 
      
    def chunkStr(self,text, n): # sorry  for this :P
        counter2 = 0
        counter1 = 0
        tempTxT  = ''
        for i in range(0,len(text)):
            counter1 += 1
            tempTxT += text[i]
            if counter1 == n:
                counter2 += 1
                tempTxT  += '\n'
                counter1  = 0
            
        if tempTxT.endswith('\n'):
            counter2 -= 1
            tempTxT   = tempTxT[0:-1]
            
        self.name_height = counter2 + 1
        return tempTxT    
    
                         
    def __init__(self, name, y=0, x=0, profile=DEFAULT_PROFILE, name_color=1, is_link=False):
        assert isinstance(profile, TUIFIProfile),'profile needs to be of type class TUIFIProfile'
        self.name_color  = name_color
        self.profile     = profile
        self.name_color  = name_color
        tempprofileSplit = self.profile.text.split('\n')
        self.y           = y
        self.x           = x
        self.name        = name
        self.is_link     = is_link
        self.chunkStr(name, self.profile.width)


    def clear(self,atpad):
        pass


    def __draw_icon(self, atpad):
        for offY, ln in enumerate((self.profile.text + '\n').split('\n')):
            mvwaddwstr(atpad,offY + self.y,self.x, ln, COLOR_PAIR(self.profile.color_map) )                    
        for offY, ln in enumerate(self.chunkStr(self.name,self.profile.width).split('\n'), offY):
            mvwaddwstr(atpad,offY + self.y,self.x, ln, COLOR_PAIR(self.name_color) ) # A_BOLD | 
        if self.is_link: # no idea why but mvwadd_wch misbehaves ...
            mvwaddwstr(atpad, self.y + self.profile.height -1 , self.x + self.profile.width -1, LINK_SYMBOL, COLOR_PAIR(LINK_SYMBOL_COLOR))  # | A_BOLD

    
    
    def draw(self,atpad, y=None, x=None, redraw_icon=False): #  na valw NEW giati sto resort() xanei to icon kai text h kati tetoio !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if y: self.y = y
        if x: self.x = x
        
        pLINES, pCOLS = getmaxyx(atpad)

        if self.is_selected:
            if redraw_icon:self.__draw_icon(atpad)
            for y in range(self.y, self.y + self.profile.height):
                mvwchgat(atpad,y, self.x, self.profile.width,A_REVERSE,7)             
        elif self.is_cut:
            if redraw_icon:self.__draw_icon(atpad)
            for y in range(self.y, self.y + self.profile.height):
                mvwchgat(atpad,y, self.x, self.profile.width,A_DIM,1)
        else:
            self.__draw_icon(atpad)


