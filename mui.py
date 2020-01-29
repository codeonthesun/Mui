import os
from datetime import date
from glob import glob
from shutil import Error, make_archive, move
from time import sleep


class Mui():

    def __init__(self):
        self.script_path = (os.path.dirname(os.path.realpath(__file__)))
        self.custom_path = [f for f in glob('/*')]
        self.files = [f for f in glob(self.script_path + '/*')]
        self.file_extensions = {os.path.splitext(ext)[1] for ext in self.files}
        self.errors = []
        self.menu_state = False

    def directory_select(self):
        for i, directory in enumerate(self.custom_path):
            print('○', i, directory)
        print('Please select a directory to expand and type "start" to begin')
        self.draw_user_input('>')
        _ = range(0, len(self.custom_path))
        if int(self.user_choice) in _:
            new_path = self.custom_path[int(self.user_choice)]
            print(new_path, 'is selected, ', '\n')
            self.custom_path = [f for f in glob(f'{new_path}/*')]
            for files in self.custom_path:
                print(files)
            if self.user_choice == 'y':
                pass

    def record_error(self, msg):
        """
        Simple error logger, only appends if a valid exception is thrown.
        """
        self.errors.append(msg)

    def draw_user_input(self, prompt=None, enter_key=False):
        """
        User input and prompt.

        enter_key=True, for when we only want shallow input (not to be saved.)
        """

        if enter_key:
            self.user_choice = input('(Press [Enter]-key to proceed.)')
        else:
            self.user_choice = input(prompt + ': ').strip().lower()

    def draw_error(self):
        """
        Display error count if any, otherwise prompt user session was err free.
        """
        if self.errors:
            print(f'Error Count: {len(self.errors)}')
        else:
            print("Wow! No errors, isn't that great?")

    def draw_files_in_dir(self):
        """
        Count files in current directory, starting from 1.

        Displaying whether or not they are file or folder.
        """
        directory = (
            '⌂ Directory Contents:',
            '(NOTE! Under main directory. "•" = File & "○" = Folder.)')
        for dir_count, self.file in enumerate(self.files, start=1):
            if os.path.isfile(self.file):
                print(f'  • {self.file}   ')  # File differentiation
            elif os.path.isdir(self.file):
                print(f'  ○ {self.file}   ')  # Folder differentiation
        print('\n', self.script_path, '\n'.join(directory))
        print('In Directory:', dir_count)

    def main_loop(self):
        self.draw_files_in_dir()
        # Commented out until method is finished.
        #  self.directory_select()
        print('-' * 25, 'Type "Menu" for Help.', sep='\n')
        _ = ('Would you like to sort this directory into sub-folders? [Y/N]')
        while True:
            self.draw_user_input(_)
            if self.user_choice.startswith('y'):
                self.draw_user_input(enter_key=True)
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

    def draw_help_menu(self):
        """
        Static help menu, with commands, about and optional "backup" feature.
        """
        menu = ('Help Menu:', 'List of commands:', '"About", "Backup"')
        about = ('Mui:',
                 'A small tool to aid file organization, written in Python3.',
                 'Default method is set to consolidate via file extension.',
                 'This means for each unique file extension (e.g. .zip, ect.)',
                 'a folder will be made & matching files moved to folder.',
                 'Simple, automated, & built to run across platforms.',
                 '(Python required of course!)')
        print('\n', '\n\t'.join(menu), '\n')
        while self.menu_state:
            print('Type "Close" to return to main.')
            self.draw_user_input('>')
            if 'close' in self.user_choice:
                self.main_loop()
                break
            elif 'about' in self.user_choice:
                print('\n', '\n'.join(about), '\n')
                continue
            elif 'backup' in self.user_choice:
                print('\n', '(WARNING: This could take a long time!)')
                self.draw_user_input(
                    'You MUST type "X" to confirm and hit [Enter]-key')
                if 'x' in self.user_choice:
                    self.backup()
                    continue

    def create_directory_for_extension(self):
        # Initialize count for successful operations.
        self.files_copied, self.folders_created = 0, 0
        # Check each file for extension type.
        for self.extension in self.file_extensions:
            # Verify source is file
            if self.extension:
                self.path_destination = os.path.join(
                    self.script_path, self.extension)  # Initialize path dest.
                self.make_folder()
                sleep(0.5)
                self.copy_file()

    def make_folder(self):
        """
        Make a new directory (folder) for each unique file-extension type.

        Uses self.path_destination set from create_directory_for_extension.
        """
        # Make sure folder does not already exist before creating
        if not os.path.exists(self.path_destination):
            try:
                os.mkdir(self.path_destination)
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
        """
        Move all files into corresponding extension-type folder.
        """
        for self.file in self.files:
            # Check files for matching extension type
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

    def backup(self):
        """
        Optional backup, makes a zip backup up entire directory.

        Use with caution, depending on amount of content in directory and
        file sizes, the procedure could take a long time.
        """
        backup_path, timestamp = os.path.join(
            self.script_path, 'backup'), str(date.today())
        # Initialize backup folder name with  current timestamp.
        archive = f'{backup_path}_{timestamp}'
        print('Working.')
        sleep(0.5)
        if not os.path.exists(backup_path):
            try:
                os.mkdir(backup_path)
            except OSError as e:
                print(f'Creation of the directory: backup failed. {e}')
            else:
                print('Successfully created the directory: backup.')
                sleep(0.5)
        else:
            print('Directory already exists.')
        try:
            make_archive(
                base_name=archive, format='zip', root_dir=self.script_path)
        except Exception as e:
            print(f'Error: {e}')
        else:
            print('Archive created.')
            sleep(0.5)

        try:
            move(archive + '.zip', backup_path + '/')
        except Exception as e:
            print(f'Error: {e}')
        else:
            print('Done.')

    def post_prompt(self):
        """
        Message to be displayed after operations.

        Includes successful file transfer count and error count if valid.
        """
        _ = ('Task Complete:', 'directories created and', 'files moved.')
        print(
            f'{_[0]} {self.folders_created} {_[1]} {self.files_copied} {_[2]}')
        self.draw_error()
        print('- Feel free to close this window.')


if __name__ == '__main__':
    m = Mui()
    # m.main_loop()
