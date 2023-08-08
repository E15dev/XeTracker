# structure COMMAND: (INFO, USAGE)

cmds = {
# base
"help": ("prints help", "help"),
"exit": ("quit editor, same as Ctrl+C", "exit"),
"unload": ("like restarting editor but keep settings", "unload"),
# settings
"auto": ("enable auto visualizing values", "auto"),
"hv": ("in `auto` command change between hrf and values", "hv"),
# projects
"new": ("create new project", "new NAME"),
"save": ("save current project with name given when creating", "save"),
"load": ("load project from file", "load PATH"),
# visual
"hrf": ("show patterns in human readable format", "hrf"),
"values": ("like hrf but only show play ranges", "values"),
# changing project data
"tempo": ("show or set tempo", "tempo [VALUE]"),
"rn": ("show or set root note, default i C4 (3)", "rn [INT]"),
# changing pattern data
"set": ("set value in pattern", "set PATTERN_ID INDEX VALUE"),
"len": ("show or set len of pattern play range", "len [VALUE(FROM 1 TO 64)]"),
"ofs": ("set play range offset", "ofs PATTERN_ID VALUE"),
"plo": ("set index of first note in play range", "plo PATTERN_ID VALUE(FROM 0 TO PLAY_RANGE_LEN)"),
"lock": ("lock pattern from writing to it", "lock PATTERN_ID"),
"unlock": ("unload pattern from writing to it", "unload PATTERN_ID"),
"mute": ("prevent player from playing this pattern", "mute PATTERN_ID"),
"unmute": ("unmute pattern", "unmute PATTERN_ID"),
"shf": ("shif every note in pattern", "shf PATTERN_ID VALUE"),
"cpv": ("copy values of pattern to different one", "cpv ID_OF_FIRST_PATTERN ID_OF_SECOND_PATTERN")
}

ENAME = "XeTrEditor:"                                   # base command input text (no project name)
USAGE = "USAGE:"                                        # what to print before saying usage of command (when command used wrong)
NPY = "you arent editing any project yet"               # error message when you dont have loaded project
POOR = "probably pattern id is too big"                 # error when trying to access pattern out of range
LK = "this pattern is locked, use unlock on it first"   # when trying to write to locked pattern
IC = "invalid command"                                  # when cmd cant match any commands
OD = "project may be too old aleady, try older editor"  # when i make too much changes and projects aren compatible

