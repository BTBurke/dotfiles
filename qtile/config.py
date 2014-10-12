from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group

from libqtile.manager import Click, Drag, Screen
from libqtile.config import Match

sup = "mod4"
alt = "mod1"

keys = [
# MONAD TALL KEYBINDINGS
    Key([alt], "j", lazy.layout.down()),
    Key([alt], "k", lazy.layout.up()),
    Key([alt, "shift"], "j", lazy.layout.shuffle_down()),
    Key([alt, "shift"], "k", lazy.layout.shuffle_up()),
    Key([alt], "l", lazy.layout.grow()),
    Key([alt], "h", lazy.layout.shrink()),
    Key([alt], "n", lazy.layout.normalize()),
    
    
# LAYOUT CHANGERS
    # move to next layout in the stack
    Key([alt], "space", lazy.nextlayout()),
    # switch master windows
    Key([alt, "shift"], "space", lazy.layout.rotate()),

# MOVEMENT KEYS
    # windows style alt-tab/alt-shift-tab
    Key([alt], "Tab", lazy.layout.next()),
    Key([alt, "shift"], "Tab", lazy.layout.previous()),

    # kill current window
    Key([alt, "shift"], "c", lazy.window.kill()),

    # dec ratio of current window
    Key([alt], "q", lazy.layout.decrease_ratio()),

    # inc ratio of current window
    Key([alt], "e", lazy.layout.increase_ratio()),

    # cycle to previous group
    Key([sup], "Left", lazy.group.prevgroup()),

    # cycle to next group
    Key([sup], "Right", lazy.group.nextgroup()),

# APPLICATION LAUNCHERS
    Key([alt, "shift"], "Return", lazy.spawn("urxvt")),
    Key([alt, "shift"], "s", lazy.spawn("subl")),
    Key([alt, "shift"], "f", lazy.spawn("firefox")),
    Key([alt, "shift"], "c", lazy.spawn("google-chrome")),
    Key([alt, "shift"], "g", lazy.spawn("gimp")),
    Key([alt, "shift"], "m", lazy.spawn("thunderbird")),
    Key([alt, "shift"], "z", lazy.spawn("zeal")),
    Key([alt, "shift"], "p", lazy.spawncmd()),
    
# AUDIO
    Key([alt], "F11", lazy.spawn("amixer --quiet set Master 1-")),
    Key([alt], "F12", lazy.spawn("amixer --quiet set Master 1+")),
    Key([alt], "F4",  lazy.spawn("ncmpcpp prev")),
    Key([alt], "F5",  lazy.spawn("ncmpcpp pause")),
    Key([alt], "F6",  lazy.spawn("amixer --quiet set Master mute")),
    Key([alt], "F7",  lazy.spawn("amixer --quiet set Master unmute")),
    Key([alt], "F8",  lazy.spawn("ncmpcpp play")),
    Key([alt], "F9",  lazy.spawn("ncmpcpp next")),

# PRINT SCREEN
    Key([alt], "F10", lazy.spawn("import -window root ~/screenshot.png")),

# CHANGE WALLPAPER
    #Key([alt], "F1", lazy.spawn("wallpaperchanger -timeout 1 -folder /storage/Users/Skynet/Pictures/Wallpaper/")),

# BASE COMMANDS
    # shutdown
    Key([alt, "shift"], "q", lazy.shutdown()),
    # restart qtile
    Key([alt, "shift"], "r", lazy.restart()),
    # toggle floating
    Key([alt], "t", lazy.window.toggle_floating()),
]

mouse = [
    Drag([alt], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([alt], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([alt], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group position to generate
# a key binding for it.

groups = [
     Group('1-web', layout='max', matches=[Match(wm_class=["Firefox"])]),
     Group('2-code', layout='xmonad-tall', matches=[Match(wm_class=["Sublime Text"])]),
     Group('3-docs', layout='stack', matches=[Match(wm_class=["Zeal"])]),
     Group('4-mail', layout='max', matches=[Match(wm_class=["Thunderbird"])]),
     Group('5'),
     Group('6'),
     Group('7')
]



#groups = [Group(name, **kwargs) for name, kwargs in group_names]


for index, grp in enumerate(groups):

     # index is the position in the group list grp is the group object.
     # We assign each group object a set of keys based on it's
     # position in the list.

     # Eventually we will implement a function to change the name based
     # on what window is active in that group.

     keys.extend([

             # switch to group
         Key([alt], str(index+1), lazy.group[grp.name].toscreen()),

             # send to group
         Key([alt, "shift"], str(index+1), lazy.window.togroup(grp.name)),

             # swap with group
         Key([sup, "shift"], str(index+1), lazy.group.swap_groups(grp.name))
    ])


# Three simple layout instances:

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Tile(ratio=0.50, masterWindows=2),
    layout.xmonad.MonadTall(ratio=0.60),
]


# orange text on grey background
default_data = dict(fontsize=12,
                    foreground="FF6600",
                    background="1D1D1D",
                    font="ttf-droid")

# we need a screen or else qtile won't load
screens = [
    Screen(bottom = bar.Bar([widget.GroupBox(**default_data),
                             widget.Prompt(),
                             widget.TaskList(highlight_method="block", borderwidth=0, **default_data),
                             widget.Systray(),
                             widget.TextBox('CPU:', name="cpu", **default_data),
                             widget.CPUGraph(),
                             widget.TextBox('Mem:', name="mem", **default_data),
                             widget.MemoryGraph(),
                             widget.TextBox('Net:', name="net", **default_data),
                             widget.NetGraph(),
                             widget.CurrentLayout(**default_data),
                             widget.Clock(**default_data)],
                             27,))]

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

@hook.subscribe.client_new
def grouper(window, windows={'firefox': '1-web',
                              'subl': '2-code',
                              'zeal': '3-docs',
                              'thunderbird': '4-mail'}):

     """
     This function relies on the contentious feature of default arguments
     where upon function definition if the argument is a mutable datatype,
     then you are able to mutate the data held within that object.

     Current usage:

     {window_name: group_name}

     or for grouping windows to different groups you will need to have a
     list under the window-key with the order that you're starting the
     apps in.

     See the 'runner()' function for an example of using this method.

     Here:

     {window_name: [group_name1, group_name2]}

     Window name can be found via window.window.get_wm_class()
     """


     windowtype = window.window.get_wm_class()[0]

     # if the window is in our map
     if windowtype in windows.keys():

          # opening terminal applications gives
          # the window title the same name, this
          # means that we need to treat these apps
          # differently

          if windowtype != 'urxvt':
               window.togroup(windows[windowtype])
               windows.pop(windowtype)

          # if it's not on our special list,
          # we send it to the group and pop
          # that entry out the map
          else:
               try:
                    window.togroup(windows[windowtype][0])
                    windows[windowtype].pop(0)
               except IndexError:
                    pass


@hook.subscribe.startup
def runner():
     import subprocess

     """
     Run after qtile is started
     """

     # startup-script is simple a list of programs to run
     #subprocess.Popen('startup-script')

     # terminal programs behave weird with regards to window titles
     # we open them separately and in a defined order so that the
     # client_new hook has time to group them by the window title
     # as the window title for them is the same when they open

     #subprocess.Popen(['urxvt', '-e', 'ncmpcpp-opener'])
     #subprocess.Popen(['urxvt', '-e', 'weechat-curses'])