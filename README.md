[![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)


# RStudio Experience in a Real Editor

A Sublime Text plug-in that tries to bring parts of the user experience of
RStudio to Sublime Text. It is primarily designed to fulfill my personal  needs,
but you may find it useful as a template for your own customizations.
SublimeStudio has  borrowed heavily from
[R-Box](https://github.com/randy3k/R-Box) by randy3k (which is available
through package control).


## Features

- a prominent top level menu in SublimeStudio. You will love it (if R is your 
  main language), or hate it (otherwise).

- RStudio niceties: shiny, rmarkdown, roxygen, load all, build and reload

- Support for different versions of R (or S-plus, or remote R sessions)

- An efficient debugging strategy

- Windows and Mac support 


## Installation

- Download the [zip folder](https://github.com/christophsax/SublimeStudio/archive/master.zip). Unzip.

- Move the `SublimeStudio` folder to your package directory (`Preferences > Browse Packages`).

- On Windows, adjust the path to your R installation(s) in 
  `SublimeStudio.sublime-settings`.



## The Sublime Studio Menu

All functions can be called from the SublimeStudio menu; the more frequent
ones also have a short-key:

![](img/sublime-studio-menu.png)



## Setting the R-directory

Many functions from the menu need the 'R-directory' to be set. Press <kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>H</kbd> to use the current file's folder as the 'R-directory'. If
you use, e.g., *LoadAll* (<kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>L</kbd>), this directory will be loaded.

For convenience, if you are inside the R subfolder of an R package, the parent
folder is chosen.

If you want to run a Shiny app, make the directory of your shiny app (the
one with `ui.R` and `server.R`) your 'R-directory'. Press <kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>A</kbd> to run the app.


## Debugging

For R debugging, I find the following strategy useful:

1. Mark the command you want to investigate and save it in the SublimStudio 
   R-Buffer (<kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>O</kbd>). It stays there until you re-assign the buffer.

2. Set a `browser()` somewhere in your function. 

3. Press <kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>L</kbd>: This saves the file, re-loads the package (using
   devtools) und runs the buffer line, so that R will halt were you set the 
   browser. (Make sure the option `browserNLdisabled` is set to `TRUE`; 
   otherwise new lines will quit the browser.)

4. After changing the code, press <kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>Q</kbd> to quit the browser and 
   <kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>L</kbd> to retry.


## Switching R Versions

Press <kbd>Shift</kbd>+<kbd>Ctrl/Cmd</kbd>+<kbd>V</kbd> to select different versions of R. Occasionally, I also
use S-plus with SublimeStudio, which helps me forget that I use S-plus. I also
added a terminal option (on Mac) to work directly on a Linux server.

## Credits

Randy3k, as mentioned. [Autohotkey](http://www.autohotkey.com), which is
included in the `bin` folder and used on Windows to transfer data from 
Sublime Text to R.


