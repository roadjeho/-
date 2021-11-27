import random
import pygame

pygame.init()

#화면 크기 설정
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("new game")

#FPS 설정
clock = pygame.time.Clock()

#배경이미지 불러오기
background = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/background.png")
jungle = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/jungle.png")                               

#엔딩이미지 불러오기
ending = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/ending.png")
cel1 = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/celebration.png")
cel2 = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/celebration 2.png")

#오브젝트 불러오기
character = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/deer.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 6) - (character_width)
character_y_pos = (screen_height / 2) - (character_height / 2)

obstacle = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/trap.png")
obstacle_size = obstacle.get_rect().size
obstacle_width = obstacle_size[0]
obstacle_height = obstacle_size[1]
obstacle_x_pos = screen_width
obstacle_y_pos = random.randint(0, screen_height - obstacle_height)
obstacle_speed = 8

rf = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/rotten_apple1.png")
rf_size = rf.get_rect().size
rf_width = rf_size[0]
rf_height = rf_size[1]
rf_x_pos = screen_width
rf_y_pos = random.randint(0, screen_height - rf_height)
rf_speed = 7
rf_weight = 5

ff = pygame.image.load("C:/Users/IBK/OneDrive/사진/Saved Pictures/fresh_apple1.png")
ff_size = ff.get_rect().size
ff_width = ff_size[0]
ff_height = ff_size[1]
ff_x_pos = screen_width
ff_y_pos = random.randint(0, screen_height - ff_height)
ff_speed = 6
ff_weight = 3

#이동 좌표
to_x = 0
to_y = 0

#폰트 정하기
game_font = pygame.font.Font(None, 40) # (폰트, 크기)

#게임 시간
total_time = 61

#시작 시간
start_ticks = pygame.time.get_ticks() #시작시간, 현재시

#무게(점수) 변수 추가
total_weight = 15


#게임 진행
running = True
while running:
    dt = clock.tick(60)
    
    
    for event in pygame.event.get():    #이벤트 발생
        if event.type == pygame.QUIT:   # 창닫기
            running = False             #게임종료

        if event.type == pygame.KEYDOWN:       #키보드 입력 
            if event.key == pygame.K_UP:       
                to_y += 10
            elif event.key == pygame.K_DOWN:    
                to_y -= 10
            
        if event.type == pygame.KEYUP:         #키보드 입력 중지
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    #오브젝트 위치 정의, 화면 이탈 제어
    character_x_pos += to_x
    character_y_pos -= to_y

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    obstacle_x_pos -= obstacle_speed  #장애물 이동

    if obstacle_x_pos < 0:
        obstacle_x_pos = screen_width
        obstacle_y_pos = random.randint(0, screen_height - obstacle_height)#(반복)

    rf_x_pos -= rf_speed  # -요소 이동

    if rf_x_pos < 0:
        rf_x_pos = screen_width 
        rf_y_pos = random.randint(0, screen_height - rf_height)
        
    ff_x_pos -= ff_speed  #+요소 이동

    if ff_x_pos < 0:
        ff_x_pos = screen_width 
        ff_y_pos = random.randint(0, screen_height - ff_height)

    #게임 종료
    #시간 종료시 (성공)
    #장애물 충돌시 (실패)


    #충돌 처리용 rect 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    obstacle_rect = obstacle.get_rect()
    obstacle_rect.left = obstacle_x_pos
    obstacle_rect.top = obstacle_y_pos

    rf_rect = rf.get_rect()
    rf_rect.left = rf_x_pos
    rf_rect.top = rf_y_pos

    ff_rect = ff.get_rect()
    ff_rect.left = ff_x_pos
    ff_rect.top = ff_y_pos


    #충돌체크
    if character_rect.colliderect(obstacle_rect):
        running = False

    if character_rect.colliderect(rf_rect):
        rf_x_pos = screen_width 
        rf_y_pos = random.randint(0, screen_height - rf_height)
        total_weight -= rf_weight 

    if character_rect.colliderect(ff_rect):
        ff_x_pos = screen_width 
        ff_y_pos = random.randint(0, screen_height - ff_height)
        total_weight += ff_weight

#배경, 오브젝트 그리기
    screen.blit(background,(0, 0))

    screen.blit(jungle, (0,0))

    screen.blit(character, (character_x_pos, character_y_pos))

    screen.blit(obstacle, (obstacle_x_pos, obstacle_y_pos))

    screen.blit(rf, (rf_x_pos, rf_y_pos))

    screen.blit(ff, (ff_x_pos, ff_y_pos))

    #타이머 추가
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #초로 표시 ms to s

    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    # 출력 문자, True, 글자 색상

    screen.blit(timer, (10, 10))

    #무게(점수) 추가
    score = game_font.render(str(int(total_weight)), True, (255, 255, 255))

    screen.blit(score,(750,10))


    #시간이 0이하면 종료
    if total_time - elapsed_time <= 0:
        running = False

    #점수가 0이하면 종료
    if total_weight <= 0:
        running = False
        
    pygame.display.update() # 게임화면 다시 그리기 Update

#종료 전 대기
screen.blit(ending,(0, 0))

if total_time - elapsed_time <= 0:
    complete = game_font.render(("Missoin Complete"), True, (255, 255, 255))
    txt1 = game_font.render(("weight:"), True, (255, 255, 255))
    screen.blit(cel1, (0, 400))
    screen.blit(cel2, (700, 400))
    screen.blit(complete, (280, 100))
    screen.blit(score, (440, 250))
    screen.blit(txt1, (300, 250))

elif total_weight <= 0:
    game_over = game_font.render(("Game Over..."), True, (255, 255, 255))
    txt1 = game_font.render(("weight:"), True, (255, 255, 255))
    screen.blit(game_over, (300, 100))
    screen.blit(score, (440,250))
    screen.blit(txt1, (300, 250))

elif character_rect.colliderect(obstacle_rect):
    game_over = game_font.render(("Game Over..."), True, (255, 255, 255))
    txt1 = game_font.render(("weight:"), True, (255, 255, 255))
    screen.blit(game_over, (300, 100))
    screen.blit(score, (440,250))
    screen.blit(txt1, (300, 250))

elif event.type == pygame.QUIT:
    txt2 = game_font.render(("Good Bye!"), True, (255, 255, 255))
    screen.blit(txt2, (330,100))

pygame.display.update()
pygame.time.delay(4000)

pygame.quit()
