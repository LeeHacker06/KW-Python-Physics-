from vpython import *

## 상수
g = 9.8 # 중력 가속도
t = 0  # 시간 시작점
deltat = 0.001  # 시간 간격

# 첫 번째 물체의 시작 각도, 줄의 길이, 질량, 운동량
theta1 = 1.2  # 시작 각도 (radian)
L1 = 0.8  # 줄의 길이
m1 = 0.1  # 물체 질량 (kg)
p1 = m1 * vector(0, 0, 0)  # 시작 운동량

# 두 번째 물체의 시작 각도, 줄의 길이, 질량, 운동량
theta2 = 3.8  # 시작 각도 (radian)
L2 = 0.8  # 줄의 길이
m2 = 0.1  # 물체 질량 (kg)
p2 = m2 * vector(0, 0, 0)  # 시작 운동량

# 줄을 아주 큰 k로 취급하여 스프링처럼 취급
k = 1e5

## 천장, 물체, 줄 생성
ceiling = box(pos=vector(-0.5, 1, 0), size=vector(0.01, 0.01, 0.01))
ball1 = sphere(pos=vector(ceiling.pos.x + L1 * sin(theta1), ceiling.pos.y - L1 * cos(theta1), 0), radius=0.05,
               color=color.red, make_trail=True, interval=40, retain=1e4)
ball2 = sphere(
    pos=vector(ceiling.pos.x + L1 * sin(theta1) + L2 * sin(theta2), ceiling.pos.y - L1 * cos(theta1) - L2 * cos(
        theta2), 0), radius=0.05, color=color.blue, make_trail=True, interval=20, retain=1e4)
string1 = cylinder(pos=ceiling.pos, axis=ball1.pos - ceiling.pos, color=color.white, radius=0.008)
string2 = cylinder(pos=ball1.pos, axis=ball2.pos - ball1.pos, color=color.white, radius=0.008)

# 그래프 설정
scene1 = graph(title='1번 진자 운동', xtitle='시간 (초)', ytitle='Theta (라디안)')
theta1_graph = gcurve(color=color.red, graph=scene1)
scene1.width = 1500  # 그래프 너비 조정

scene2 = graph(title='2번 진자 운동', xtitle='시간 (초)', ytitle='Theta (라디안)')
theta2_graph = gcurve(color=color.blue, graph=scene2)
scene2.width = 1500  # 그래프 너비 조정

## 계산 루프
while t < 1e2:
    rate(1 / deltat)

    # 방사형 벡터 및 힘 계산
    r1 = vector(ball1.pos.x - ceiling.pos.x, ball1.pos.y - ceiling.pos.y, ball1.pos.z - ceiling.pos.z)
    r2 = vector(ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y, ball2.pos.z - ball1.pos.z)
    F1 = m1 * vector(0, -g, 0) - k * (r1 - L1 * r1.norm()) + k * (r2 - L2 * r2.norm())
    F2 = m2 * vector(0, -g, 0) - k * (r2 - L2 * r2.norm())

    # 운동량 및 위치 업데이트
    p1 = p1 + F1 * deltat
    ball1.pos = ball1.pos + (p1 / m1) * deltat
    string1.axis = ball1.pos - ceiling.pos

    p2 = p2 + F2 * deltat
    ball2.pos = ball2.pos + (p2 / m2) * deltat
    string2.axis = ball2.pos - ball1.pos
    string2.pos = ball1.pos

    # 시간에 따른 각도(theta) 저장 및 그래프 그리기
    theta1 = atan2(string1.axis.x, -string1.axis.y)
    theta2 = atan2(string2.axis.x, -string2.axis.y)
    theta1_graph.plot(pos=(t, theta1))
    theta2_graph.plot(pos=(t, theta2))

    t += deltat

