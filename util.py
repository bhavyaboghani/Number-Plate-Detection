import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_num', 'car_id', 'car_bbox',
                                                'number_plate_bbox', 'number_plate_bbox_score', 'numberplate_number',
                                                'numberplate_number_score'))

        for frame_num in results.keys():
            for car_id in results[frame_num].keys():
                print(results[frame_num][car_id])
                if 'car' in results[frame_num][car_id].keys() and \
                   'number_plate' in results[frame_num][car_id].keys() and \
                   'text' in results[frame_num][car_id]['number_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_num,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_num][car_id]['car']['bbox'][0],
                                                                results[frame_num][car_id]['car']['bbox'][1],
                                                                results[frame_num][car_id]['car']['bbox'][2],
                                                                results[frame_num][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_num][car_id]['number_plate']['bbox'][0],
                                                                results[frame_num][car_id]['number_plate']['bbox'][1],
                                                                results[frame_num][car_id]['number_plate']['bbox'][2],
                                                                results[frame_num][car_id]['number_plate']['bbox'][3]),
                                                            results[frame_num][car_id]['number_plate']['bbox_score'],
                                                            results[frame_num][car_id]['number_plate']['text'],
                                                            results[frame_num][car_id]['number_plate']['text_score'])
                            )
        f.close()


def number_plate_complies_format(text):
    """
    Check if the license plate text complies with the Indian format: AA NN AA NNNN
    """
    if len(text) != 10:
        return False

    def is_letter(ch):
        return ch in string.ascii_uppercase or ch in dict_int_to_char

    def is_digit(ch):
        return ch in string.digits or ch in dict_char_to_int

    return (
        is_letter(text[0]) and is_letter(text[1]) and         # AA
        is_digit(text[2]) and is_digit(text[3]) and           # NN
        is_letter(text[4]) and is_letter(text[5]) and         # AA
        is_digit(text[6]) and is_digit(text[7]) and           # NNNN
        is_digit(text[8]) and is_digit(text[9])
    )



def format_number_plate(text):
    """
    Format the license plate by correcting character/number mismatches
    according to AA NN AA NNNN format.
    """
    formatted = ''
    mapping = {
        0: dict_int_to_char, 1: dict_int_to_char,     # letters
        2: dict_char_to_int, 3: dict_char_to_int,     # digits
        4: dict_int_to_char, 5: dict_int_to_char,     # letters
        6: dict_char_to_int, 7: dict_char_to_int,     # digits
        8: dict_char_to_int, 9: dict_char_to_int
    }

    for i in range(10):
        char = text[i]
        if i in mapping and char in mapping[i]:
            formatted += mapping[i][char]
        else:
            formatted += char

    return formatted



def read_number_plate(number_plate_crop):
    detections = reader.readtext(number_plate_crop)

    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '').replace('\n', '')
        print("OCR detected:", text, "with score:", score)

        if number_plate_complies_format(text):
            formatted = format_number_plate(text)
            print("Formatted:", formatted)
            return formatted, score

    print("No valid plate found in this crop.")
    return 0, 0



def get_car(number_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        number_plate (tuple): Tuple containing the coordinates of the license plate (x1, y1, x2, y2, score, class_id).
        vehicle_track_ids (list): List of vehicle track IDs and their corresponding coordinates.

    Returns:
        tuple: Tuple containing the vehicle coordinates (x1, y1, x2, y2) and ID.
    """
    x1, y1, x2, y2, score, class_id = number_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1
