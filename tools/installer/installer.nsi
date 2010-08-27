# define name of installer
outFile "..\..\eagle3d_${VERSION}.exe"
 
# define installation directory
InstallDir "$PROGRAMFILES\eagle3d"

Name "Eagle3D ${VERSION}"
Caption "Eagle3D ${VERSION}"
 
; Page components
LicenseData "..\..\COPYING"
Page license
Page directory
Page instfiles
 
AutoCloseWindow false
ShowInstDetails show

# start default section
section
 
    # set the installation directory as the destination for the following actions
    setOutPath $INSTDIR
 
    # create the uninstaller
    writeUninstaller "$INSTDIR\uninstall.exe"
    
    file /r "..\..\build\eagle3d\*"
     
sectionEnd

UninstPage uninstConfirm
UninstPage instfiles
UninstallText "Uninstall Eagle3D ${VERSION}"
 
# uninstaller section start
section "uninstall"
 
    # first, delete the uninstaller
    delete "$INSTDIR\uninstall.exe"
    
    ;Delete Files 
    RMDir /r "$INSTDIR\*.*"   
     
# uninstaller section end
sectionEnd

