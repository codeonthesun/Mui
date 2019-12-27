import glob
import os
import shutil


class Mui():
    def __init__(self):
        self.files = [f for f in glob.glob('*')]
        self.file_extensions = [os.path.splitext(val)[1] for val in self.files]
        self.path = os.getcwd()
        self.errors = 0

    def draw_list(self):
        print(f"Files in directory: {self.files}")
        self.user_choice = input(
            'Are you sure you want to organize this directory?[Y/N]: ')
        self.temp = self.user_choice.lower()

    def draw_confirmation(self):
        while 'y' or 'n' not in self.temp:
            if 'y' in self.temp:
                self.create_directory_for_extension()
                print('Success')
                break
            elif 'n' in self.temp:
                print('Goodbye.')
                break
            else:
                self.draw_list()

    def create_directory_for_extension(self):
        for self.extension in self.file_extensions:
            self.dir_name = self.extension
            self.make_folder(self.dir_name)
            self.copy_file()

    def make_folder(self, dir_name):
        try:
            os.mkdir(dir_name)
        except OSError:
            print(f'Creation of the directory {dir_name} failed')
            self.errors += 1
        else:
            print(f'Successfully created the directory {self.path}')

    def copy_file(self):
        for file in self.files:
            fname = file
            if self.dir_name in fname:
                try:
                    shutil.move(f'{fname}', f'{self.dir_name} //')
                except shutil.Error as e:
                    print(f'Error: {e}')
                except IOError as e:
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')

    def draw_errors(self):
        if self.errors > 0:
            print(self.errors)


m = Mui()
m.draw_list()
m.draw_confirmation()
