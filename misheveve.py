import pyautogui
from time import sleep
sleep(6)
text1 = '\n\nAkaulizia mama  "unapika mboga gani?"\n mama akasema "leo nimeunda misheveve"\nkijana akasema "sikutaka hizi, nilitaka sarati"\n'
text2 = 'Baba alifika bila shaka kumuokoa mama\n Alimwangamiza vipii?\n'
text3 = 'Alianza kwa kutafuna mzee vidole\n Anatafuna mzee vidole nikama anatafuna omena\n.....'
def type():
    misheveve = text1+text2+text3
    typing_speed = 0.088
    pyautogui.typewrite(misheveve, typing_speed)

type()