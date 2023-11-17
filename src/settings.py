from pysettings import tk
from constants import STYLE_GROUP as SG

class Config:
    pass




class SettingsGUI(tk.Dialog):
    def __init__(self, master):
        super().__init__(master, SG)
        self.setTitle("SkyBlockTools-Settings")
        self.setMinSize(400, 400)

        self.notebook = tk.Notebook(self, SG)
        self.generalTab = self.notebook.createNewTab("General", SG)
        self.constTab = self.notebook.createNewTab("Constants", SG)
        self.notebook.placeRelative()





        self.show()


    @staticmethod
    def openSettings(master):
        SettingsGUI(master)