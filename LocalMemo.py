"""
로컬 메모
"""

print("새 메모를 입력하세요: ") #새로운 내용을 입력 받는다.
memo = input()

f = open("새파일.txt", 'a') #입력받은 값을 새 파일에 저장한다.
f.write(memo)
f.write('\n')
f.close()

f2 = open("새파일.txt", 'r') #저장된 내용을 출력한다.
print(f2.read())
f2.close()

#메모 시간 추가 예정
