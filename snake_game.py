#from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1
                print("sss")

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()
               
               
####################################################
    SYMULACJA_SYGNALU = False
####################################################
    mac_adress = 'e5:32:b4:53:55:ba'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################
    import pygame,sys,time,random
    while True:
      
        # Difficulty settings
        # Easy      ->  10
        # Medium    ->  25
        # Hard      ->  40
        # Harder    ->  60
        # Impossible->  120
        difficulty = 4

        # Window size
        frame_size_x = 720
        frame_size_y = 480

        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors

        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


        # Colors (R, G, B)
        black = pygame.Color(0, 0, 0)
        white = pygame.Color(255, 255, 255)
        red = pygame.Color(255, 0, 0)
        green = pygame.Color(0, 255, 0)
        blue = pygame.Color(0, 0, 255)


        # FPS (frames per second) controller
        fps_controller = pygame.time.Clock()


        # Game variables
        snake_pos = [100, 50]
        snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        direction = 'RIGHT'
        change_to = direction

        score = 0


        # Game Over
        def game_over():
            my_font = pygame.font.SysFont('times new roman', 90)
            game_over_surface = my_font.render('YOU DIED', True, red)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
            game_window.fill(black)
            game_window.blit(game_over_surface, game_over_rect)
            show_score(0, red, 'times', 20)
            pygame.display.flip()
            time.sleep(3)
            pygame.quit()
            sys.exit()


        # Score
        def show_score(choice, color, font, size):
            score_font = pygame.font.SysFont(font, size)
            score_surface = score_font.render('Score : ' + str(score), True, color)
            score_rect = score_surface.get_rect()
            if choice == 1:
                    score_rect.midtop = (frame_size_x/10, 15)
            else:
                    score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
            game_window.blit(score_surface, score_rect)
            # pygame.display.flip()

        # Main logic
        while True:
            if blink.value==1:
                    blink.value=0
                    image = pygame.image.load(r'arrow.jpg')
                    game_window.blit(image, (0, 0))
                    pygame.display.update()
                    time.sleep(2)
                    if blink.value==1:
                            change_to = 'UP'
                            
                    else:
                            image = pygame.image.load(r'arrow2.jpg')
                            game_window.blit(image, (0, 0))
                            pygame.display.update()
                            time.sleep(2)
                            if blink.value==1:
                                    change_to = 'DOWN'
                                    
                            else:
                                    image = pygame.image.load(r'arrow.jpg')
                                    game_window.blit(image, (0, 0))
                                    pygame.display.update()
                                    time.sleep(2)
                                    if blink.value==1:
                                            change_to = 'LEFT'
                                            
                                    else:
                                            image = pygame.image.load(r'arrow2.jpg')
                                            game_window.blit(image, (0, 0))
                                            pygame.display.update()
                                            time.sleep(2)
                                            if blink.value==1:
                                                    change_to = 'RIGHT'
                                                    


            # Making sure the snake cannot move in the opposite direction instantaneously
            if change_to == 'UP' and direction != 'DOWN':
                    direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                    direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                    direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                    direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                    snake_pos[1] -= 10
            if direction == 'DOWN':
                    snake_pos[1] += 10
            if direction == 'LEFT':
                    snake_pos[0] -= 10
            if direction == 'RIGHT':
                    snake_pos[0] += 10

            # Snake body growing mechanism
            snake_body.insert(0, list(snake_pos))
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                    score += 1
                    food_spawn = False
            else:
                    snake_body.pop()

            # Spawning food on the screen
            if not food_spawn:
                    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            food_spawn = True

            # GFX
            game_window.fill(black)
            for pos in snake_body:
                    # Snake body
                    # .draw.rect(play_surface, color, xy-coordinate)
                    # xy-coordinate -> .Rect(x, y, size_x, size_y)
                    pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

            # Snake food
            pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

            # Game Over conditions
            # Getting out of bounds
            if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
                    game_over()
            if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
                    game_over()
            # Touching the snake body
            for block in snake_body[1:]:
                    if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                            game_over()

            show_score(1, white, 'consolas', 10)
            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            fps_controller.tick(difficulty)  


# Zakończenie podprocesów
    proc_blink_det.join()
