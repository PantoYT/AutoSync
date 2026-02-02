' ═══════════════════════════════════════════════════
' AutoSync Master Launcher v2.1
' Unified launcher with start/stop/restart capabilities
' ═══════════════════════════════════════════════════
Option Explicit

Dim fso, shell, scriptDir, batFile, arg
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' Get script directory
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
batFile = scriptDir & "\master_sync.bat"

' Check if batch file exists
If Not fso.FileExists(batFile) Then
    MsgBox "ERROR: Cannot find master_sync.bat at:" & vbCrLf & vbCrLf & batFile, _
           vbCritical, "AutoSync Launcher"
    WScript.Quit 1
End If

' Parse command line arguments
If WScript.Arguments.Count > 0 Then
    arg = LCase(Trim(WScript.Arguments(0)))
Else
    arg = "start"
End If

' Handle commands
Select Case arg
    Case "start", "/start", "-start"
        StartAutoSync()
        
    Case "stop", "/stop", "-stop"
        StopAutoSync()
        MsgBox "AutoSync stopped successfully!", vbInformation, "AutoSync"
        
    Case "restart", "/restart", "-restart"
        StopAutoSync()
        WScript.Sleep 2000
        StartAutoSync()
        MsgBox "AutoSync restarted successfully!", vbInformation, "AutoSync"
        
    Case "status", "/status", "-status"
        CheckStatus()
        
    Case Else
        StartAutoSync()
End Select

WScript.Quit 0

' ═══════════════════════════════════════════════════
' FUNCTIONS
' ═══════════════════════════════════════════════════

Sub StartAutoSync()
    ' Check if already running
    If IsProcessRunning("cmd.exe", "master_sync.bat") Then
        Dim choice
        choice = MsgBox("AutoSync is already running!" & vbCrLf & vbCrLf & _
                       "Do you want to restart it?", _
                       vbQuestion + vbYesNo, "AutoSync")
        
        If choice = vbYes Then
            StopAutoSync()
            WScript.Sleep 2000
        Else
            WScript.Quit 0
        End If
    End If
    
    ' Start the batch file silently
    shell.Run Chr(34) & batFile & Chr(34), 0, False
    
    ' Optional: Show notification (comment out if you don't want it)
    ' MsgBox "AutoSync started successfully!" & vbCrLf & _
    '        "Monitoring for USB drive...", _
    '        vbInformation, "AutoSync"
End Sub

Sub StopAutoSync()
    Dim killed
    killed = KillProcess("cmd.exe", "master_sync.bat")
    
    If killed = 0 Then
        ' Also try to kill by window title
        On Error Resume Next
        shell.Run "taskkill /FI ""WINDOWTITLE eq master_sync.bat*"" /F", 0, True
    End If
End Sub

Sub CheckStatus()
    If IsProcessRunning("cmd.exe", "master_sync.bat") Then
        MsgBox "AutoSync Status: RUNNING" & vbCrLf & vbCrLf & _
               "Monitoring USB drive and syncing files.", _
               vbInformation, "AutoSync Status"
    Else
        MsgBox "AutoSync Status: STOPPED" & vbCrLf & vbCrLf & _
               "Run this script to start AutoSync.", _
               vbExclamation, "AutoSync Status"
    End If
End Sub

Function IsProcessRunning(processName, searchString)
    Dim objWMI, colProcesses, objProcess, found
    
    found = False
    
    On Error Resume Next
    Set objWMI = GetObject("winmgmts:\\.\root\cimv2")
    
    If Err.Number <> 0 Then
        IsProcessRunning = False
        Exit Function
    End If
    
    Set colProcesses = objWMI.ExecQuery("SELECT * FROM Win32_Process WHERE Name = '" & processName & "'")
    
    For Each objProcess In colProcesses
        If searchString = "" Or IsNull(searchString) Then
            found = True
            Exit For
        End If
        
        If Not IsNull(objProcess.CommandLine) Then
            If InStr(1, objProcess.CommandLine, searchString, vbTextCompare) > 0 Then
                found = True
                Exit For
            End If
        End If
    Next
    
    Set colProcesses = Nothing
    Set objWMI = Nothing
    
    IsProcessRunning = found
End Function

Function KillProcess(processName, searchString)
    Dim objWMI, colProcesses, objProcess, killed
    
    killed = 0
    
    On Error Resume Next
    Set objWMI = GetObject("winmgmts:\\.\root\cimv2")
    
    If Err.Number <> 0 Then
        KillProcess = 0
        Exit Function
    End If
    
    Set colProcesses = objWMI.ExecQuery("SELECT * FROM Win32_Process WHERE Name = '" & processName & "'")
    
    For Each objProcess In colProcesses
        If searchString = "" Or IsNull(searchString) Then
            objProcess.Terminate()
            killed = killed + 1
        Else
            If Not IsNull(objProcess.CommandLine) Then
                If InStr(1, objProcess.CommandLine, searchString, vbTextCompare) > 0 Then
                    objProcess.Terminate()
                    killed = killed + 1
                End If
            End If
        End If
    Next
    
    If killed > 0 Then
        WScript.Sleep 500
    End If
    
    Set colProcesses = Nothing
    Set objWMI = Nothing
    
    KillProcess = killed
End Function

' Clean up
Set shell = Nothing
Set fso = Nothing
