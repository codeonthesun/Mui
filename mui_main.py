import glob
import os
import shutil


class Mui():
    def __init__(self):
        self.files = [f for f in glob.glob('*')]
        self.file_extensions = {os.path.splitext(val)[1] for val in self.files}
        self.path = os.getcwd()
        self.errors = []

    # TODO define error function
        
    def draw_list(self):
        print(f"Files in directory: {self.files}")
        self.user_choice = input(
            'Are you sure you want to organize this directory?[Y/N]: ')

    def draw_confirmation(self):
        while True:
            if self.user_choice.lower().startswith('y'):
                self.create_directory_for_extension()
                print('Success.')
                break
            elif self.user_choice.lower().startswith('n'):
                print('Goodbye.')
                break
            else:
                self.draw_list()

    def create_directory_for_extension(self):
        for self.extension in self.file_extensions:
            self.make_folder()
            self.copy_file()

    def make_folder(self):
        try:
            os.mkdir(self.extension)
        except OSError:
            print(f'Creation of the directory {self.extension} failed')
        else:
            print(f'Successfully created the directory {self.extension}')

    def copy_file(self):
        for file in self.files:
            if self.extension in file:
                try:
                    shutil.move(file, self.extension)
                except shutil.Error as e:
                    print(f'Error: {e}')
                except IOError as e:
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')


if __name__ == '__main__':
    m = Mui()
    m.draw_list()
    m.draw_confirmation()
