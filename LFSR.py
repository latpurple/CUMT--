def LFSR():
    print("请输入寄存器(16位)的初始状态")
    s = input()
    if s == '0000000000000000' or len(s) != 16:
        print("输入有误，请重新输入")
        return LFSR()
    print("初始寄存器状态是：",s)
    ss = s
    tmp = list(s)  # 字符串转列表
    cycle = 0
    while True:
        # 选择不可约多项式 x^16+x^12+x^3+x+1
        i = int(tmp[15]) ^ int(tmp[11]) ^ int(tmp[2]) ^ int(tmp[0])
        # 左移一位
        for j in range(len(tmp)):
            tmp[len(tmp) - 1 - j] = tmp[len(tmp) - 2 - j]
        # 添加异或结果
        tmp[0] = str(i)
        # print(len(tmp))
        s2 = "".join(tmp)  # 列表转字符串
        cycle += 1
        # print(s2)
        if s2 == ss:
            # print(s2)
            break
    print("最后寄存器状态是：",s2)
    print("周期为：", cycle)
    if cycle == pow(2, len(s)) - 1:
        print("验证成功！")
    else:
        print("验证失败！")

if __name__ == '__main__':
    LFSR()