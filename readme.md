place the plugin folder (matSelector) in the following path (replace <...> with your details):
    C:\Users\<user>\Documents\maya\<version>\plug-ins
(if the "plug-ins" folder doesn't exist create it
place the following line:
    MAYA_PLUG_IN_PATH = C:\Users\<user>\Documents\maya\<version>\plug-ins\matSelector
in the following file:
    C:\Users\<user>\Documents\maya\<version>\Maya.env

after that go to "Windows -> Settings/Preferences -> Plug-in Manager" and check "Loaded" and "Auto load" for "materialsPlugin.py"
if "materialsPlugin.py" isn't showing up try the following:
    click "Browse" and select the file from the file explorer, cick "Open"
