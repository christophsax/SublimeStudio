; Original by Andrew Redd 2011 <halpo@users.sourceforge.net>
; Modified by Randy Lai 2013 <randy.cs.lai@gmail.com>
; Modified by Christoph Sax 2014 <christoph.sax@gmail.com>
; use govorned by the MIT license http://www.opensource.org/licenses/mit-license.php

RGetOrStart(Rguiexe) {
    SetTitleMatchMode, 1

    if (WinExist("R Console")) {
        WinGet RprocID, ID ;,A
        return RprocID
    }
    else {
        run %Rguiexe% --sdi,dir,,RprocID
        WinWait ,R Console,, 2
        WinGet RprocID, ID ,A
        return RprocID
    }
}

oldclipboard = %clipboard%  ; save current clipboard to restore later
WinGet stID, ID, A          ; save current window ID to return here later

Rguiexe = %1%
cmd = %2%

cmd := RegExReplace(cmd, "^\n", "")
newline = `n
clipboard := cmd . newline

RprocID:=RGetOrStart(Rguiexe)
WinMenuSelectItem ahk_id %RprocID%,,2&,2& ;edit->paste

WinActivate ahk_id %stID%
clipboard := oldclipboard
