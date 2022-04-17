#!/usr/bin/env python3

import math
import random
import sys
KEY_SIZE = 2048


# we find r and s in (n-1) = r*(2^s). r is odd
def rabin_miller(n):
    # s_num = num - 1
    # t_num = 0
    # while s_num % 2 == 0:
    #     s_num = s_num // 2
    #     t_num += 1

    # for trials in range(5):
    #     a_num = random.randrange(2, num - 1)
    #     v_num = pow(a_num, s_num, num)
    #     if v_num != 1:
    #         i_index = 0
    #         while v_num != (num - 1):
    #             if i_index == t_num - 1:
    #                 return False
    #             else:
    #                 i_index = i_index + 1
    #                 v_num = (v_num ** 2) % num
    s = 0
    r = n - 1
    while r%2==0:
        s+=1
        r=r//2
    for _ in range(5):
        a = random.randrange(2, n-1)
        x = pow(a,r,n)
        if x!=1:
            i = 0
            while x !=n-1:
                if i == s-1:
                    return False
                else:
                    i +=1 
                    x = (x**2) % n
    return True

def prime_test(n):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    return rabin_miller(n)

def modular_inverse(a,m):
    if gcd(a,m) != 1:
        return None
    mod_m = m
    x = 1
    y = 0

    if m == 1:
        return 0
    while a > 1:
        quotient = a // m
        temp = m
        m = a % m
        a = temp
        temp = y

        y = x - quotient * y
        x = temp
    
    if x < 0:
        x = x + mod_m
    
    return x

def gcd(a,b):
    while a != 0:
        a, b = b % a, a
    return b


def generate_keys(keysize = KEY_SIZE):

    while True:
        p = random.randrange(2**(keysize-1)+1, 2**(keysize) - 1)
        if prime_test(p):
            break

    while True:
        q = random.randrange(2**(keysize-1)+1, 2**(keysize) - 1)
        if prime_test(q):
            break

    n = p * q
    phi_n = (p-1)*(q-1)

    while True:
        e = random.randrange(2**(keysize-1)+1, 2**(keysize) - 1)
        if gcd(e, phi_n) == 1:
            break
    
    d = modular_inverse(e, phi_n)

    pub_key = (n, e)
    priv_key = (n, d)
    return (n , e , d)


if __name__ == "__main__":
    print('Start')
    n , e, d = generate_keys(KEY_SIZE)
    with open(sys.argv[1] +".pub", 'w') as file:
        file.write('%s, %s, %s' % (KEY_SIZE, n, e))

    with open(sys.argv[1] +".prv", 'w') as file:
        file.write('%s, %s, %s' % (KEY_SIZE, n, d))
    