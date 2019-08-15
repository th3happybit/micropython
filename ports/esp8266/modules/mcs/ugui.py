from time import sleep_ms
from mcs.ili9341 import color565

class EditText:
    def __init__(self, text, x, y, display, width=100, focus=False, padding=4, color=0xffff, background=color565(0x52, 0x52, 0x52), enabled=True, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.display = display
        self.padding = padding
        self.color = color
        self.background = background
        self.enabled = enabled
        self.textwidthp = len(self.text) * 8
        self.buttonWidth = self.textwidthp + self.padding * 2
        self.buttonHeight = 8 + self.padding * 2
        self.realX = self.x - int(self.textwidthp/2) + self.padding
        self.realY = self.y - self.padding - 4
        self.action = action
        self.focus = False
        self.width = width

    def draw(self):
        if (len(self.text) * 8) < self.width - 8:
            self.display.fill_rectangle(self.realX, self.realY, self.width, self.buttonHeight, self.background)
            self.display.text(self.text, self.realX + self.padding, self.realY + self.padding , self.color, self.background)

    def is_touched(self ,x ,y):
        x = 240 - ((x*240)/480)
        y = (y*320)/264
        if (x >= self.realX) and (x <= (self.realX + self.width)):
            if (y >= self.realY) and (y <= (self.realY + self.buttonHeight)):
                if self.enabled:
                    self.focus = True
                    self.focusEffect()
                    self.focused()
                    return True
        return False

    def focused(self):
        if self.action:
            self.action()

    def focusEffect(self):
        if self.focus and ((len(self.text) * 8) < self.width - 8):
            self.display.fill_rectangle(self.realX-1, self.realY-1, self.width+2, self.buttonHeight+2, color565(0x00, 0x84, 0xf0))
            self.draw()
        else:
            self.draw()

class Screen:
    screens = []
    def __init__(self, name, display, actionbar=None):
        self.name = name
        self.elements = []
        self.display = display
        self.screens.append([self, False])
        self.actionbar = actionbar

    def draw(self):
        for i in range(len(self.screens)):
            if self.screens[i][0].name == self.name:
                self.screens[i][1] = True
            else:
                self.screens[i][1] = False

        self.display.fill(0x0000)
        for element in self.elements:
            if type(element) is not KeyPad:
                element.draw()

    def addElement(self, element):
        self.elements.append(element)

class ActionBar:
    def __init__(self, title, display, button=True, action=None):
        self.title = title
        self.display = display
        self.backAction = action
        if button:
            self.button = Button("<-", 12, 30, display, padding=10, background=color565(0x95, 0x95,0x95), action=self.backAction)
        else:
            self.button = None

    def draw(self):
        self.display.fill_rectangle( 10, 10, 220, 40, 0xffff)
        self.display.text(self.title, 10+int((self.display.width - 10 - len(self.title) * 8)/2), 26, color=0x0000, background=0xffff)
        if self.button:
            self.button.draw()

class TextView:
    def __init__(self, text, x, y, display, padding=4, color=0x0000, background=0xffff):
        self.text = text
        self.x = x
        self.y = y
        self.padding = padding
        self.display = display
        self.color = color
        self.background = background
        self.textwidthp = len(self.text) * 8
        self.textViewWidth = self.textwidthp + self.padding * 2
        self.textViewHeight = 8 + self.padding * 2
        self.realX = self.x - int(self.textwidthp/2) + self.padding
        self.realY = self.y - self.padding - 4

    def draw(self):
        self.display.fill_rectangle(self.realX, self.realY, self.textViewWidth, self.textViewHeight, self.background)
        self.display.text(self.text, self.realX + self.padding, self.realY + self.padding , self.color, self.background)

class TextArea:
    def __init__(self, x, y, display, padding=4, color=0x0000, background=0xffff):
        self.x = x
        self.y = y
        self.display = display
        self.padding = padding
        self.display = display
        self.color = color
        self.background = background
        self.lines = []
        self.linesSpace = 0
        self.maxCharsLine = 20
        self.lineSpace = 20

    def append(self, text):
        texts = self.textFormat(text)
        for lineText in texts:          
            textv = TextView(lineText, self.x, self.y + self.linesSpace, self.display, self.padding, self.color, self.background)
            self.lines.append(textv)
            self.linesSpace += self.lineSpace

    def draw(self):
        maxWidth = 0
        rx = 0
        for textv in self.lines:
            if textv.textViewWidth > maxWidth:
                maxWidth = textv.textViewWidth
                rx = textv.realX
        if len(self.lines) > 0:
            gap = self.lines[0].textViewHeight - self.lineSpace
            self.display.fill_rectangle(rx, self.lines[0].realY, maxWidth, ((self.lines[0].textViewHeight * len(self.lines)) - (gap*len(self.lines))) + int(self.lineSpace/2), self.background)
        for textv in self.lines:
            textv.draw()

    def textFormat(self, text):
        lines = []
        if len(text) > self.maxCharsLine:
            loops = int(len(text)/ self.maxCharsLine) + 2
            j = 0
            for i in range(1,loops):
                lines.append(text[j:self.maxCharsLine * i])
                j += self.maxCharsLine
            if len(text) > j:
                lines.append(text[j:len(text)])
        else:
            lines.append(text)
        return lines

class Button:
    def __init__(self, name, x, y, display, padding=4, action=None, color=0x0000, background=0xffff, enabled=True):
        self.name = name
        self.x = x
        self.y = y
        self.padding = padding
        self.display = display
        self.color = color
        self.background = background
        self.action = action
        self.enabled = enabled
        self.namewidthp = len(self.name) * 8
        self.buttonWidth = self.namewidthp + self.padding * 2
        self.buttonHeight = 8 + self.padding * 2
        self.realX = self.x - int(self.namewidthp/2) + self.padding
        self.realY = self.y - self.padding - 4

    def draw(self):
        self.display.fill_rectangle(self.realX, self.realY, self.buttonWidth, self.buttonHeight, self.background)
        self.display.text(self.name, self.realX + self.padding, self.realY + self.padding , self.color, self.background)

    def is_touched(self ,x ,y):
        x = 240 - ((x*240)/480)
        y = (y*320)/264
        if (x >= self.realX) and (x <= (self.realX + self.buttonWidth)):
            if (y >= self.realY) and (y <= (self.realY + self.buttonHeight)):
                if self.action:
                    if self.enabled:
                        self.clickedEffet()
                        self.action()
                return True
        return False

    def enable(self, boolVal):
        self.enabled = boolVal

    def clickedEffet(self):
        self.background = color565(0x22, 0x81, 0xf3)
        self.color = 0xffff
        self.draw()
        sleep_ms(20)
        self.background = 0xffff
        self.color = 0x0000
        self.draw()

class List:
    def __init__(self, name, x, y, display,width=150, padding=10, color=0x0000, background=0xffff):
        self.name = name
        self.items = []
        self.selectedItem = None
        self.x = x
        self.y = y
        self.display = display
        self.padding = padding
        self.color = color
        self.background = background
        self.width = width
        self.realX = self.x - int(self.width/2) + self.padding
        self.realY = self.y - self.padding - 4
        self.itemsSpace = 0
        self.start = 0
        self.end = 0

    def scrollUp(self):
        self.itemsSpace = 0
        if (self.start < len(self.items)) and (self.end < len(self.items)):
            self.start += 1
            self.end += 1
            self.draw()

    def scrollDown(self):
        self.itemsSpace = 0
        if (self.start > 0) and (self.end > self.getItemNumber()):
                self.start -= 1
                self.end -= 1
                self.draw()

    def append(self, item):
        item.display = self.display
        self.items.append(item)

    def draw(self):
        if len(self.items) > self.getItemNumber():
            self.display.fill_rectangle(self.realX, self.realY, self.width, (self.items[0].itemHeight + 4) * self.getItemNumber(), self.background)
        else:
            self.display.fill_rectangle(self.realX, self.realY, self.width, (self.items[0].itemHeight + 4) * len(self.items), self.background)
        if len(self.items) < self.getItemNumber():
            for item in self.items:
                item.draw(self.realX, self.realY + self.itemsSpace, self.width)
                self.itemsSpace += item.itemHeight + 2
        else:
            if self.end == 0:
                self.end = self.getItemNumber()
            for i in range(self.start,self.end):
                self.items[i].draw(self.realX, self.realY + self.itemsSpace, self.width)
                self.itemsSpace += self.items[i].itemHeight + 2

    def check_selected(self, value):
        if len(self.items) < self.getItemNumber():
            for item in self.items:
                if item.is_selected(value[0], value[1]):
                    self.selectedItem = item
                    return self.selectedItem.title
        else:
            for i in range(self.start, self.end):
                if self.items[i].is_selected(value[0], value[1]):
                    self.selectedItem = self.items[i]
                    return self.selectedItem.title

    def getItemNumber(self):
        if len(self.items) > 0:
            listTall = 320 - self.y
            number = int(listTall/self.items[0].itemHeight)
            return number
        else:
            return 0

    def init(self):
        self.items = []
        self.itemsSpace = 0

class ListItem:
    def __init__(self, title, display=None, padding=8, action=None):
        self.title = title[:25]
        self.padding = padding
        self.display = display
        self.titlewidthp = len(self.title) * 8
        self.itemWidth = self.titlewidthp + self.padding * 2
        self.itemHeight = 8 + self.padding * 2
        self.width = self.itemWidth
        self.realX = None
        self.realY = None

    def draw(self, realX, realY, width, color=color565(0x95, 0x95,0x95)):
        self.realX = realX
        self.realY = realY
        self.width = width
        self.display.fill_rectangle(realX+2, realY+2, width-4, self.itemHeight, color)
        self.display.text(self.title, realX+ 2 + self.padding, realY +2 + self.padding , color=0x0000, background=color)

    def is_selected(self ,x ,y):
        x = 240 - ((x*240)/480)
        y = (y*320)/264
        if self.realX and self.realY:
            if (x >= self.realX+2) and (x <= (self.realX + self.width)):
                if (y >= self.realY+2) and (y <= (self.realY + self.itemHeight)):
                    self.selectedEffect()
                    return True
        return False

    def selectedEffect(self):
        self.draw(self.realX, self.realY, self.width, color565(0x22, 0x81, 0xf3))
        sleep_ms(20)
        self.draw(self.realX, self.realY, self.width, color565(0x95, 0x95,0x95))

class GridLayout:
    def __init__(self, x, y, xr, yr, display, width=230):
        self.x = x
        self.y = y
        self.xr = xr
        self.yr = yr
        self.display = display
        self.elements = []
        self.width = width
        self.realX = self.x - int(self.width/2)
        self.realY = self.y - 4
        self.matrix = []

    def append(self, element):
        self.elements.append(element)

    def draw(self):
        width = int(self.width/self.xr)
        position = int(self.width/(self.xr * 2))
        elms = self.elements[:]
        elms.reverse()
        for x in range(self.xr):
            vl = List(str(x), position+x*2*position, self.realY, self.display, width=width)
            for y in range(self.yr):
                element = elms.pop()
                if element:
                    item = ListItem(element)
                    vl.append(item)
                else:
                    break
            vl.draw()
            self.matrix.append(vl)

class KeyPad:
    def __init__(self, display, action=None, enabled=True):
        self.display = display
        self.gridl = GridLayout(105, 225, 3, 4, display)
        self.gridl.append("1")
        self.gridl.append("4")
        self.gridl.append("7")
        self.gridl.append("OK")
        self.gridl.append("2")
        self.gridl.append("5")
        self.gridl.append("8")
        self.gridl.append("0")
        self.gridl.append("3")
        self.gridl.append("6")
        self.gridl.append("9")
        self.gridl.append("DEL")
        self.typedText = ""
        self.action = action
        self.enabled = enabled

    def draw(self):
        self.gridl.draw()

    def show(self):
        self.enabled = True
        self.draw()

    def hide(self):
        if self.action:
            self.enabled = False
            self.action()

    def is_typed(self, value):
        if self.enabled:
            for lst in self.gridl.matrix:
                val = lst.check_selected(value)
                if val:
                    if val=="DEL":
                        self.typedText = self.typedText[:len(self.typedText)-1]
                    elif val=="OK":
                        self.hide()
                    else:
                        self.typedText += val
    