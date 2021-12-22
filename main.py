import os
import wx

class PhotoLabel(wx.App):
    
    c1 = wx.Point(-1,-1)
    c2 = wx.Point(-1,-1)
    
    def __init__(self, redirect=False, filename=None):
        self.path = "/home/user/Desktop/aEffacer/0003"
        self.liste = []
        self.listeName = []
        self.size = 0
        self.n = 0
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Label')
                          
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 640
        self.start()
        self.createWidgets()
        self.frame.Show()
        self.onView()
        
    def start(self):
        print("kkkkkkkkk")
        for (root_, dirs, files) in os.walk(self.path):
            if files:
                for file_ in files:
                    img_path = os.path.join(self.path, file_)
                    self.listeName.append(file_)
        self.listeName.sort()
        for imgName in self.listeName:
            img_path = os.path.join(self.path, imgName)
            self.liste.append(img_path)
        self.size = len(self.liste)
        
    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.EmptyImage(640,640)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Creation des boutons
        self.sizerA = wx.BoxSizer(wx.HORIZONTAL)
        btn_previous = wx.Button(self.panel, label='Previous')
        btn_next = wx.Button(self.panel, label='Next')
        self.sizerA.Add(btn_previous, 0, wx.ALL, 5)
        self.sizerA.Add(btn_next, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizerA, 0, wx.ALL, 5)
        
        # Ajout de l'image
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

        # Ajout de la liste
        self.sizerB = wx.BoxSizer(wx.HORIZONTAL)
        self.position = wx.StaticText(self.panel,label="rrrrrrrr")
        btn_clipboard = wx.Button(self.panel, label="Copy clipboard")
        self.sizerB.Add(self.position, 1000, wx.ALL | wx.EXPAND, 5)
        self.sizerB.Add(btn_clipboard, 0, wx.ALIGN_RIGHT,5)
        self.mainSizer.Add(self.sizerB,0,wx.ALL | wx.EXPAND,5)
        
        #Formate la page principale
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.ALL|wx.EXPAND, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
        
        #Event
        btn_next.Bind(wx.EVT_BUTTON, lambda e: self.onChange(e,1))
        btn_previous.Bind(wx.EVT_BUTTON, lambda e: self.onChange(e,-1))
        btn_clipboard.Bind(wx.EVT_BUTTON, lambda e: self.onCopyClipboard(e))
        self.imageCtrl.Bind(wx.EVT_MOTION, self.onMouseMove)
        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.imageCtrl.Bind(wx.EVT_LEFT_UP, self.onMouseUp)
        self.panel.Bind(wx.EVT_PAINT, self.onPaint)
        
    def onCopyClipboard(self,e):
        print("lkkk")
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.position.GetLabel()))
            wx.TheClipboard.Close()

        
    def onChange(self,ev,delta):
        self.n += delta
        if self.n<0:
            self.n = 0
        if self.n==self.size:
            self.n=self.size-1
        self.frame.SetTitle("Photo Label - "+str(self.n+1)+"/"+ str(self.size) + " - "+self.listeName[self.n])
        # Réinitialise les valeurs
        self.c2 = wx.Point(-1,-1)
        self.position.SetLabel("")
        # Actualise la vue
        self.onView()

    def onView(self):
        filepath = self.liste[self.n]
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if False:
            # Ajuste l'image à la fenetre
            if W > H:
                NewW = self.PhotoMaxSize
                NewH = self.PhotoMaxSize * H / W
            else:
                NewH = self.PhotoMaxSize
                NewW = self.PhotoMaxSize * W / H
            img = img.Scale(NewW,NewH)
        # Ajuste la taille de la fenetre à la nouvelle image
        size = self.frame.GetSize() 
        frame_w = max(W+10,size.GetWidth())
        frame_h = max(H+145,size.GetHeight())
        self.frame.SetSize(wx.Size(frame_w,frame_h))
        # Update l'image
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.panel.Layout()
        self.panel.Refresh()
        
    def onMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.c2 = event.GetPosition()
            self.panel.Refresh()

    def onMouseDown(self, event):
        self.c1 = event.GetPosition()
        self.c2 = wx.Point(-1,-1)
        self.position.SetLabel("")
        self.onPaint(None)

    def onMouseUp(self, event):
        self.panel.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        #self.Destroy()
        
    def onPaint(self, event):
        global selectionOffset, selectionSize
        img = wx.Bitmap(self.liste[self.n])
        if self.c2.x!=-1 : 
            dc = wx.MemoryDC(img)
            dc.SetPen(wx.Pen('red', 1))
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), wx.TRANSPARENT))
            dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)
            cx=(self.c1.x+self.c2.x)/(2*640)
            cy=(self.c1.y+self.c2.y)/(2*640)
            lx=abs(self.c1.x-self.c2.x)/(640)
            ly=abs(self.c1.y-self.c2.y)/(640)
            self.position.SetLabel("xxxx "+str(cx)+" "+str(cy)+" "+str(lx)+" "+str(ly))
        self.imageCtrl.SetBitmap(img)
        #selectionOffset = str(self.c1.x) + "x" + str(self.c1.y)
        #selectionSize = str(abs(self.c2.x - self.c1.x)) + "x" + str(abs(self.c2.y - self.c1.y))
        
if __name__ == '__main__':
    app = PhotoLabel()
    app.MainLoop()