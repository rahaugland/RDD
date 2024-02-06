import json
import cv2

path_img = "train/images/Norway_000545.jpg"
labels_path = "train/labels/Norway_000545.txt"
unformatted_path = "../dataset/train/images/Norway_007360.jpg"
unformatted_path_label = "../dataset/train/labels/Norway_007360.txt"
image_id= 6860

def draw_coc_data(path_img, labels_path, img_id):
        image = cv2.imread(path_img)
        h, w,_ = image.shape
        print(h)
        
        filtered_annotations = []
        with open(labels_path, 'r') as file: 
                annotations = json.load(file)['annotations']
                filtered_annotations = [annotation for annotation in annotations if annotation['image_id'] == img_id]
        print(len(filtered_annotations))
        for annotation in filtered_annotations:
                x, y, width, height = annotation['bbox']
                x, y, width, height = int(x), int(y), int(width), int(height)
                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.imshow("Image",  cv2.resize(image, (2040,1040)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def draw_yolo_data(path_img, labels_path):
        image = cv2.imread(path_img)
        img_height, img_width, _  = image.shape
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        label = open(labels_path, "r").read()
        label = label.split("\n")[:-1]
        print(label)

        for l in label:
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
                print(img_height, img_width)
                print(f'{x1},{x2},{y1},{y2}, {box_height}, {box_width}')

                # Draw the rectangle on the image
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Image with Bounding Boxes", cv2.resize(image, (2040,1040)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

draw_yolo_data(path_img, labels_path)
