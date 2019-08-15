

from bot import bot_processing
from app import run_app

import logging
import multiprocessing

console = logging.StreamHandler()
console.setLevel(logging.INFO)

log_file = logging.FileHandler(filename='error.log', mode='a')
log_file.setLevel(logging.ERROR)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, handlers=[log_file, console])

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    app_process = multiprocessing.Process(target=run_app)
    app_process.start()
    bot_processing()
    app_process.join()
