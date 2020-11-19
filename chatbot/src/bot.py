from telegram.ext import Updater

from chatbot.config import bot_config
from chatbot.handlers import error_callback
from chatbot.handlers.config_handler import config_handler
from chatbot.handlers.question_handler import question_handler
from chatbot.handlers.start_handler import start_handler
from chatbot.jobs.PendingQuestionJob import PendingQuestionJob
from chatbot.log.logger import logger
from howru_models.models import Patient


def main():
    updater = Updater(token=bot_config.TOKEN, use_context=True)

    logger.info("Started HOW-R-U psychologist")

    # Initialize bot
    dispatcher = updater.dispatcher
    handlers = [start_handler, config_handler, question_handler]

    # Add handlers to dispatcher
    for handler in handlers:
        dispatcher.add_handler(handler)

    # Add error callback
    dispatcher.add_error_handler(error_callback)

    # Start bot service
    updater.start_polling()

    # Restore bot jobs
    for patient in Patient.objects.all():
        PendingQuestionJob(context=updater, patient=patient)

    updater.idle()


if __name__ == "__main__":
    main()
