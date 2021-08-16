# -*- coding: utf-8 -*-

def get_num():
	key=0
	print("请输入密钥数字")
	key=int(input())%26
	return key

def get_message():
	print("请输入明文")
	message=input()
	return message

def encry(message,key):
	encryption=""
	for i in message:
		if i.isalpha():
			temp=ord(i)+key	#ord返回十进制整数
			if i.islower():
				if temp>ord('z'):
					temp-=26
				elif temp<ord('a'):
					temp+=26
			if i.isupper():
				if temp>ord('Z'):
					temp-=26
				elif temp<ord('A'):
					temp+=26
			encryption+=chr(temp)

		else:
			encryption+=i
	return encryption

def decry(message,key):
	key=-key
	decryption=""
	for i in message:
		if i.isalpha():
			temp=ord(i)+key
			if i.islower():
				if temp>ord('z'):
					temp-=26
				elif temp<ord('a'):
					temp+=26
			if i.isupper():
				if temp>ord('Z'):
					temp-=26
				elif temp<ord('A'):
					temp+=26
			decryption+=chr(temp)
		else:
			decryption+=i
	return decryption

def getmode():
	while True:
		print("请选择模式")
		print("1.encryption")
		print("2.decryption")
		print("3.brute")
		chioce =input("yout chioce\n")
		if chioce =='1':
			messages=input("你选择了加密模式,请输入明文：")
			key=get_num()
			encryptions=encry(messages,key)	#加密
			print(encryptions)
		if chioce=='2':
			messages=input("你选择了解密模式,请输入需要解密的密文：")
			key=get_num()
			decryptions=decry(encryptions,key)	#解密
			print(decryptions)
		if chioce=='3':
			messages=input("你选择了爆破模式,请输入需要解密的密文：")
			for j in range(0,25):
			#	encryptions=encry(messages,key)
				decryptions=decry(encryptions,j)
				print(decryptions)

if __name__ == '__main__':
	getmode()