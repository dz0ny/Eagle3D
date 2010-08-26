# define name of installer
outFile "eagle3d-${VERSION}.exe"
 
# define installation directory
InstallDir "$PROGRAMFILES\eagle3d"
 
# start default section
section
 
    # set the installation directory as the destination for the following actions
    setOutPath $INSTDIR
 
    # create the uninstaller
    writeUninstaller "$INSTDIR\uninstall.exe"
    
    file /r "..\..\build\eagle3d\*"
     
sectionEnd
 
# uninstaller section start
section "uninstall"
 
    # first, delete the uninstaller
    delete "$INSTDIR\uninstall.exe"
    
    ;Delete Files 
    RMDir /r "$INSTDIR\*.*"   
     
# uninstaller section end
sectionEnd

