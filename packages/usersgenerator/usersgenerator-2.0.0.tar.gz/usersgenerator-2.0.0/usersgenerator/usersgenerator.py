#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from colorama import init, Fore
from time import sleep
init()

if sys.version_info < (3, 0):
	print(Fore.RED + "Disculpa, la aplicacion usa python 3.x\n")
	sys.exit(1)
def checkVersion():
	if sys.version_info < (3, 0):
	    print(Fore.RED + "Disculpa, la aplicacion usa python 3.x\n")
	    sys.exit(1)

def logo():
	
	header = '''
 _   _                     _____                           _             
| | | |                   |  __ \                         | |            
| | | |___  ___ _ __ ___  | |  \/ ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
| | | / __|/ _ \ '__/ __| | | __ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
| |_| \__ \  __/ |  \__ \ | |_\ \  __/ | | |  __/ | | (_| | || (_) | |   
 \___/|___/\___|_|  |___/  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_|   

		                              Autor: AbelJM, AngussMoody
		                                   Web: abeljm.github.io
	'''
	print(header)

def readFile(usersfile):
	users = []
	with open(usersfile, "r") as user:
		for line in user:
			users.append(line.rstrip())
		return users		

def generateUsers(users):
	g_users = []
	for user in users:		
		user_s = user.split(" ")
		if len(user_s) == 2:
			initial_u = user_s[0][0]
			initial_l = user_s[1][0]
			g_users.append(user_s[0]) 
			g_users.append(user_s[1])
			g_users.append(user.replace(' ',"-"))
			g_users.append(user.replace(' ',"_"))
			g_users.append(user.replace(' ',"."))
			g_users.append(user_s[0]+user_s[1])
			g_users.append(initial_u+user_s[1])        		
			g_users.append(initial_u+'-'+user_s[1])
			g_users.append(initial_u+'_'+user_s[1])
			g_users.append(initial_u+'.'+user_s[1])
			g_users.append(user_s[0]+initial_l)	
			g_users.append(user_s[0]+'-'+initial_l)
			g_users.append(user_s[0]+'_'+initial_l)
			g_users.append(user_s[0]+'.'+initial_l)
			g_users.append(initial_u+initial_l)
	
	return g_users
			

def saveFile(g_users,name_file):
	path = os.getcwd()
	path_file = "%s/%s" %(path,name_file)
	with open(path_file, mode='w', encoding='utf-8') as file:
		for g_user in g_users:
			file.write('%s\n' %(g_user))
	return path_file

def main():
	parser = argparse.ArgumentParser(description='Ejemplo:', epilog="python3 usersgenerator.py -u users.txt -o resultado.txt")
	parser.add_argument("-u", "--users", type=str, required=True, help="lista de usuarios en archivo de texto, ejemplo: -u users.txt")
	parser.add_argument("-o", "--output",  type=str, required=True, help="Guardar resultado en archivo de texto, poner nombre ejemplo: -o resultado.txt")
	args = parser.parse_args()

	logo ()
	checkVersion()	
	
	try:
		userfile = args.users
		file_g = args.output
		users = readFile(userfile)
		print(Fore.GREEN + "[*] Lista de usuarios" + Fore.RESET)
		for user in users:
			print("[+] %s" % (user.rstrip()))
			sleep(0.1)
		print(Fore.GREEN + f"\n[*] Generar usuarios" + Fore.RESET)
		g_users = generateUsers(users)
		for g_user in g_users:
			print("[+] %s" % (g_user.rstrip()))
			sleep(0.03)
		print(Fore.GREEN + f"\n[*] guardando usuarios" + Fore.RESET)
		file_g = saveFile(g_users, file_g)
		if os.path.isfile(file_g):
			print("[+] Archivo guardado: " + Fore.YELLOW + file_g + Fore.RESET)
		
	except Exception as e:
		print(e)
	

if __name__ == '__main__':
	main()

	