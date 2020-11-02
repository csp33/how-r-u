from datetime import datetime

import pytz
from telegram import ParseMode
from telegram.ext import ConversationHandler, CallbackQueryHandler

from chatbot.config.messages import messages
from chatbot.handlers import send_typing_action
from chatbot.log.logger import logger
from howru_models.models import AnsweredQuestion, PendingQuestion, Response, Patient


@send_typing_action
def answer_question(update, context):
    """
    Prompts user's question by querying PendingQuestion DB.
    Creates an AsweredQuestion object.
    """
    # Answer query
    update.callback_query.answer()

    # Get patient and response
    patient = Patient.objects.get(identifier=update.callback_query.from_user.id)
    response_id = update.callback_query.data.split('response-')[1]
    response = Response.objects.get(id=response_id)

    # Get question that is being answered from DB:
    try:
        question_task = _get_pending_question_task(str(patient.identifier))
    except PendingQuestion.DoesNotExist:
        logger.info(
            f'User {patient.username} id {patient.identifier} wrote {response} while there was no question to answer')
        return ConversationHandler.END

    question = question_task.question

    # Log response
    logger.info(f'User {patient.username} answered "{response}" to question "{question_task.question}"')

    # Create answered question entry
    answered_question = AnsweredQuestion(patient_id=patient.identifier, doctor=question_task.doctor,
                                         answer_date=datetime.now(pytz.timezone('Europe/Madrid')),
                                         response=response,
                                         question=question)
    answered_question.save()

    # Set answering to false
    question_task.answering = False
    question_task.save()

    # Edit message
    update.callback_query.edit_message_text(messages[patient.language]['answered_question'].format(question, response),
                                            parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def _get_pending_question_task(user_id):
    """
    Obtains the question that the user is answering
    """
    return PendingQuestion.objects.get(patient_id=user_id, answering=True)


question_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(answer_question, pattern="^response-[a-zA-Z1-9]*$")],
    states={},
    fallbacks=[],
    name="questions_handler"
)
