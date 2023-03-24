import os
import PySimpleGUI as sg

def remove_text(input_path):
    with open(input_path, 'rb') as input_file:
        content = input_file.read().decode('utf-8', 'ignore')
        start_index = content.find('<?xml version="1.0" encoding="utf-8"?>')
        if start_index == -1:
            return None
        output_content = content[start_index:]
    return output_content.encode('utf-8')

def convert_files(input_path, output_folder):
    if os.path.isfile(input_path):
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(input_path))[0] + '.svg')
        output_content = remove_text(input_path)
        with open(output_path, 'wb') as output_file:
            output_file.write(output_content)
    elif os.path.isdir(input_path):
        for dirpath, dirnames, filenames in os.walk(input_path):
            for filename in filenames:
                if filename.lower().endswith('.vsvg_c'):
                    input_file_path = os.path.join(dirpath, filename)
                    output_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.svg')
                    output_content = remove_text(input_file_path)
                    with open(output_file_path, 'wb') as output_file:
                        output_file.write(output_content)

sg.theme('Dark Blue 3')

layout = [[sg.Text('Select a folder or a file')],
          [sg.Input(key='-PATH-'), sg.FileBrowse('Browse File'), sg.Button('Browse Folder')],
          [sg.Text('Select output folder')],
          [sg.Input(key='-OUTPUT_PATH-'), sg.FolderBrowse('Browse Output Folder')],
          [sg.Button('Convert'), sg.Button('Exit')]]

window = sg.Window('vsvg_c to svg Converter', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Convert':
        input_path = values['-PATH-']
        output_folder = values['-OUTPUT_PATH-']
        if not input_path or not output_folder:
            sg.popup_error('Please select a valid input file/folder and output folder.')
        else:
            convert_files(input_path, output_folder)
            sg.popup('Conversion completed successfully!')
    elif event == 'Browse Folder':
        folder_path = sg.popup_get_folder('Select a folder')
        if folder_path:
            window['-PATH-'].update(folder_path)

window.close()
