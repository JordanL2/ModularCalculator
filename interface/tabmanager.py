#!/usr/bin/python3


class TabManager():

    def __init__(self, interface):
        self.interface = interface
        self.entry = self.interface.entry
        self.display = self.interface.display
        self.tabs = []
        self.tabbar = self.interface.tabbar
        self.filemanager = self.interface.filemanager
        self.selectedTab = None


    def restoreTabs(self):
        self.tabs = self.interface.fetchStateArray("tabs")
        if len(self.tabs) > 0:
            for tab in self.tabs:
                tabfile = self.getTabName(tab['currentFile'], tab['currentFileModified'])
                self.tabbar.addTab(tabfile)
            self.selectedTab = self.interface.fetchStateNumber("selectedTab")
            if self.selectedTab is None:
                self.loadTab(0)
            else:
                self.loadTab(self.selectedTab)
        else:
            self.addTab()
            self.loadTab(0)
        self.interface.tabbar.currentChanged.connect(self.selectTab)
        self.interface.tabbar.tabCloseRequested.connect(self.closeTab)
        self.interface.tabbar.tabMoved.connect(self.moveTab)


    def getTabName(self, currentFile, currentFileModified):
        if currentFile is None:
            return '(untitled)'
        tabName = currentFile
        if currentFileModified:
            tabName += ' *'
        return tabName

    def addTab(self):
        self.tabs.append({
            'entry': {}, 
            'display': {'rawOutput': []}, 
            'currentFile': None, 
            'currentFileModified': False
        })
        self.tabbar.addTab(self.getTabName(None, None))
        self.tabbar.setCurrentIndex(len(self.tabs) - 1)

    def storeSelectedTab(self):
        if self.selectedTab is not None:
            i = self.selectedTab
            self.tabs[i]['entry'] = self.entry.saveState()
            self.tabs[i]['display'] = self.display.saveState()

    def selectTab(self, i):
        self.storeSelectedTab()
        self.loadTab(i)

    def loadTab(self, i):
        self.selectedTab = i
        self.entry.restoreState(self.tabs[i]['entry'])
        self.display.restoreState(self.tabs[i]['display'])
        self.display.refresh()
        self.filemanager.setCurrentFileAndModified(self.tabs[i]['currentFile'], self.tabs[i]['currentFileModified'])
        if self.tabbar.currentIndex != i:
            self.tabbar.setCurrentIndex(i)

    def closeTab(self, i):
        if self.filemanager.checkIfNeedToSave(i):
            return
        
        self.storeSelectedTab()
        self.tabbar.blockSignals(True)

        self.tabs.pop(i)
        self.tabbar.removeTab(i)
        if self.selectedTab >= i:
            self.selectedTab -= 1
            if self.selectedTab < 0:
                self.selectedTab = 0
            if len(self.tabs) == 0:
                self.addTab()
            self.loadTab(self.selectedTab)

        self.tabbar.blockSignals(False)

    def closeCurrentTab(self):
        self.closeTab(self.selectedTab)

    def previousTab(self):
        i = self.selectedTab
        if i == 0:
            i = len(self.tabs)
        i -= 1
        self.selectTab(i)

    def nextTab(self):
        i = self.selectedTab
        i += 1
        if i == len(self.tabs):
            i = 0
        self.selectTab(i)

    def moveTab(self, toPos, fromPos):
        movedTab = self.tabs.pop(fromPos)
        self.tabs.insert(toPos, movedTab)
        self.selectedTab = toPos