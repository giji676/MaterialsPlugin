# Maya matSelector Plugin Installation Guide

Follow the steps below to install the matSelector plugin for Maya:

## Step 1: Place the Plugin Folder
1. Locate the **matSelector** plugin folder.
2. Move the plugin folder to the following path, replacing `<username>` and `<version>` with your specific details:
`C:\Users\<username>\Documents\maya\<version>\plug-ins\matSelector`
**Note:** If the **plug-ins** folder doesn't exist, create it manually.

## Step 2: Update the `Maya.env` File
1. Open the **Maya.env** file located at:
`C:\Users\<username>\Documents\maya\<version>\Maya.env`
2. Add the following line to the file:
`MAYA_PLUG_IN_PATH = C:\Users\<username>\Documents\maya\<version>\plug-ins\matSelector`
**Note:** If the **Maya.env** file doesn't exist, create it manually.

## Step 3: Enable the Plugin in Maya
1. Open Maya and navigate to the **Plugin Manager**:
- Go to `Windows -> Settings/Preferences -> Plugin Manager`
2. In the Plugin Manager, locate **materialsPlugin.py** and check the following options:
- **Loaded**: Check this box
- **Auto load**: Check this box

## Step 4: Troubleshooting
If **materialsPlugin.py** is not showing up in the Plugin Manager:
1. Click **Browse**
2. Use the file explorer to navigate to the location of `materialsPlugin.py`
3. Select the file and click **Open**

If plugin is not being loaded properly or not showing up in the menu bar:
1. You might have to restart Maya to apply the changes

- The plugin will now be ready for use once loaded and auto-loaded!
