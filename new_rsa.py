import random
import binascii
#-------快速幂算法------
def quick_pow(m,e,n):
	result=1
	while e>0:
		if e%2 == 1:
			result=result*m%n
		m=m*m%n
		e=e//2
		#e=int(e/2)		#用这个贼慢
#----或者：e//=2
#----取整除法
	return result%n

#---欧几里得算法判断素数---
def gcd(a, b):
    """
    a,b顺序无所谓
    """
    while b != 0:
        # print(a, b)
        a, b = b, a % b
    return a

#---扩展欧几里得求逆---
def extd_gcd(a, b):
     if b == 0:
         return 1, 0, a
     else:
         x, y, q = extd_gcd(b, a % b) # q = gcd(a, b) = gcd(b, a%b)
         x, y = y, (x - (a // b) * y)
         return x, y, q

# #---产生大素数---
def get_prime(length):
	while True:
		n=get_longint(length)		#得到的是偶数，重新生成
		if n%2==0:
			continue
		#---进行10次素性检验---
		flag=1
		for i in range(10):
			if rabin(n)==False:		#不满足，则重新找
				flag=0
				break
		if flag==1:				#满足10次检验后，不是素数的可能性已经很小了
			return n

#---得到大整数,默认位数为1024---
def get_longint(key_size=1024):
	num = random.randrange(2**(key_size-1), 2**key_size)
	return num
    # while True:
    #     num = random.randrange(2**(key_size-1), 2**key_size)
    #     if is_prime(num):
    #         return num

#---另外一种方法---
# def is_prime(num):
#     # 排除0,1和负数
#     if num < 2:
#         return False

#     # 创建小素数的列表,可以大幅加快速度
#     # 如果是小素数,那么直接返回true
#     small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
#     89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 
#     197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
#     331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 
#     461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
#     607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
#     751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 
#     907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
#     if num in small_primes:
#         return True

#     # 如果大数是这些小素数的倍数,那么就是合数,返回false
#     for prime in small_primes:
#         if num % prime == 0:
#             return False

#     # 如果这样没有分辨出来,就一定是大整数,那么就调用rabin算法
#     return rabin(num)


# # 得到大整数,默认位数为1024
# def get_prime(key_size=1024):
#     while True:
#         num = random.randrange(2**(key_size-1), 2**key_size)
#         if is_prime(num):
#             return num

#---rabin算法进行素性检验---
def rabin(n):
	r=n-1
	t=0
	while n%2==0:
		t+=1
		n//=2
	a=random.randrange(2,n-2)
	#---费马小定理---a^(n-1)=1 mod n，
	if quick_pow(a,r,n)==1:
		return True
		#---存在一个i使得下列式子成立，则n可能是一个素数---
	for i in range(0,t):
		if quick_pow(a,(2^i)*r,n)==n-1:
			return True
	return False

#---得到公钥---
def get_e(fai):
	while True:
		e=random.randint(2,fai)
		if gcd(e,fai)==1:
			return e

	# for e in range(2,fai):		
	# 	if gcd(e,fai)==1:
	# 		return e

#---得到私钥---
def get_d(e,fai):
	d,x,y=extd_gcd(e,fai)
	if d<0:
		d+=fai
	return d


#---加解密部分---
print("请输入素数位数：")
l=int(input())
p=get_prime(l//2)
q=get_prime(l//2)
n=p*q
print("p=",p,"\nq=",q,"\nn=",n)
fai=(p-1)*(q-1)
e=get_e(fai)		#找到e
# e=get_e(fai)		
d=get_d(e,fai)		#计算d
print("\nfai=",fai,"\ne=",e,"\nd=",d)

print("请输入密文")
# m="abcdefgh123"
m=input()
m=m.encode().hex()		#这里转成将每个字符变成十六进制

print("消息十六进制表示",m)
m=int(m,16)				#变成十六进制整数
# print(m)
c=quick_pow(m,e,n)
print("加密后结果是：",c)
message=quick_pow(c,d,n)
print("解密后十进制表示是：",message)
# print("解密后结果是：")
message=hex(message)
message=str(message)[2:]
# message=message.decode().hex()

tmp=''
for i in range(0,len(message),2):
	xx='0x'+(message[i:i+2])
	tmp+=chr(int(eval(xx)))		#eval去掉两边引号，QAQ十六进制转字符串想了好久

print("解密结果是：",tmp)