import logging

from scrim_bot.scrim_bot import ScrimBot

if __name__ == '__main__':
    logger = logging
    logger.basicConfig(format='%(asctime)s - %(name)s -  %(levelname)s - %(message)s', level=logging.INFO,
                       datefmt='%d-%b-%y %H:%M:%S')

    bot = ScrimBot()
    bot.run()
