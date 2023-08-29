# structure is: "COMMAND: (INFO, ARGS)"

cmds = {
# base
"help": ("prints help", "help"),
"exit": ("quit editor, same as Ctrl+C", "exit"),
"unload": ("like restarting editor but keep settings", "unload"),
# projects
"new": ("create new project", "NAME"),
"save": ("save current project with name given when creating", ""),
"load": ("load project from file", "PATH"),
"reload": ("discard changes in current project, and load it back from saved file", ""),
# visual
"hrf": ("show patterns in human readable format", ""),
"values": ("like hrf but only show play ranges", ""),
# changing project data
"tempo": ("show or set tempo", "[VALUE]"),
"rn": ("show or set root note, default i C4 (3)", "[INT]"),
# changing pattern data
"len": ("show or set len of pattern play range", "[VALUE(FROM 1 TO 64)]"),
"ofs": ("set play range offset", "VALUE"),
"plo": ("set index of first note in play range", "VALUE(FROM 0 TO PLAY_RANGE_LEN)"),
"lock": ("lock selected pattern", ""),
"unlock": ("allow wrting to selected pattern", ""),
"mute": ("mute selected pattern", ""),
"unmute": ("unmute selected pattern", ""),
"shf": ("shif every note in selected pattern", "VALUE"),
"cpv": ("copy values of selected pattern to other", "ID_OF_DESTINATION_PATTERN"),
# patterns
"ap": ("add new pattern", ""),
"rp": ("remove selected pattern", ""),
# things i have no idea how to name this category
"go": ("set cursor in place you want", "PATTERN_ID NOTE"), # TODO: CHANGE THIS BECAUSE ITS HARD TO UNDERSTAND
"chrd": ("place chord (and change next patterns too so use it carefully), with root note being note in place where you are", "maj/min/pow")
}

settings = {
# hrf/values
"hv": "change if editor should display all values in all patterns or only values in ranges that will be played by player",
"am": "after setting value move cursor automaticly"
}

prefixes = {
"/": "before commands",
"%": "before config"
}

ENAME = "XeTrEditor:"                                   # base command input text (no project name)
USAGE = "ARGS:"                                         # what to print before saying usage of command (when command used wrong)
NPY = "you arent editing any project yet"               # error message when you dont have loaded project
POOR = "probably pattern id is too big"                 # error when trying to access pattern out of range
LK = "this pattern is locked, use unlock on it first"   # when trying to write to locked pattern
IC = "invalid command"                                  # when cmd cant match any commands
OD = "this project may be too old aleady, try older version of program" # when i make too much changes and projects arent compatible
CHRDNF = "chord not found"                              # well, when chord not found
NPM = "you need more patterns in project to do that"    # when for example you want to do "chrd 0 0 min" which needs to set 3 notes, but you only have 2 channels
VI = "VALUE:"                                           # asked for example in .edit command
IU = "invalid usage"                                    # when IndexError in exc

def areYouSure():
    try:
        while True:
            match input("are you sure? [Y/n]").lower():
                case "y":
                    return True
                case "n":
                    return False
                case _:
                    pass
    except EOFError:
        return false
