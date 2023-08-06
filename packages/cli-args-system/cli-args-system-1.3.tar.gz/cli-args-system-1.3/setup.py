from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  name = 'cli-args-system',        
  description = 'A Cli flags libary  to control argv flags and content',   
  long_description = long_description,
  long_description_content_type='text/markdown',
  packages = ['cli_args_system'],
  version = '1.03',    
  license='MIT',     


  author = 'Mateus Moutinho Queiroz',               
  author_email = 'mateusmoutinho01@gmail.com',      
  url = 'https://github.com/mateusmoutinho/python-cli-args.git',  
  download_url = 'https://github.com/mateusmoutinho/python-cli-args/archive/refs/heads/main.zip',    # I explain this later on
  keywords = ['ARGV', 'ClI ARGUMENTS'], 

  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)