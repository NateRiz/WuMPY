# WuMPY

WuMPY is a Window Manager created in Python3 for snapping windows and launching preset applications in a workspace. 
<p align="center">
   <img src="./Preview/WuMPY.png />
</p>
## Instructions
A workspace contains windows that'll be open on the desktop all at once. For example, a work based workspace may contain an Excel sheet, Spotify, Email, and Zoom.
<br>Workspaces support multiple monitors and are generalizable to different monitor sizes. 
<br><br>Windows Properties:
* X/Y Position - top left position of the window on the desktop. For relative or absolute position, see Pixel Precision.
* Z-index - A window with a higher Z-index will display in front of windows with a lower Z-index. To keep your workspace general to all monitors, you should not use pixel precision.
* Pixel Precision - If enabled, will enable absolute positions and sizes. Otherwise it'll use percentages for relative positions.
* Window Name - Used to determine which window to move.
* Target - If WuMPY couldn't find the window specified by 'Window Name' it'll run this command. Usually just the file location for the window, but can be any command.
* Color - comma separated RGB, purely for organization.

Monitor Properties:
* Monitor Index - Used to override which monitor the workspace will be applied to. There shouldn't be a need to modify this right now as it's automatically set. 
* Add New Window - Add a new window to the selected monitor.
* Delete Window - Delete the selected window.
* Run - Run the program and apply the workspace to your desktop. Can also be run from headless from the command line.

## Usage

```python
# GUI
py main.py

# Headless Auto-run
py main.py my_workspace
```

## Todo
- Create a new Virtual Desktop
- Auto open window and snap after (wait & retry)
- Rename Monitors
- Custom Monitor dimensions
- Regex search for window names
- Auto detect windows on screen to create workspace
- Fix color selector