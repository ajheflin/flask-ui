
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

if %OS%==32BIT "%~dp0vc_redist.x86.exe" /install /passive /norestart
if %OS%==64BIT "%~dp0vc_redist.x64.exe" /install /passive /norestart

python get-pip.py

pip install spacy
pip install tk
pip install wordfreq

pip install contextualSpellCheck

python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
REM python -m spacy download en_core_web_lg

PAUSE
