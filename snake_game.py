import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置窗口大小和标题
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 设置时钟
CLOCK = pygame.time.Clock()
FPS = 15

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 蛇的初始位置和大小
SNAKE_SIZE = 20

# 确保中文正常显示
pygame.font.init()
font_options = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial"]
FONT = None
for font_name in font_options:
    if font_name in pygame.font.get_fonts() or font_name.lower() in [f.lower() for f in pygame.font.get_fonts()]:
        FONT = pygame.font.SysFont(font_name, 36)
        break
if FONT is None:
    FONT = pygame.font.SysFont(None, 36)

class SnakeGame:
    def __init__(self):
        self.reset_game()
        self.score = 0
        self.high_score = 0
        self.game_state = "START"
    
    def reset_game(self):
        # 初始化蛇的位置和方向
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        
        # 初始化食物位置
        self.food_position = self.generate_food()
        self.food_spawn = True
    
    def generate_food(self):
        # 生成食物位置，确保不会出现在蛇身上
        while True:
            position = [
                random.randrange(1, (WINDOW_WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (WINDOW_HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE
            ]
            # 检查是否与蛇身重叠
            if position not in self.snake_body:
                return position
    
    def handle_events(self):
        # 处理用户输入事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 游戏开始界面
                if self.game_state == "START":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "PLAYING"
                # 游戏进行中
                elif self.game_state == "PLAYING":
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.change_to = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.change_to = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.change_to = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.change_to = "RIGHT"
                    elif event.key == pygame.K_p:
                        self.game_state = "PAUSED"
                        # 确保暂停状态立即生效
                        print("游戏已暂停")
                # 游戏暂停
                elif self.game_state == "PAUSED":
                    if event.key == pygame.K_p:
                        self.game_state = "PLAYING"
                    elif event.key == pygame.K_r:
                        self.game_state = "START"
                        self.reset_game()
                # 游戏结束
                elif self.game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.game_state = "START"
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    
    def update_game_state(self):
        if self.game_state != "PLAYING":
            return
        
        # 更新蛇的方向
        self.direction = self.change_to
        
        # 更新蛇头位置
        if self.direction == "UP":
            self.snake_position[1] -= SNAKE_SIZE
        elif self.direction == "DOWN":
            self.snake_position[1] += SNAKE_SIZE
        elif self.direction == "LEFT":
            self.snake_position[0] -= SNAKE_SIZE
        elif self.direction == "RIGHT":
            self.snake_position[0] += SNAKE_SIZE
        
        # 蛇头移动到屏幕另一端
        if self.snake_position[0] < 0:
            self.snake_position[0] = WINDOW_WIDTH - SNAKE_SIZE
        elif self.snake_position[0] >= WINDOW_WIDTH:
            self.snake_position[0] = 0
        if self.snake_position[1] < 0:
            self.snake_position[1] = WINDOW_HEIGHT - SNAKE_SIZE
        elif self.snake_position[1] >= WINDOW_HEIGHT:
            self.snake_position[1] = 0
        
        # 将蛇头添加到蛇身体的最前面
        self.snake_body.insert(0, list(self.snake_position))
        
        # 检测是否吃到食物（使用矩形碰撞检测，更可靠）
        snake_head_rect = pygame.Rect(self.snake_position[0], self.snake_position[1], SNAKE_SIZE, SNAKE_SIZE)
        food_rect = pygame.Rect(self.food_position[0], self.food_position[1], SNAKE_SIZE, SNAKE_SIZE)
        
        if snake_head_rect.colliderect(food_rect):
            self.score += 1
            self.food_spawn = False
        else:
            # 如果没吃到食物，移除蛇尾
            self.snake_body.pop()
        
        # 生成新的食物
        if not self.food_spawn:
            self.food_position = self.generate_food()
            self.food_spawn = True
        
        # 检测碰撞
        self.check_collision()
        
        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
    
    def check_collision(self):
        # 检测是否撞到自己的身体
        for block in self.snake_body[1:]:
            if self.snake_position == block:
                self.game_state = "GAME_OVER"
                return
    
    def draw_game(self):
        # 填充背景色
        WINDOW.fill(BLACK)
        
        if self.game_state == "START":
            # 显示开始界面
            title_text = FONT.render("贪吃蛇游戏", True, GREEN)
            start_text = FONT.render("按空格键开始游戏", True, WHITE)
            instruction_text = FONT.render("使用方向键控制蛇的移动", True, WHITE)
            pause_text = FONT.render("按P键暂停游戏", True, WHITE)
            
            WINDOW.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 150))
            WINDOW.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, 220))
            WINDOW.blit(instruction_text, (WINDOW_WIDTH // 2 - instruction_text.get_width() // 2, 270))
            WINDOW.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, 320))
        
        elif self.game_state == "PLAYING":
            # 绘制蛇
            for pos in self.snake_body:
                pygame.draw.rect(WINDOW, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
            # 绘制蛇头
            pygame.draw.rect(WINDOW, BLUE, pygame.Rect(self.snake_position[0], self.snake_position[1], SNAKE_SIZE, SNAKE_SIZE))
            # 绘制食物
            pygame.draw.rect(WINDOW, RED, pygame.Rect(self.food_position[0], self.food_position[1], SNAKE_SIZE, SNAKE_SIZE))
            # 显示分数和最高分
            score_text = FONT.render(f"分数: {self.score}", True, WHITE)
            high_score_text = FONT.render(f"最高分: {self.high_score}", True, WHITE)
            WINDOW.blit(score_text, (10, 10))
            WINDOW.blit(high_score_text, (10, 50))
        
        elif self.game_state == "PAUSED":
            # 显示暂停界面
            pause_text = FONT.render("游戏暂停", True, WHITE)
            continue_text = FONT.render("按P键继续游戏", True, WHITE)
            restart_text = FONT.render("按R键重新开始", True, WHITE)
            
            WINDOW.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, 200))
            WINDOW.blit(continue_text, (WINDOW_WIDTH // 2 - continue_text.get_width() // 2, 250))
            WINDOW.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 300))
        
        elif self.game_state == "GAME_OVER":
            # 显示游戏结束界面
            game_over_text = FONT.render("游戏结束", True, RED)
            score_text = FONT.render(f"最终分数: {self.score}", True, WHITE)
            high_score_text = FONT.render(f"最高分: {self.high_score}", True, WHITE)
            restart_text = FONT.render("按R键重新开始", True, WHITE)
            quit_text = FONT.render("按Q键退出游戏", True, WHITE)
            
            WINDOW.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 150))
            WINDOW.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 220))
            WINDOW.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, 260))
            WINDOW.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 300))
            WINDOW.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, 340))
        
        # 更新显示
        pygame.display.update()
    
    def run(self):
        # 游戏主循环
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw_game()
            CLOCK.tick(FPS)

# 主函数
if __name__ == "__main__":
    game = SnakeGame()
    game.run()