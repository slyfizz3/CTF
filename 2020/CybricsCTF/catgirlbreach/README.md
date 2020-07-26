## Catgirlbreach (rebyC)

Author: Stanislav Rakovskiy [@hexadec1mal](https://t.me/hexadec1mal)

CatGirl Industrials was breached by a malware attack from their competitors. They have lost all their secret flags to the encrypting ransomware! Can you decrypt their most precious flag?

Download: [catgirlbreach.tar.gz](catgirlbreach.tar.gz)

---

## Solution

1. Extract the file do_not_pet_me.exe

2. Extract main.exe from madoka.bat

3. Use [pyextractor](https://github.com/extremecoders-re/pyinstxtractor) to extract main.py from main.exe

4.In main.py, you can get another source code by replace exec to print and than you can get really main.py source

5.finally just reverse the source code([reversable.py](./reversable.py)) and you can get the [flag](./flag.png) 
