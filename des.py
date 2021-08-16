# -*- coding:utf-8 -*-
from _box import *
import re
import base64

#---字符串转二进制---
def str_to_bin(message):
	res=''
	for i in message:
		tmp=bin(ord(i))[2:]		#去掉前面的 0b
		for j in range(0,8-len(tmp)):
			tmp='0'+tmp			#最高位补0，变成8位
		res+=tmp
	return res

#---二进制转成字符串---
def bin_to_str(bin_str):
	res=''
	tmp=re.findall(r'.{8}',bin_str)		#8位一组
	for i in tmp:
		res+=chr(int(i,2))
	return res

#---IP置换---
def ip_change(bin_str):
	res=''
	for i in IP_table:
		res+=bin_str[i-1]		#数组下标从0开始
	return res

#---IP逆置换
def ip_re_change(bin_str):
	res=''
	for i in IP_re_table:
		res+=bin_str[i-1]		#数组下标从0开始
	return res

#---E置换---
def e_change(bin_str):
    res = ''
    for i in E:
        res += bin_str[i-1]
    # print("E_change:",res)
    return res

#---异或操作---
def xor(str1,str2):
	res=''
	for i in range(0,len(str1)):
		tmp=int(str1[i],10)^int(str2[i],10)
		if tmp==1:
			res+='1'
		if tmp==0:
			res+='0'
		# if str1[i]==str2[i]:
		# 	res+='0'
		# else:
		# 	res+='1'
	return res

#---左移---
def left_(str_,time):
	return str_[time:len(str_)]+str_[0:time]

#---pc1---
def pc1_change(key):
	res=''
	for i in PC_1:
		res+=key[i-1]
	return res

#---pc2---
def pc2_change(key):
	res=''
	for i in PC_2:
		res+=key[i-1]
	return res

#---s_box---
def s_box(str_bin):
	res=''
	si=0			#第i个s盒
	for i in range(0,len(str_bin),6):
		current_str=str_bin[i:i+6]	#每6位一组
		row=int(current_str[0]+current_str[5],2)	#行号
		col=int(current_str[1:5],2)			#列号
		num=bin(S[si][row*16+col])[2:]				#去掉0b
		#4位二进制表示一个十六进制，所以可能不满足4位
		for t in range(0,4-len(num)):
			num='0'+num
		res+=num
		si+=1
	return res

#---p置换---
def p_change(str_bin):
	res=''
	for i in P:
		res+=str_bin[i-1]	#str_bin[-1]就是最后一个
	return res

#---F函数---
def f_function(str_bin,key):
	E_result=e_change(str_bin)		#E置换
	xor_result=xor(E_result,key)	#异或
	s_box_result=s_box(xor_result)	#s盒处理
	p_result=p_change(s_box_result)	#p盒处理
	return p_result

#---子密钥---
def subkey(key):
	keylist=[]
	key=pc1_change(key)
	# print("key:",key)
	#---分成左右两部分---
	SHIFT=[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]		#进行循环左移操作
	key_left=key[0:28]
	key_right=key[28:56]
	for i in SHIFT:
		key_left=left_(key_left,i)
		key_right=left_(key_right,i)
		sub=pc2_change(key_left+key_right)		#字串合并后进行pc2置换
		keylist.append(sub)
	# print(keylist)
	return keylist

#---单次加密---
#---按照书上流程进行---
def encrp(bin_message,bin_key):
	ip_message=ip_change(bin_message)	#对二进制消息进行IP置换

	bintext=''
	key_list=subkey(bin_key)			#获取子密钥
	# print("子密钥是：",key_list)
	L=ip_message[0:32]					#分成左右两部分
	R=ip_message[32:64]

	#---开始十六轮迭代---
	for i in range(15):
		tmp=R
		f_result=f_function(tmp,key_list[i])	#f_function函数结束之后，p置换结束，
		R=xor(L,f_result)

		L=tmp 			#tmp就是Ri-1
		#---最终得到了R15，L15
		#---执行R15->R16
	L=xor(L,f_function(R,key_list[15]))
	L_R=L+R
	res=ip_re_change(L_R)
	# print('十六轮迭代后二进制表示',res)
	bintext=res
	res=bin_to_str(res)
	return res,bintext
	
