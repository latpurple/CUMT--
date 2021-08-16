# #---本源多项式---
import random
print("请输入初始寄存器状态")
source=str(input())
tmp=''
f=['1',]		#f是抽头
count_1=0
for i in range(len(source)):
	f.append(str(random.randint(0,1)))
	if f[i]=='1':
		count_1+=1
	if source[i]=='1':
		# print(i)
		tmp=tmp+'x^'+str(len(source)-i)+'+'
tmp+='1'
if count_1%2==1:
	f[-2]='0'
print("对应的多项式是：",tmp)
print("抽头f:",f[:-1])
print("初始寄存器状态是：",source)
# print("tmp:",tmp)
length=2**len(source)-1		#2^n-1
cmpare=source
time=0
for i in range(length):
	x=0
	##根据当前寄存器的状态，进行异或操作
	for k in range(len(f)-1):	
		if f[k]=='1':
			x=x^int(source[k])
	if x==1:
		tmp+=source[-1]		#输出最右边
		source=source[:-1]
		source='1'+source 	#把'1'加到最左边，下同		
		time+=1
	else:
		tmp+=source[-1]
		source=source[:-1]
		source='0'+source		
		# print("source_len",len(source))
		time+=1
	if cmpare==source:
		break
if time==length:	#length=2**len(source)-1
	print("正确")
	print("当前寄存器状态是:",source)
	print("周期是：",time)
else:
	print("错误，请重新输入寄存器初始状态")
