import pygame
import numpy as np
import pickle

# โหลดโมเดลที่ถูกฝึก
with open('hypertension_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# เริ่มต้นใช้งาน Pygame
pygame.init()

# การตั้งค่าหน้าจอ
screen = pygame.display.set_mode((800, 900))
pygame.display.set_caption("Hypertension Risk Prediction")

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# ฟังก์ชันสำหรับแสดงข้อความบนหน้าจอ
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# ฟังก์ชันสำหรับรับค่าจากผู้ใช้ในรูปแบบ Yes/No
def yes_no_input(prompt, x, y):
    font = pygame.font.Font(None, 36)
    done = False
    response = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    response = 1  # Yes = 1
                    done = True
                elif no_button.collidepoint(event.pos):
                    response = 0  # No = 0
                    done = True

        screen.fill(BLACK)  # พื้นหลังสีดำ
        draw_text(prompt, font, WHITE, screen, x - 200, y)  # ข้อความสีขาว
        yes_button = pygame.Rect(x, y + 50, 100, 50)
        no_button = pygame.Rect(x + 150, y + 50, 100, 50)

        pygame.draw.rect(screen, GREEN, yes_button)
        pygame.draw.rect(screen, RED, no_button)

        draw_text("Yes", font, BLACK, screen, x + 20, y + 60)
        draw_text("No", font, BLACK, screen, x + 170, y + 60)

        pygame.display.flip()

    return response

# ฟังก์ชันสำหรับรับค่าตัวเลข
def get_input(prompt, x, y):
    input_box = pygame.Rect(x, y + 50, 140, 32)  # กล่องข้อความอยู่ใต้ข้อความที่แสดง
    font = pygame.font.Font(None, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)  # พื้นหลังสีดำ
        draw_text(prompt, font, WHITE, screen, x - 150, y)  # ข้อความสีขาว

        # แสดงข้อความที่กำลังป้อนอยู่
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

# ลูปหลัก
running = True
font = pygame.font.SysFont(None, 30)

while running:
    screen.fill(BLACK)

    # รับข้อมูลจากผู้ใช้
    male = yes_no_input("Are you male?", 250, 50)
    age = int(get_input("Age:", 250, 120))
    currentSmoker = yes_no_input("Do you currently smoke?", 250, 190)
    cigsPerDay = int(get_input("Cigarettes per day:", 250, 260)) if currentSmoker == 1 else 0
    BPMeds = yes_no_input("Are you on BP medication?", 250, 330)
    diabetes = yes_no_input("Do you have diabetes?", 250, 400)
    totChol = float(get_input("Total Cholesterol:", 250, 470))
    sysBP = float(get_input("Systolic BP:", 250, 540))
    diaBP = float(get_input("Diastolic BP:", 250, 610))
    BMI = float(get_input("BMI:", 250, 680))
    heartRate = int(get_input("Heart Rate:", 250, 750))
    glucose = float(get_input("Glucose:", 250, 800))

    # ใช้ข้อมูลที่ได้รับเพื่อทำนาย
    new_data = np.array([[male, age, currentSmoker, cigsPerDay, BPMeds, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose]])
    print(new_data)
    predicted_risk = model.predict(new_data)
    print(predicted_risk)
    
    # แสดงผลลัพธ์
    if predicted_risk[0] == 1:
        print("Predicted Risk: High risk of hypertension")
    else:
        print("Predicted Risk: Low risk of hypertension")

    # แสดงผลการทำนายบนหน้าจอ
    result_text = f"Hypertension Risk: {'High' if predicted_risk[0] == 1 else 'Low'}"
    screen.fill(BLACK)
    draw_text(result_text, font, WHITE, screen, 300, 300)
    draw_text("Click to continue", font, GREEN, screen, 300, 400)  # แสดงข้อความให้คลิกเพื่อทำงานต่อ

    pygame.display.update()

    # รอให้คลิกก่อนที่จะเริ่มลูปใหม่
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_click = False

pygame.quit()
