; Original by Andrew Redd 2011 <halpo@users.sourceforge.net>
; Modified by Randy Lai 2013 <randy.cs.lai@gmail.com>
; Modified by Christoph Sax 2014 <christoph.sax@gmail.com>
; use govorned by the MIT license http://www.opensource.org/licenses/mit-license.php

SGetOrStart(Spexe) {
    SetTitleMatchMode, 1

    if (WinExist("TIBCO Spotfire S+ Console")) {
        WinActivate
        WinGet RprocID, ID ;,A
        Outputdebug % dstring . "exiting, RprocID=" . RprocID
        return RprocID
    }
    else { 
        SetTitleMatchMode, 1
        run %Spexe% 
        WinWait ,R Console,, 2
        WinGet RprocID, ID ,A
        Outputdebug % dstring . "Exiting, RprocID=" . RprocID
        return RprocID
    }
}

oldclipboard = %clipboard%  ; save current clipboard to restore later
WinGet stID, ID, A          ; save current window ID to return here later

Spexe = %1%
cmd = %2%

cmd := RegExReplace(cmd, "^\n", "")
newline = `n
clipboard := cmd . newline

WinGet stID, ID, A          ; save current window ID to return here later
RprocID:=SGetOrStart(Spexe)
SendInput {Raw}%clipboard%
WinActivate ahk_id %stID%
clipboard := oldclipboard

