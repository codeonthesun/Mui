import glob
import os
import shutil
import time


class Mui():
    def __init__(self):
        self.files = [f for f in glob.glob('*')]
        self.file_extensions = {os.path.splitext(val)[1] for val in self.files}
        self.path = os.getcwd()
        self.errors = []

    def record_error(self, msg):
        self.errors.push(msg)

    def draw_errors(self):
        print(f'Error Count: {len(self.errors)}')

    def draw_files_in_dir(self):
        print('''Files in Directory:
        ''')
        for file in self.files:
            print(f'''   {file}   ''')

    def draw_confirmation(self):
        while True:
            self.user_choice = input(
                'Are you sure you want to organize this directory? [Y/N]: '
            ).strip().lower()

            if self.user_choice.startswith('y'):
                self.create_directory_for_extension()
                print('Success.')
                break
            elif self.user_choice.startswith('n'):
                print('Goodbye.')
                break
            else:
                print("[ Sorry, that's not an appropriate answer. Try again ]")

    def create_directory_for_extension(self):
        for self.extension in self.file_extensions:
            self.make_folder()
            time.sleep(0.5)
            self.copy_file()

    def make_folder(self):
        try:
            os.mkdir(self.extension)
        except OSError as err:
            self.record_error(err)
            print(
                f'Creation of the directory {self.extension} failed. {err}')
        else:
            print(f'Successfully created the directory {self.extension}')

    def copy_file(self):
        for file in self.files:
            if self.extension in file:
                try:
                    shutil.move(file, self.extension)
                except shutil.Error as e:
                    self.record_error(e)
                    print(f'Error: {e}')
                except IOError as e:
                    self.record_error(e)
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')


if __name__ == '__main__':
    m = Mui()
    m.draw_files_in_dir()
    m.draw_confirmation()
    m.draw_errors()
