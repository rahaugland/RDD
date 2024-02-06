import os 
import cv2 
from VOC_to_YOLO import convert

dirs = ['train', 'validate']
classes = ['D00', 'D10', 'D20', 'D40']


def getImagesInDir(dir_path: str):
    image_list = []
    for root, dirs, files in os.walk(os.path.join(dir_path, 'images')):
        for filename in files:
            if filename.lower().endswith('.jpg'):
                image_list.append(os.path.join(root, filename))
    return image_list


def split_img(img_path:str,label_path:str, reduce_factor:tuple[int,int], output_folder_img:str,output_folder_label:str, show=False):
    image = cv2.imread(img_path)
    img_height, img_width, img_channels = image.shape
    output_height = img_height//reduce_factor[0]
    output_width = img_width//reduce_factor[1]

    label = open(label_path, "r").read()
    labels = label.split("\n")[:2]
    resized_labels= []
    for l in labels:
        class_id, x_center, y_center, box_width, box_height = map(float, l.split())
        x_center, y_center, box_width, box_height = (
                    x_center * img_width,
                    y_center * img_height,
                    box_width * img_width,
                    box_height * img_height
                )
        x1 = int((x_center - box_width // 2))
        y1 = int((y_center - box_height // 2))
        x2 = int((x_center + box_width // 2))
        y2 = int((y_center + box_height // 2))
        resized_labels.append(f"{int(class_id)} {x_center} {y_center} {box_width} {box_height} {x1} {y1} {x2} {y2}")
        

        # Draw the rectangle on the image
        #cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #cv2.imshow("Image with Bounding Boxes", cv2.resize(image, (720,1024)))
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    print(resized_labels)
    sub_images = []
    
    for i in range(reduce_factor[0]):
        start_row = i*output_height
        end_row = start_row + output_height

        for k in range(reduce_factor[1]):
            start_col = k*output_width
            end_col = start_col+output_width

            sub_img = image[start_row:end_row, start_col:end_col, :]
            sub_images.append(sub_img)

            image_filename = os.path.basename(img_path)    
            sub_img_filename = f"{os.path.splitext(image_filename)[0]}_{i * reduce_factor[1] + k + 1}.jpg"
            sub_img_path = os.path.join(output_folder_img, sub_img_filename)
            sub_label_filename = f"{os.path.splitext(image_filename)[0]}_{i * reduce_factor[1] + k + 1}.txt"
            sub_label_path = os.path.join(outpout_folder_label, sub_label_filename)
            h,w, _ = sub_img.shape
            with open(sub_label_path, 'w') as file:
                #print(f'current img placement :  Y: {start_row}:{end_row}, X: {start_col}:{end_col}')
                for lable in resized_labels:
                    class_id, x_center, y_center, box_width, box_height, x1, y1, x2, y2 =  map(float, lable.split())
                    if (start_row <= y1 <= end_row and 
                        start_row <= y2 <= end_row and
                        start_col <= x1 <= end_col and
                        start_col <= x2 <= end_col): #checks if entire box is within one sub image
                        print("perfect match")
                        print(end_row, end_col)
                        box = x1-start_col, x2-start_col, y1-start_row, y2-start_row
                        
                        print(box)
                       
                        bb = convert((w,h), box)
                        file.write(str(int(class_id)) + " " + " ".join([str(a) for a in bb]) + '\n')
                        resized_labels.remove(lable)
                        break
                    elif (start_row <= y1 <= end_row and
                          start_row <= y2 <= end_row and
                          start_col <= x1 <= end_col): # box lies between this image and the image to the right
                            box = x1-start_col, end_col-start_col, y1-start_row, y2-start_row
                            bb = convert ((w,h), box)
                            file.write(str(int(class_id)) + " " + " ".join([str(a) for a in bb]) + '\n')

                            print(f"{int(class_id)} {x_center} {y_center} {box_width} {box_height} box: {i}, {k}, but also lies in image to the rigth")   
                    elif (start_row <= y1 <= end_row and
                          start_row <= y2 <= end_row and
                          start_col <= x2 <= end_col): #box lies between this image and the image to the left
                        
                        print(f"{int(class_id)} {x_center} {y_center} {box_width} {box_height} box: {i}, {k}, but also lies in image to the left")   
                    elif (start_col <= x1 <= end_col and
                          start_col <= x2 <= end_col and
                          start_row <= y1 <= end_row):  #box lies between this image and the image on top
                        print(f"{int(class_id)} {x_center} {y_center} {box_width} {box_height} box: {i}, {k}, but also lies in image above")   
                    elif (start_col <= x1 <= end_col and
                          start_col <= x2 <= end_col and
                          start_row <= y2 <= end_row): #box lies between this image and the image below
                        print(f"{int(class_id)} {x_center} {y_center} {box_width} {box_height} box: {i}, {k}, but also lies in image below")   


            file.close()    
            #saving the splitted image
            
            cv2.imwrite(sub_img_path, sub_img)

    if show:
        for i, sub_img in enumerate(sub_images):
            cv2.imshow(f"Sub-Image {i + 1}", cv2.resize(sub_img, (640,520)))
        print("Press 0 to quit")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return sub_images



def split_data(img_path:str, label_path:str, reduce_factor:tuple[int,int] ,output_folder_img: str, output_folder_label:str, show=False):
    sub_imgs = split_img(img_path,label_path, reduce_factor,output_folder_img,outpout_folder_label, show=False)
    
   

def reduce_img(img_path:str,label_path:str, reduce_factor_heigth, output_folder_img:str,output_folder_label:str, show=False):
    image = cv2.imread(img_path)
   
    img_height, img_width, img_channels = image.shape
    reduce_factor_height = 0.4  # Replace with your actual reduce factor
    output_height = int(img_height * reduce_factor_height)
    print(img_height, img_width)
    reduced_img = image[output_height:img_height, 0:img_width, :]
    if show:
        cv2.imshow("Image", cv2.resize(image, (640*2,358*2)))
        cv2.imshow("Image1", cv2.resize(reduced_img, (640*2, 358*2)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    image_filename = os.path.basename(img_path)    
    sub_img_filename = f"{os.path.splitext(image_filename)[0]}.jpg"

    sub_img_path = os.path.join(output_folder_img, sub_img_filename)
    cv2.imwrite(sub_img_path, reduced_img)

    label = open(label_path, "r").read()
    labels = label.split("\n")[:-1]
    
    sub_label_filename = f"{os.path.splitext(image_filename)[0]}.txt"
    sub_label_path = os.path.join(outpout_folder_label, sub_label_filename)
    with open(sub_label_path, 'w') as file:
        for l in labels:
            class_id, x_center, y_center, box_width, box_height = map(float, l.split())
            x_center, y_center, box_width, box_height = (
                        x_center,
                        (y_center - 0.4) / 0.6,
                        box_width,
                        (box_height) / 0.6
                    )
            bb = x_center, y_center, box_width, box_height
            file.write(str(int(class_id)) + " " + " ".join([str(a) for a in bb]) + '\n')
        file.close()




test_path = "train/images/Norway_008145.jpg"
#label_path = "train/labels/Norway_008145.txt"
output_folder_img = "validate/smaller_img/"
outpout_folder_label = "validate/smaller_labels/"

#print(getImagesInDir(dirs[0])[0])
def create_dataset():
    imgs = getImagesInDir('validate')
    for img in imgs:
        basename = os.path.basename(img)
        basename_no_ext = os.path.splitext(basename)[0]
        label_path = f'validate/labels/{basename_no_ext}.txt'
        reduce_img(img, label_path, 0.4, output_folder_img, outpout_folder_label)

create_dataset()