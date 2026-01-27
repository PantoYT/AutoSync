' ═══════════════════════════════════════════════════
' AutoSync Master Launcher (VBS)
' Starts the master batch script silently in background
' ═══════════════════════════════════════════════════

Option Explicit

Dim fso, shell, scriptDir, batFile

' Create filesystem object
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where THIS VBS file is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Build path to master batch file
batFile = scriptDir & "\master_sync.bat"

' Check if batch file exists
If Not fso.FileExists(batFile) Then
    MsgBox "ERROR: Cannot find master_sync.bat at:" & vbCrLf & vbCrLf & batFile, _
           vbCritical, "AutoSync Launcher"
    WScript.Quit 1
End If

' Create shell object
Set shell = CreateObject("WScript.Shell")

' Run batch file:
' - Chr(34) adds quotes around path (handles spaces)
' - 0 = hidden window (runs silently)
' - False = don't wait for completion (async)
shell.Run Chr(34) & batFile & Chr(34), 0, False

' Show brief notification (optional - comment out if you don't want it)
' MsgBox "AutoSync started successfully!" & vbCrLf & _
'        "Monitoring for USB drive...", _
'        vbInformation, "AutoSync"

' Clean up
Set shell = Nothing
Set fso = Nothing

WScript.Quit 0
