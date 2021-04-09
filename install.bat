@echo off
chcp 65001
echo [93mLe programme d'installation va télécharger et installer plusieurs paquets additionnels Python. Ceci peut durer plusieurs minutes.[0m

echo.
call :upgradepip
call :installpackage "PySide2==5.15.2"
call :installpackage "opencv-python==4.5.1.48
call :installpackage "dict2xml==1.7.0"
call :installpackage "torch==1.8.1+cu102 -f https://download.pytorch.org/whl/torch_stable.html"
goto ok

:upgradepip
echo [93mPip upgrade...[0m
python -m pip install --upgrade pip setuptools > python-packages.log
if errorlevel 1 goto error

echo [93mPip upgrade OK[0m
exit /b 0

:installpackage
echo [93mInstall %~1...[0m
pip install %~1 >> python-packages.log
if errorlevel 1 goto error
echo [93mInstall %~1 OK[0m
exit /b 0

:error
echo.
echo [91mUne erreur est survenue, vérifiez que Python est installé, vérifiez votre connexion internet. Si le problème persiste contactez le support.[0m
pause
exit

:ok
echo.
echo [92mL'installation des paquets additionnels de Python s'est deroulée correctement.[0m
echo [92mVous pouvez exécuter le fichier "Main.py".[0m
del python-packages.log
pause
exit
