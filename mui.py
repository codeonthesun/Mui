import glob
import os
import shutil
import time


class Mui():

    def __init__(self):
        self.path_to_script = (os.path.dirname(os.path.realpath(__file__)))
        self.files = [f for f in glob.glob(self.path_to_script + '/*')]
        self.errors = {}
        self.menu_state = False  # Default menu state for user.

    def record_error(self, msg, source):
        self.errors[msg] = source

    def draw_user_input(self, prompt=None, newline=False, enter_key=False):
        if enter_key:
            self.user_choice = input('(Press [enter] key to proceed.)')
        else:
            self.user_choice = input(prompt + ': ').strip().lower()
        if newline:
            print('\n')
        else:
            pass

    def draw_error(self):
        """
        Output error count if any. Otherwise prompt no errors found.
        """
        if len(self.errors):
            print(f'Error Count: {len(self.errors)}')
            for key, val in self.errors.items():
                print(f'{key} : {val}')
        else:
            print("Wow! No errors, isn't that great?")

    def draw_files_in_dir(self):
        """
        Output all files in current working directory/path to screen.
        """
        print(f'''\n { self.path_to_script } | (Directory Contents):
         ''')
        for file in self.files:
            """
            Formatting to differentiate files from folders.
            """
            if os.path.isfile(file):
                print(f'''  • {file}   ''')  # File
            elif os.path.isdir(file):
                print(f'''  // {file}   ''')  # Folder

    def draw_confirmation(self):
        """
        Continuously prompt response from user. 
        """
        print('_______________________')
        print(' Enter "Menu" for Help ')
        while True:
            self.draw_user_input(
                'Would you like to organize this directory into folders? [Y/N]')
            if self.user_choice.startswith('y'):
                self.draw_user_input(enter_key=True)
                self.create_directory_for_extension()  # Default organization method
                count = len(self.files) - len(self.errors)
                print(
                    f' Success! {count}/{self.files} files moved.')
                self.draw_user_input(enter_key=True)
                break
            elif self.user_choice.startswith('n'):
                print(' Good-bye!')
                quit()
            elif 'menu' in self.user_choice:
                self.menu_state = True
                self.draw_help_menu()
                break
            else:
                print(" Sorry, that's not an appropriate response. Try again.")

    def draw_main_loop(self):
        """
        Initialize main loop combining 'draw_files_in_dir' & 'draw_confirmation'.
        """
        self.draw_files_in_dir()
        self.draw_confirmation()

    def draw_help_menu(self):
        print("""
    (NOTE! Under main directory: "•" = File and "//" = Folder.)
            """)
        print("""Help Menu.
        Here is a list of commands:
        'Close', 'About', 'Options'""")
        while self.menu_state:
            self.draw_user_input('>')
            if 'close' in self.user_choice:  # Reset program loop
                os.system('cls' if os.name == 'nt' else 'clear')  # Return
                self.draw_main_loop()
                break
            elif 'about' in self.user_choice:
                print('''   
        Mui:
    A small tool to aid in file organization, written in Python 3. Default method of organizing is set to consolidate via file extension type. 
    This means for each unique file extension type (e.g. .zip, .txt, .py, ect.) a folder will be created and appropriately matching files moved to said folder.
    Simple, automated, and designed to run flawlessly across platforms. (Python required of course!)
    ''')
                continue
            elif 'options' in self.user_choice:
                pass

    def create_directory_for_extension(self):
        """
        Organize folder contents by file extensions.
        """
        self.file_extensions = {os.path.splitext(ext)[1] for ext in self.files}
        for self.extension in self.file_extensions:
            if not self.extension:  # Prevent creation & copying of folders.
                pass
            else:
                self.path_destination = os.path.join(
                    self.path_to_script, self.extension)  # Define destination for files
                self.make_folder()
                time.sleep(0.5)
                self.copy_file()

    def make_folder(self):
        try:
            os.mkdir(self.path_destination)
        except OSError as e:
            self.record_error(e, self.extension)
            print(f'Creation of the directory: {self.extension} failed. {e}')
        else:
            print(f'Successfully created the directory: {self.extension}')

    def copy_file(self):
        """
        Move all files into matching directories created from 'make_folder'.
        """
        for file in self.files:
            if self.extension in file:
                try:
                    shutil.move(file, self.path_destination)
                except shutil.Error as e:
                    self.record_error(e, file)
                    print(f'Error: {e}')
                except IOError as e:
                    self.record_error(e, file)
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')


if __name__ == '__main__':
    """
    Initialize command-line interface
    """
    m = Mui()
    m.draw_main_loop()
    m.draw_error()
