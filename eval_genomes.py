import pygame
import random
import math
import neat, os
from pygame import mixer
# initailise game
pygame.init()

def eval_genomes(genomes, config):

    # create screen
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Space Invaders')
    icon = pygame.image.load('transport.png')
    pygame.display.set_icon(icon)
    background = pygame.image.load('background.png')

    mixer.music.load('background.wav')
    mixer.music.play(-1)

    ge = []
    nets = []
    for genome_id, genome in genomes:
        # Bird.birds.append(Bird(SCREEN_WIDTH //2, SCREEN_HEIGHT//2, Bird.COLORS[genome_id % 6]))
        ge.append(genome)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

    
    # player
    playerimg = pygame.image.load('gaming.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    # enemy
    enemyimg =[]
    enemyX =[]
    enemyY = []
    enemyX_change =[]
    enemyY_change =[]
    enemynum = 6

    for i in range(enemynum):
        enemyimg.append(pygame.image.load('avatar.png'))
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    # enemy
    bulletimg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = 'ready'

    # score 
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10
    overfont = pygame.font.Font('freesansbold.ttf', 64)
    def game_over():
        overscore = overfont.render('GAME OVER', True, (255,255,255))
        screen.blit(overscore, (200,250))	

    def show_score(x,y):
        score = font.render('Score : ' + str(score_value), True, (255,255,255))
        screen.blit(score, (x,y))

    def player(x,y):
        screen.blit(playerimg, (x,y))

    def enemy(x,y,i):
        screen.blit(enemyimg[i], (x,y))

    def shoot(x,y):
        global bullet_state
        bullet_state = 'fire'
        screen.blit(bulletimg, (x + 16, y + 10))

    def iscollision(enemyX, enemyY, bulletX, bulletY):
        dist = math.sqrt(math.pow((enemyX-bulletX),2) + math.pow((enemyY-bulletY),2))
        if dist < 27:
            return True
        else:
            return False


    #game loop
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN:
            #     print('a keystroke is pressed')
            #     if event.key == pygame.K_LEFT:
            #         print('left key down')
            #         playerX_change = -5
            #     if event.key == pygame.K_RIGHT:
            #         print('right key down')
            #         playerX_change = 5
            #     if event.key == pygame.K_SPACE:
            #         if bullet_state == 'ready':
            #             print('space bar down')
            #             bulletX = playerX
            #             shoot(bulletX, bulletY)
            #             mixer.Sound('laser.wav').play()
            # if event.type ==  pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         print('keystroke is released')
            #         playerX_change = 0
        output = nets[0].activate((playerX, enemyX[0], enemyY[0]))
        if output[0] > 0.5:
            playerX_change = 5
        if output[1] > 0.5:
            playerX_change = -5
        if output[2] > 0.5:
            shoot(bulletX, bulletY)


        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(enemynum):
            #gameover
            if enemyY[i] >=440:
                for j in range(enemynum):
                    enemyY[j] = 2000
                game_over()

            enemy(enemyX[i], enemyY[i], i)

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX[i] = 0
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]

            elif enemyX[i] >= 736:
                enemyX[i] = 736
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            #collision

            collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)

            if collision:
                bulletY = 480
                bullet_state = 'ready'
                enemyX[i] = random.randint(0,736)
                enemyY[i] = random.randint(50,150)
                score_value += 1
                mixer.Sound('explosion.wav').play()
                




        #bullet
        if bulletY <= 0:
            bullet_state = 'ready'
            bulletY = 480

        if bullet_state == 'fire':
            shoot(bulletX,bulletY)
            bulletY -= bulletY_change




        show_score(textX, textY)
        player(playerX,playerY)
        
        pygame.display.update()

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

if __name__ == "__main__":
    # main()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
    # run("./config.text")
    # eval_genomes()