from vpython import *

## 상수
g = 9.8            # 중력 가속도
t = 0            # 시간 시작점
deltat = 0.001   # 시간 간격

# 진자의 시작 각도, 줄의 길이, 질량, 운동량
theta = 1.2       # 시작 각도 (라디안)
L = 0.8           # 줄의 길이
m = 0.1           # 질량 (kg)
p = m * vector(0, 0, 0)  # 시작 운동량

# 줄을 아주 큰 k로 취급하여 스프링처럼 취급
k = 1e5

## 천장, 진자, 줄 생성
ceiling = box(pos=vector(-0.5, 1, 0), size=vector(0.01, 0.01, 0.01))
ball = sphere(pos=vector(ceiling.pos.x + L * sin(theta), ceiling.pos.y - L * cos(theta), 0), radius=0.05,
              color=color.red, make_trail=True, interval=40, retain=1e4)
string = cylinder(pos=ceiling.pos, axis=ball.pos - ceiling.pos, color=color.white, radius=0.008)

# 그래프 설정
oscillation = graph(title='단일 진자 운동', xtitle='시간 (초)', ytitle='Theta (라디안)')
anglegraph = gcurve(graph=oscillation, color=color.red,)
oscillation.width = 1500

## 계산 루프
while t < 1e2:
    rate(1 / deltat)

    # 방사형 벡터와 힘 계산
    r = vector(ball.pos.x - ceiling.pos.x, ball.pos.y - ceiling.pos.y, ball.pos.z - ceiling.pos.z)
    F = m * vector(0, -g, 0) - k * (r - L * r.norm())

    # 운동량 및 위치 업데이트
    p = p + F * deltat
    ball.pos = ball.pos + (p / m) * deltat
    string.axis = ball.pos - ceiling.pos

    # 시간에 따른 각도(theta) 그래프 그리기
    theta = atan2(string.axis.x, -string.axis.y)
    anglegraph.plot(pos=(t, theta))

    t = t + deltat

    # 각도(theta) 업데이트
    theta = atan2(ball.pos.x - ceiling.pos.x, ceiling.pos.y - ball.pos.y)

