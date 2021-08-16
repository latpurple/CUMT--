
low=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
up=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


#---获取密钥---
def get_real_key():
    """
    获取列需要加的秘钥
    """
    print("输入你的秘钥")
    key = input()      #得确保都是英文
    tmp = []
    flag = 0
    for i in key:
        if i.isalpha():
            pass
        else:
            flag = 1
    if flag == 0:
        for i in key:
            tmp.append(ord(i.upper()) - 65)		#---全部大写---
        return tmp
    else:
        print("请输入英文秘钥")

#---加密---
def encryp(text,key):
	res=''
	key_len=0
	for i in text:
		if key_len%len(key)==0:
			key_len=0
		if i.isalpha():
			#---是大写---
			if i.isupper():
				res+=up[(ord(i)-65+key[key_len])%26]
				key_len+=1
			#---是小写---
			if i.islower():
				res+=low[(ord(i)-97+key[key_len])%26]
				key_len+=1
		else:
			res+=i
	return res

#---解密---
def decryp(text,key):
	res=''
	key_len=0
	for i in text:
		if key_len%len(key)==0:
			key_len=0
		if i.isalpha():
			#---是大写---
			if i.isupper():
				res+=up[(ord(i)-65-key[key_len])%26]
				key_len+=1
			#---是小写---
			if i.islower():
				res+=low[(ord(i)-97-key[key_len])%26]
				key_len+=1
		else:
			res+=i
	return res

#---选择模式---
def get_mode():
	print("请选择模式：")
	print("加密：1")
	print("解密：2")
	chioce=input("你的选择是:---")
	if chioce=='1':
		print("加密模式，请输入需要加密的内容")
		text=input()
		# print("请输入你的密钥")
		key=get_real_key()
		print("加密的结果是："+encryp(text,key))
	if chioce=='2':
		print("解密模式，请输入需要解密的内容")
		text=input()
		# print("请输入你的密钥")
		key=get_real_key()
		print("解密的结果是："+decryp(text,key))


if __name__ == '__main__':
	while True:
		get_mode()