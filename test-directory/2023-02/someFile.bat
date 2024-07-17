@echo OFF

set dt=%DATE:~6,4%.%DATE:~3,2%.%DATE:~0,2%_%TIME:~0,2%.%TIME:~3,2%.%TIME:~6,2%
set dt=%dt: =0%

echo %dt%

for /f "skip=5 tokens=1,2,4,5* delims= " %%a in ('dir  /a:-d /o:d /t:c') do (
    if "%%~c" NEQ "bytes" (
        echo(
        @echo file name:     %%~d
        @echo creation date: %%~a
        @echo creation time: %%~b
        echo(

    )
)

pause
