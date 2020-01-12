from datetime import date
from glob import glob
from os import mkdir, name, system
from os.path import dirname, exists, isdir, isfile, join, realpath, splitext
from shutil import Error, make_archive, move
from time import sleep


class Mui():

    def __init__(self):
        self.script_path = (dirname(realpath(__file__)))
        self.files = [f for f in glob(self.script_path + '/*')]
        self.errors = []
        self.menu_state = False  # Default menu state for user.

    def record_error(self, msg):
        self.errors.append(msg)

    @property
    def error_count(self):
        return len(self.errors)

    def draw_user_input(self, prompt=None, enter_key=False):
        if enter_key:
            self.user_choice = input('(Press [Enter]-key to proceed.)')
        else:
            self.user_choice = input(prompt + ': ').strip().lower()

    def draw_error(self):
        if self.errors:
            print(f'Error Count: {self.error_count}')
        else:
            print("Wow! No errors, isn't that great?")

    def draw_files_in_dir(self):
        _ = ('⌂ Directory Contents:',
             '(NOTE! Under main directory: "•" = File and "○" = Folder.)')
        print('\n', self.script_path, '\n'.join(_), '\n')
        for self.file in self.files:
            if isfile(self.file):
                print(f'  • {self.file}   ')  # File
            elif isdir(self.file):
                print(f'  ○ {self.file}   ')  # Folder

    def draw_confirmation(self):
        print('_______________________', 'Type "Menu" for Help.', sep='\n')
        _ = ('Would you like to sort this directory into sub-folders? [Y/N]')
        while True:
            self.draw_user_input(_)
            if self.user_choice.startswith('y'):
                self.create_directory_for_extension()
                self.post_prompt()
                break
            elif self.user_choice.startswith('n'):
                print('Good-bye!')
                quit()
            elif 'menu' in self.user_choice:
                self.menu_state = True
                self.draw_help_menu()
                break
            else:
                print('Sorry, not an appropriate response. Try again.')

    def draw_main_loop(self):
        self.draw_files_in_dir()
        self.draw_confirmation()

    def draw_help_menu(self):
        _men = ('Help Menu:', 'List of commands:', '"About", "Backup"')
        _abt = ('Mui:',
                'A small tool to aid file organization, written in Python3.',
                'Default method is set to consolidate via file extension.',
                'This means for each unique file extension (e.g. .zip, ect.)',
                'a folder will be made & matching files moved to said folder.',
                'Simple, automated, & built to run across platforms.',
                '(Python required of course!)')
        print('\n', '\n\t'.join(_men), '\n')
        while self.menu_state:
            print('Type "Close" to return to main.')
            self.draw_user_input('>')
            if 'close' in self.user_choice:
                system('cls' if name == 'nt' else 'clear')
                self.draw_main_loop()
                break
            elif 'about' in self.user_choice:
                print('\n', '\n'.join(_abt), '\n')
                continue
            elif 'backup' in self.user_choice:
                print('\n', '(WARNING: This could take a long time!)')
                self.draw_user_input(
                    'Confirm with "X" or leave empty and hit [Enter]-key')
                if 'x' in self.user_choice:
                    self.optional_backup()
                    continue

    def optional_backup(self):
        _backup_path, _timestamp = join(
            self.script_path, 'backup'), str(date.today())
        archive = f'{_backup_path}_{_timestamp}'
        print('Working.')
        sleep(0.5)
        if not exists(_backup_path):
            try:
                mkdir(_backup_path)
            except OSError as e:
                print(f'Creation of the directory: backup failed. {e}.')
            else:
                print('Successfully created the directory: backup.')
                sleep(0.5)
        else:
            print('Directory already exists.')
        try:
            make_archive(base_name=archive, format='zip',
                         root_dir=self.script_path)
        except Exception as e:
            print(f'Error: {e}')
        else:
            print('Archive created.')
            sleep(0.5)
        try:
            move(archive + '.zip', _backup_path + '/')
        except Exception as e:
            print(f'Error: {e}')
        else:
            print('Done.')

    def create_directory_for_extension(self):
        self.folders_created, self.files_copied = 0, 0
        self.file_extensions = {splitext(ext)[1] for ext in self.files}
        for self.extension in self.file_extensions:
            if self.extension:
                self.path_destination = join(self.script_path, self.extension)
                self.make_folder()
                sleep(0.5)
                self.copy_file()

    def make_folder(self):
        if not exists(self.path_destination):
            try:
                mkdir(self.path_destination)
            except OSError as e:
                self.record_error(e)
                print(
                    f'Creation of the directory: {self.extension} failed. {e}')
            else:
                print(f'Successfully created the directory: {self.extension}.')
                self.folders_created += 1
        else:
            print('Directory already exists.')

    def copy_file(self):
        for self.file in self.files:
            if self.extension in self.file:
                try:
                    move(self.file, self.path_destination)
                except Error as e:
                    self.record_error(e)
                    print(f'Error: {e}')
                except IOError as e:
                    self.record_error(e)
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')
                    self.files_copied += 1

    def post_prompt(self):
        _ = ('Task Complete:', 'directories created and', 'files moved.')
        print(
            f'{_[0]} {self.folders_created} {_[1]} {self.files_copied} {_[2]}')
        self.draw_error()
        self.draw_user_input(enter_key=True)


if __name__ == '__main__':
    m = Mui()
    m.draw_main_loop()
