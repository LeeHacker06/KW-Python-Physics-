from vpython import *

## 상수
g = 9.8        # 중력 가속도
t = 0          # 시간 시작점
deltat = 0.001 # 시간 간격


# 각 개체의 시작 각도, 줄의 길이, 질량, 운동량
theta1 = 1.2   # 첫 번째 진자의 시작 각도 (라디안)
L1 = 0.8       # 첫 번째 진자의 줄의 길이
m1 = 0.1       # 첫 번째 진자의 질량 (kg)
p1 = m1 * vector(0, 0, 0)  # 첫 번째 진자의 시작 운동량

theta2 = 3.8   # 두 번째 진자의 시작 각도 (라디안)
L2 = 0.8       # 두 번째 진자의 줄의 길이
m2 = 0.1       # 두 번째 진자의 질량 (kg)
p2 = m2 * vector(0, 0, 0)  # 두 번째 진자의 시작 운동량

theta3 = 2.0   # 세 번째 진자의 시작 각도 (라디안)
L3 = 0.8       # 세 번째 진자의 줄의 길이
m3 = 0.1       # 세 번째 진자의 질량 (kg)
p3 = m3 * vector(0, 0, 0)  # 세 번째 진자의 시작 운동량

# 줄을 긴장시키기 위해 줄을 아주 큰 k로 취급
k = 1e5

## 천장, 진자, 줄 생성
ceiling = box(pos=vector(-0.5, 1, 0), size=vector(0.01, 0.01, 0.01))

# 첫 번째 진자
ball1 = sphere(pos=vector(ceiling.pos.x + L1 * sin(theta1), ceiling.pos.y - L1 * cos(theta1), 0), radius=0.05, color=color.red, make_trail=True, interval=40, retain=1e4)
string1 = cylinder(pos=ceiling.pos, axis=ball1.pos - ceiling.pos, color=color.red, radius=0.008)

# 두 번째 진자
ball2 = sphere(pos=vector(ball1.pos.x + L2 * sin(theta2), ball1.pos.y - L2 * cos(theta2), 0), radius=0.05, color=color.blue, make_trail=True, interval=20, retain=1e4)
string2 = cylinder(pos=ball1.pos, axis=ball2.pos - ball1.pos, color=color.white, radius=0.008)

# 세 번째 진자
ball3 = sphere(pos=vector(ball2.pos.x + L3 * sin(theta3), ball2.pos.y - L3 * cos(theta3), 0), radius=0.05, color=color.green, make_trail=True, interval=20, retain=1e4)
string3 = cylinder(pos=ball2.pos, axis=ball3.pos - ball2.pos, color=color.blue, radius=0.008)

# 그래프 설정
oscillation1 = graph(title='1번 진자의 운동', xtitle='시간 (초)', ytitle='각도 (라디안)')
angle1_graph = gcurve(color=color.red, graph=oscillation1)  # 1번 진자의 각도 그래프
oscillation1.width = 1500

oscillation2 = graph(title='2번 진자의 운동', xtitle='시간 (초)', ytitle='각도 (라디안)')
angle2_graph = gcurve(color=color.blue, graph=oscillation2)  # 2번 진자의 각도 그래프
oscillation2.width = 1500

oscillation3 = graph(title='3번 진자의 운동', xtitle='시간 (초)', ytitle='각도 (라디안)')
angle3_graph = gcurve(color=color.green, graph=oscillation3)  # 3번 진자의 각도 그래프
oscillation3.width = 1500

## 계산 루프
while t < 1e2:
    rate(1 / deltat)

    # 각 진자의 방사형 벡터와 힘 계산
    r1 = vector(ball1.pos.x - ceiling.pos.x, ball1.pos.y - ceiling.pos.y, ball1.pos.z - ceiling.pos.z)
    r2 = vector(ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y, ball2.pos.z - ball1.pos.z)
    r3 = vector(ball3.pos.x - ball2.pos.x, ball3.pos.y - ball2.pos.y, ball3.pos.z - ball2.pos.z)

    F1 = m1 * vector(0, -g, 0) - k * (r1 - L1 * r1.norm()) + k * (r2 - L2 * r2.norm())
    F2 = m2 * vector(0, -g, 0) - k * (r2 - L2 * r2.norm()) + k * (r3 - L3 * r3.norm())
    F3 = m3 * vector(0, -g, 0) - k * (r3 - L3 * r3.norm())

    # 각 진자의 운동량 및 위치 업데이트
    p1 = p1 + F1 * deltat
    ball1.pos = ball1.pos + (p1 / m1) * deltat
    string1.axis = ball1.pos - ceiling.pos

    p2 = p2 + F2 * deltat
    ball2.pos = ball2.pos + (p2 / m2) * deltat
    string2.axis = ball2.pos - ball1.pos
    string2.pos = ball1.pos

    p3 = p3 + F3 * deltat
    ball3.pos = ball3.pos + (p3 / m3) * deltat
    string3.axis = ball3.pos - ball2.pos
    string3.pos = ball2.pos

    # 각도 계산
    theta1 = atan2(string1.axis.x, -string1.axis.y)
    theta2 = atan2(string2.axis.x, -string2.axis.y)
    theta3 = atan2(string3.axis.x, -string3.axis.y)

    # 그래프에 각도 그리기
    angle1_graph.plot(pos=(t, theta1))
    angle2_graph.plot(pos=(t, theta2))
    angle3_graph.plot(pos=(t, theta3))

    t = t + deltat

