

from bot import bot_processing

import logging

console = logging.StreamHandler()
console.setLevel(logging.INFO)

log_file = logging.FileHandler(filename='error.log', mode='a')
log_file.setLevel(logging.ERROR)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, handlers=[log_file, console])

if __name__ == '__main__':
    bot_processing()
