import os
import base64
from test_data import *
import time
import random

import subprocess
from docx import Document

TEMP_FOLDER = temp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

def convert_to_pdf_service(data):
    input_file_fullname = data['filename'] if 'filename' in data else None
    input_file_data = data['data'] if 'data' in data else None
    if (input_file_fullname and input_file_data):
        filename, output_base64 = _convert_to_pdf(input_file_fullname, INPUT_DOCX_FILE)
        return filename,output_base64
    else:
        raise Exception('Неверные данные')

def _get_name_and_extension(input_file_name: str) -> {str, str}:
    input_file_name, input_file_extension = input_file_name.rsplit('.', 1)
    return input_file_name, input_file_extension

def _generate_temp_file_name() -> str:
    timestamp = int(time.time())
    random_number = random.randint(1, 1000)
    file_name = f"{timestamp}_{random_number}"
    return file_name

def _save_temp_input_docx_file(temp_file_name: str, input_file_extension: str, input_file_data: str) -> str:
    try:
        temp_file_path = f'{TEMP_FOLDER}/{temp_file_name}.{input_file_extension}'
        binary_data = base64.b64decode(input_file_data)
        with open(temp_file_path, 'wb') as file:
            file.write(binary_data)
        print(f"Файл успешно сохранен по пути: {temp_file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
    return temp_file_path

def _convert_to_pdf(input_file_fullname: str, input_file_data: str) -> {str, str}:
    input_file_name, input_file_extension = _get_name_and_extension(input_file_fullname)
    output_filename = f'{input_file_name}.pdf'
    output_file_path = f'{TEMP_FOLDER}/{output_filename}'
    if input_file_extension in ['doc', 'docx']:
        temp_file_name = _generate_temp_file_name()
        temp_docx_filepath = _save_temp_input_docx_file(temp_file_name, input_file_extension, input_file_data)
        print('DOCX', temp_docx_filepath)
        temp_pdf_filepath = f'{TEMP_FOLDER}/{temp_file_name}.pdf'
        print('PDF', output_file_path)
        print('Конвертирую...')
        
        subprocess.run(["unoconv", "-f", "pdf", "-o", output_file_path, temp_docx_filepath], check=True)
        print(f"Conversion successful. PDF saved to: {output_file_path}")

        print('Конвертация закончена...')
        output_file_base64 = base64.b64encode(open(output_file_path, 'rb').read()).decode('utf-8')
        os.remove(temp_docx_filepath)
        #os.remove(output_file_path)
        return output_filename, output_file_base64
    return 'sdf'

if __name__ == "__main__":
    _convert_to_pdf('mytestfile.docx', INPUT_DOCX_FILE)
    # save_temp_input_file('mytestfile.docx', INPUT_DOCX_FILE)
    # output_base64 = convert_to_pdf('mytestfile.docx', INPUT_DOCX_FILE)
    # print(output_base64)