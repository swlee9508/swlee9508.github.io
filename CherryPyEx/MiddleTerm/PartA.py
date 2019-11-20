STUDENT = 5

score = []
scoreSum = 0

for x in range(STUDENT):
    value = (int(input("성적을 입력하십시오 : ")))
    score.append(value)
    scoreSum += value

scoreAvg = scoreSum/STUDENT

highScoreStudent = 0
for i in range(len(score)):
    if score[i] >= 80:
        highScoreStudent += 1

print("성적 평균은 %f 입니다." %scoreAvg)
print("성적이 80점 이상인 학생은 %d명 입니다." %highScoreStudent)



