import sublime
import sublime_plugin
import subprocess
import os
import re

# Utility function to set R version in SublimeStudio.sublime-settings
class RSwitch(sublime_plugin.WindowCommand):
    # partially stolen from R-Box
    def show_quick_panel(self, options, done):
        sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

    def run(self):
        if sublime.platform() == 'osx':
            self.app_list = ["R", "Terminal"]
            pop_string = ["3.1.2 64bit", "Bash"]
        elif sublime.platform() == "windows":
            self.app_list = ["R-2", "R-3", "S Plus", "Terminal"]
            pop_string = ["2.15.3 64bit", "3.1.2 64bit", "S+ 8.2.0", "Command Prompt"]
        else:
            sublime.error_message("Platform not supported!")
        self.show_quick_panel([list(z) for z in zip(self.app_list, pop_string)], self.on_done)

    def on_done(self, action):
        if action == -1: return
        settings = sublime.load_settings('SublimeStudio.sublime-settings')
        settings.set('App', self.app_list[action])
        sublime.save_settings('SublimeStudio.sublime-settings')

# Subfunction to run a command in the sepcified version of R
# (will be used by the functions below)
def r_cmd(r_string):
    # partially stolen from R-Box
    if (sublime.platform() == "osx"):
        App = sublime.load_settings('SublimeStudio.sublime-settings').get("App")
        if (App == 'R'):
            r_string = r_string.replace('\"', '\\"')
            args = ['osascript', '-e']
            args.extend(['tell app "R" to cmd "' + r_string + '"'])
            subprocess.Popen(args)
        if (App == 'Terminal'):
            sublime.status_message("TODO: remove the final newline")
            r_string = r_string.replace('\"', '\\"')
            args = ['osascript', '-e']
            args.extend(['tell app "Terminal" to do script  "' + r_string + '" in front window'])
            subprocess.Popen(args)
        return
    elif (sublime.platform() == "windows"):
        ahk_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','AutoHotkeyU32')
       
        # manually add "\n" to keep the indentation of first line of block code,
        # "\n" is later removed in AutoHotkey script
        r_string = "\n" + r_string  
        
        App = sublime.load_settings('SublimeStudio.sublime-settings').get("App")

        if (App == 'R-3'):
            r_path = sublime.load_settings('SublimeStudio.sublime-settings').get("r3")
            ahk_script_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','Rgui.ahk')
        if (App == 'R-2'):
            r_path = sublime.load_settings('SublimeStudio.sublime-settings').get("r2")
            ahk_script_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','Rgui.ahk')
        if (App == 'S Plus'):
            r_path = sublime.load_settings('SublimeStudio.sublime-settings').get("splus")
            ahk_script_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','Sp.ahk')
        if (App == 'Terminal'):
            r_path = sublime.load_settings('SublimeStudio.sublime-settings').get("terminal")
            ahk_script_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','Terminal.ahk')

        args = [ahk_path, ahk_script_path, r_path, r_string]
        subprocess.Popen(args)
        return
    else:
        sublime.message_dialog("platform not supported :-(")


# run line, block or selected command
class RRunCommand(sublime_plugin.TextCommand):
    # stolen from R-Box
    # expand selection to {...} when being triggered
    def expand_sel(self, sel):
        esel = self.view.find(r"""^(?:.*(\{(?:(["\'])(?:[^\\]|\\.)*?\2|#.*$|[^\{\}]|(?1))*\})[^\{\}\n]*)+"""
            , self.view.line(sel).begin())
        if self.view.line(sel).begin() == esel.begin():
            return esel
    def run(self, edit):
        view = self.view
        cmd = ''
        for sel in [s for s in view.sel()]:
            if sel.empty():
                thiscmd = view.substr(view.line(sel))
                line = view.rowcol(sel.end())[0]
                # if the line ends with {, expand to {...}
                if re.match(r".*\{\s*$", thiscmd):
                    esel = self.expand_sel(sel)
                    if esel:
                        thiscmd = view.substr(esel)
                        line = view.rowcol(esel.end())[0]
            else:
                thiscmd = view.substr(sel)
            cmd += thiscmd +'\n'
        r_cmd(cmd)


# help on a selected topic
class RHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        r_cmd("?" + self.view.substr(sel[0]))


# reload chrome (useful for debugging shiny)
# (package Browser Refresh is a heavy alternative for this)
class RReloadChrome(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command("save")  
        if (sublime.platform() == "osx"):
            args = ['osascript']
            args.extend(['-e', 'tell application "Google Chrome" to tell the active tab of its first window'])
            args.extend(['-e', 'reload'])
            args.extend(['-e', 'end tell'])
            subprocess.Popen(args)
        else:
            ahk_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','AutoHotkeyU32')
            ahk_script_path = os.path.join(sublime.packages_path(), 'SublimeStudio', 'bin','ReloadChrome.ahk')
            args = [ahk_path, ahk_script_path]
            subprocess.Popen(args)


# sent Q to quit browser()
class RQuit(sublime_plugin.WindowCommand):
    def run(self): 
        r_cmd('Q')  


# devtools::load_all
class RLoadAllCommand(sublime_plugin.WindowCommand):
    def run(self):
        if 'gRDir' not in globals():
            global gRDir
            gRDir = "."
        if 'gRBuffer' not in globals():
            global gRBuffer
            gRBuffer = " "

        self.window.run_command("save")   
        s = 'devtools::load_all(\"' + gRDir + '\"); ' + gRBuffer
        r_cmd(s)
      

# the following commands are infrequently used and would be nicer in a menu
# the menu should contain all commands an also show the shortkey

# devtools::document
class RDocumentCommand(sublime_plugin.WindowCommand):
    def run(self):
        s = ('devtools::document(\"' + gRDir + '\", roclets=c(\"rd\", \"collate\", \"namespace\"))')
        r_cmd(s)


# build and reload
class RBuildAndReloadCommand(sublime_plugin.WindowCommand):
    def run(self):
        s = ('pth <- \"' + gRDir + '\"; pk <- basename(pth);system(paste(\'R CMD INSTALL\', pth));if (pk %in% names(sessionInfo()$otherPkgs)){detach(name = paste0(\'package:\', pk), unload = TRUE, character.only = TRUE)}; library(pk, character.only = TRUE)')
        r_cmd(s)


# build source package
class RBuildSourcePackage(sublime_plugin.WindowCommand):
    def run(self):
        s = ('system(paste(\'R CMD build\', \"' + gRDir + '\"))')
        r_cmd(s)


# set r path
class RSetDir(sublime_plugin.TextCommand):
    def run(self, edit):
        global gRDir
        path = self.view.file_name()
        # use the package root directory if inside an R package
        path = os.path.dirname(path).replace("/R", "")
        path = path.replace("\\R", "") # windows
        path = path.replace("man", "")
        gRDir = path.replace("\\", "\\\\")
        sublime.status_message("R-directory set to \'" + gRDir + "\'")


# set butter (which is called after load all, useful for debugging)
class RSetBuffer(sublime_plugin.TextCommand):
    def run(self, edit):
        global gRBuffer
        sel = self.view.sel()
        gRBuffer = self.view.substr(sel[0])
        # gRBuffer = sublime.get_clipboard()
        sublime.status_message("R-buffer set to \'" + gRBuffer + "\'")


# run shiny app included in package
class RShiny(sublime_plugin.WindowCommand):
    def run(self):
        s = ('shiny::runApp(\"' + gRDir + '\")')
        r_cmd(s)




