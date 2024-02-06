import os
import json
from xml.etree import ElementTree as ET


def pascal_voc_to_coco(input_folder, output_file):
    coco_data = {
            "info": {},
            "licenses": [],
            "categories": [],
            "images": [],
            "annotations": []
        }
    category_mapping = {
            'D00': 1,
            'D10': 2,
            'D20': 3,
            'D40': 4,
        }
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_path = os.path.join(input_folder, filename)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            image_info = {
                "id": len(coco_data["images"]) + 1,
                "width": int(root.find('size/width').text),
                "height": int(root.find('size/height').text),
                "file_name": root.find('filename').text,
                "license": 0,
                "flickr_url": "",
                "coco_url": "",
                "date_captured": ""
            }

            coco_data["images"].append(image_info)
            for obj in root.findall('object'):
                    category_name = obj.find('name').text
                    category_id = category_mapping.get(category_name, -1)

                    if category_id == -1:
                        continue

                    bbox = obj.find('bndbox')
                    x_min = int(round(float(bbox.find('xmin').text)))
                    y_min = int(round(float(bbox.find('ymin').text)))
                    x_max = int(round(float(bbox.find('xmax').text)))
                    y_max = int(round(float(bbox.find('ymax').text)))

                    annotation = {
                        "id": len(coco_data["annotations"]) + 1,
                        "image_id": image_info["id"],
                        "category_id": category_id,
                        "segmentation": [],
                        "area": (x_max - x_min) * (y_max - y_min),
                        "bbox": [x_min, y_min-0.4*int(image_info["height"]), x_max - x_min, y_max - y_min],
                        "iscrowd": 0,
                    }

                    coco_data["annotations"].append(annotation)
    for category_name, category_id in category_mapping.items():
        coco_data["categories"].append({
            "id": category_id,
            "name": category_name,
            "supercategory": ""
            })

        # Save COCO format to a JSON file
        with open(output_file, 'w') as json_file:
            json.dump(coco_data, json_file, indent=4)

input_folder = 'dataset/validate/annotations'
output_file = 'coco_annotations_validation.json'
pascal_voc_to_coco(input_folder, output_file)