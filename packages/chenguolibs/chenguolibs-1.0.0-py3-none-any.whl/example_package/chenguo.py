from math import sqrt

def is_prime(n):
    if n==1:
        return False
    for i in range(2, int(sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True

def aboutwriter():
    print("请问作者的真名是什么？")
    keyword=input()
    if keyword=="陈果":
        print("对了！祝您万事如意！")
    else:
        print("您好像不认识作者哦。")
