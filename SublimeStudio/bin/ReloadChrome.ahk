sleep, 20
WinGet stID, ID, A          ; save current window ID to return here later
WinActivate,ahk_class Chrome_WidgetWin_1
ControlSend,,{F5},ahk_class Chrome_WidgetWin_1
WinActivate ahk_id %stID%