#---单次解密---,加密的逆过程，复现书上过程
def decrp(bin_message,bin_key):
	ip_message=ip_change(bin_message)	#对二进制消息进行IP置换


	key_list=subkey(bin_key)			#获取子密钥

	L=ip_message[0:32]					#分成左右两部分
	R=ip_message[32:64]

	#---开始十六轮迭代---
	# for i in range(15,0,-1):
	lis=range(1,16)
	for i in lis[::-1]:
		tmp=R
		f_result=f_function(tmp,key_list[i])	#f_function函数结束之后，p置换结束，
		R=xor(L,f_result)				#L与f_fubction异或的结果给Ri-1

		L=tmp 		#tmp是Ri

	#---执行L0=L1^F(R1,K1)
	#---R0=R1
	L=xor(L,f_function(R,key_list[0]))
	L_R=L+R
	res=ip_re_change(L_R)
	res=bin_to_str(res)
	return res


message='abcdefgh'
key='qweqweqw'

#---消息进行分组处理---
def longmessage(message):
	res=''
	for i in message:
		tmp=bin(ord(i))[2:]		#去掉前面的0b
		for i in range(8-len(tmp)):
			tmp='0'+tmp
		res+=tmp
	#---补'0'，变成64的整数倍长
	if len(res)%64!=0:
		for i in range(64-len(res)%64):
			res+='0'
	#---分组---
	lis=[]
	for i in range(0,len(res),64):
		tmp=res[i:i+64]
		lis.append(tmp)
	return lis

#---密文消息分组---
def chipermesage(binchip):
	lis=[]
	for i in range(0,len(binchip),64):
		tmp=binchip[i:i+64]
		lis.append(tmp)
	return lis


#---加密过程---
def slove(message,key):
	#---bin_tmp是消息二进制表示---
	bin_tmp=''
	lis=longmessage(message)
	key=str_to_bin(key)
	if len(key)!=64:
		for i in range(64-len(key)%64):
			key+='0'
	res=''
	for i in lis:
		tmp,bin_=encrp(i,key)
		res+=tmp
		bin_tmp+=bin_
	print("加密的结果：",res)
	print("消息二进制表示：",bin_tmp)
	res=res.encode()
	res=base64.b64encode(res)
	print("消息base64表示：",res)
	return res

#---进行解密---
def re_slove(chiper,key):
	# chiper=longmessage(chiper)
	chiper=chipermesage(chiper)
	key =str_to_bin(key)
	if len(key)!=64:
		for i in range(64-len(key)%64):
			key+='0'
	res=''
	for i in chiper:
		tmp=decrp(i,key)
		res+=tmp
	print("解密结果是：",res)
	return res

#---选择模式---
def get_mode():
	while True:
		print("加密：1")
		print("解密：2")
		print("退出：3")
		chioce=input("请选择模式：")
		if chioce=='1':
			message=input("请输入需要加密的信息:")
			key=input("请输入你的密钥，长度小于等于64比特:")
			if len(key)>8:
				print("请重新开始")
				continue
			#---调用加密函数---
			# message=str_to_bin(message)
			# message=longmessage(message)
			# chiper=bin_to_str(message)
			# print(chiper)
			slove(message,key)

		if chioce=='2':
			chip=input("请输入需要解密的信息,用二进制表示:")
			key=input("请输入解密密钥，长度小于64比特:")
			if len(key)>8:
				print("请重新开始")
				continue
			#---调用解密函数---
			# chip=str_to_bin(message)
			# chip=chipertomessage(chip)
			# message=bin_to_str(chip)
			re_slove(chip,key)
			# print(message)
		if chioce=='3':
			break
		else :
			continue

if __name__ == '__main__':
	get_mode()