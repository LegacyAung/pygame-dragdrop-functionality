import pygame
import os
import sys


SCREEN_SIZE = (1100,720)
WHITE = (255,255,255)
CYAN_BLUE = (79, 247, 217)
GREEN =(64, 247, 192)
FPS = 60
RECT = pygame.Rect(0,0,250,720)
SCALED_WIDTH = 76
SCALED_HEIGHT = 76

#Load images
dir_path = 'assets'
img_load = []
img_rect_array = []
img_dictOrder = []

#Create the drop area
drop_area_rect = pygame.Rect(525,210,300,300)


#pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Build a PC")


#Loaded images and transform size
def load_images(dir_path):
    read_imgArray = os.listdir(dir_path)

    
    for img in read_imgArray:
        
        image_load = pygame.image.load(os.path.join(dir_path,img))
        
        #downsize the image by scale factor of 0.15
        new_width = int(image_load.get_width() * 0.15)
        new_height = int(image_load.get_height() * 0.15)
        
        scaled_img = pygame.transform.scale(image_load,(new_width, new_height))
        img_str_without_extension = img.replace('.png','')
        img_dict = {
            'name': img_str_without_extension,
            'obj': scaled_img,
        }
        img_load.append(img_dict)




#FUNCTIONS AND MAIN

#Image Rectangle and append to img_rect_array
def rect_arrayImg(scaled_width,scaled_height):
    num = 0
    width = 80
    height = 50 
    while num <= 7:
        img_array = pygame.Rect(width,height,scaled_width,scaled_height)
        img_rect_array.append(img_array)
        height+=80
        num+=1
rect_arrayImg(SCALED_WIDTH,SCALED_HEIGHT)


load_images(dir_path)

#BLit images
def blit_img(img_array):
    for img,dim in zip(img_array,img_rect_array):
        screen.blit(img['obj'],(dim.x,dim.y))
        
#Display images 
def display():
    #display screen
    screen.fill(WHITE)
    pygame.draw.rect(screen,CYAN_BLUE,RECT,border_radius=0,border_top_left_radius=0,border_top_right_radius=20, border_bottom_left_radius=0, border_bottom_right_radius=20)
    pygame.draw.rect(screen,GREEN,drop_area_rect,border_radius=10)

    #-------blit images on screen--------#
    blit_img(img_load)
    pygame.display.update()
    clock.tick(FPS)



drag_item = [False] * len(img_rect_array)
offsets = [(0,0) for _ in img_rect_array]

for img,img_rect in zip(img_load,img_rect_array):
    img_dict = {
        'name':img['name'],
        'img_rect':img_rect
    }
    img_dictOrder.append(img_dict)

for img in img_dictOrder:
    if img['name'] == 'computer-case':
        img.update({'order_no': 0})
    elif img['name'] == 'motherboard':
        img.update({'order_no': 1})
    elif img['name'] == 'cpu':
        img.update({'order_no': 2})
    elif img['name'] == 'ram':
        img.update({'order_no': 3})
    elif img['name'] == 'gpu':
        img.update({'order_no': 4})
    elif img['name'] == 'harddisk':
        img.update({'order_no': 5})
    elif img['name'] == 'power-supply':
        img.update({'order_no': 6})
    else:
        img.update({'order_no': 7})


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i,img in enumerate(img_rect_array):
                        if img.collidepoint(event.pos):
                            drag_item[i] = True
                            offsets[i] = (img.x - event.pos[0], img.y - event.pos[1])
                           
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    
                            
                    for i,image in enumerate(img_rect_array):
                        drag_item[i] = False
                        for img in img_dictOrder:
                            if img_rect_array[i].colliderect(drop_area_rect):
                                if img['order_no'] == i:
                                    img_rect_array[i].x = -SCALED_WIDTH  
                                    img_rect_array[i].y = -SCALED_HEIGHT
                               

            for i in range(len(img_rect_array)):
                if drag_item[i]:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    new_x = mouse_x + offsets[i][0]
                    new_y = mouse_y + offsets[i][1]
                    img_rect_array[i].x = max(0, min(new_x, SCREEN_SIZE[0] - SCALED_WIDTH))
                    img_rect_array[i].y = max(0, min(new_y, SCREEN_SIZE[1] - SCALED_HEIGHT))

                    

        display()
    



if __name__ == "__main__":
    main()


