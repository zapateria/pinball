import pygame
import pymunk, pymunk.pygame_util
import random

FORCE = 30
PAD_SIZE = 12

class LeftFlipper:
    def __init__(self,space):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = (300,700)
        self.body.angle = 0.436332313
        l1 = pymunk.Segment(self.body, (0,0), (80,0), PAD_SIZE)
        space.add(self.body, l1)

    def up(self):
        self.body.angular_velocity = -FORCE

    def down(self):
        self.body.angular_velocity = FORCE

    def update(self):
        if self.body.angle <= -0.436332313:
            self.body.angular_velocity = 0
            self.body.angle = -0.436332313
        if self.body.angle >= 0.436332313:
            self.body.angle = 0.436332313 
            self.body.angular_velocity = 0

class RightFlipper:
    def __init__(self,space):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = (500,700)
        self.body.angle = -0.436332313
        l1 = pymunk.Segment(self.body, (0,0), (-80,0), PAD_SIZE)
        space.add(self.body, l1)

    def up(self):
        self.body.angular_velocity = FORCE

    def down(self):
        self.body.angular_velocity = -FORCE


    def update(self):
        if self.body.angle <= -0.436332313:
            self.body.angular_velocity = 0
            self.body.angle = -0.436332313
        if self.body.angle >= 0.436332313:
            self.body.angle = 0.436332313 
            self.body.angular_velocity = 0

class Map:

    def create_segment(self,coords):
        seg = pymunk.Segment(self.body, coords[0], coords[1], 4)
        seg.elasticity = 0.4
        seg.friction = 1
        return seg

    def create_target(self,coords):
        target = pymunk.Segment(self.body, coords[0], coords[1], 8)
        target.collision_type = 2
        target.elasticity = 2
        target.friction = 0.1
        return target
    
    def __init__(self,space):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = (0,0)
        space.add(self.body)
    
        walls = [
            ((100,600), (300, 700)),
            ((700,600), (500, 700))
        ]

        targets = [
            ((290,280), (310, 300)),
            ((280,220), (300, 210)),
            ((100,480), (120, 500)),
            
        ]
    
        segments = list(map(self.create_segment, walls))
        for s in segments:
            space.add(s)
        target_segments = list(map(self.create_target, targets))
        for s in target_segments:
            space.add(s)

        """
        l = pymunk.Segment(self.body, (100,600), (300, 700), 2)
        r = pymunk.Segment(self.body, (700,600), (500, 700), 2)
        l.elasticity = 0.5
        r.elasticity = 0.5
        space.add(self.body, l, r)
        """
        
class Wall:
    def __init__(self,space):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = (0,0)
        l1 = pymunk.Segment(self.body, (0, 0), (800, 0), 50) # top
        l3 = pymunk.Segment(self.body, (0, 0), (0, 800), 50) #left
        l4 = pymunk.Segment(self.body, (800, 0), (800, 800), 50) #right

        l1.friction = 1 
        l3.friction = 1 
        l4.friction = 1
        l3.elasticity = 1
        l4.elasticity = 1
        space.add(self.body, l1,l3,l4)


class Ball:
    def __init__(self,space):
        self.mass = 1
        self.radius = 15
        self.body = pymunk.Body() 
        x = random.randint(200, 600)
        self.body.position = x, 10 
        shape = pymunk.Circle(self.body, self.radius) 
        shape.mass = self.mass 
        shape.friction = 0.2
        shape.elasticity = 1
        shape.collision_type = 1
        space.add(self.body, shape) 
        ch = space.add_collision_handler(1, 2)
        ch.post_solve = self.hit
    
    def hit(self, space, arbiter, data):
        print("hit")

    def draw(self,screen):
        pygame.draw.circle(screen, (0,0,255), self.body.position, int(self.radius), 2)

class Game:
    def __init__(self, title = "Noname"):
        self.WIDTH=800
        self.HEIGHT=900
        self.TITLE = title
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def start_game(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        clock = pygame.time.Clock()

        space = pymunk.Space()
        space.gravity = (0.0, 900.0)

        self.floor = Wall(space)
        self.map = Map(space)
        self.left_flipper = LeftFlipper(space)
        self.right_flipper = RightFlipper(space)
        self.ball = Ball(space)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.left_flipper.up()
                if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    self.left_flipper.down()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.right_flipper.up()
                if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                    self.right_flipper.down()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ball = Ball(space)
         
                    

            space.step(1/100.0)        
            self.screen.fill((0,0,0))
            self.update()
#            self.render()
            space.debug_draw(self.draw_options)
            pygame.display.flip()
            clock.tick(100)

    def update(self):
        self.left_flipper.update()
        self.right_flipper.update()
        
    def render(self):
        self.ball.draw(self.screen)
        self.floor.draw(self.screen)