#파이썬 메모

import sys

option = sys.argv[1]

if option =='-a': #메모 입력
    memo = sys.argv[2]
    f= open('memo.txt','a')
    f.write(memo)
    f.write('\n')
    f.close()

elif option=='-v': #메모 출력
    f = open('memo.txt')
    memo=f.read()
    f.close()
    print(memo)
