import os

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import chatbot.keyboards as keyboards
from chatbot.config.messages import messages
from chatbot.handlers import send_typing_action
from chatbot.jobs.PendingQuestionJob import PendingQuestionJob
from chatbot.log.logger import logger
from howru_models.models import Patient, PendingQuestion, Doctor

GENDER, PICTURE, LANGUAGE, SCHEDULE, TIMEZONE = range(5)


# noinspection PyProtectedMember
@send_typing_action
def start(update, context):
    """
    Shows welcome message and asks for language
    """
    try:
        # Try to answer query if the user is registering again
        update.callback_query.answer()
    except Exception:
        pass

    patient_id = update._effective_user.id
    # Check that user is not registered
    try:
        patient = Patient.objects.get(identifier=patient_id)
        logger.info(
            f'User {patient.username} tried to register again.')
        context.bot.send_message(chat_id=patient_id, text=messages[patient.language]['already_exists'])
        return ConversationHandler.END
    except Patient.DoesNotExist:
        # The user should not exist in DB
        context.user_data['patient'] = Patient(name=update._effective_user.first_name,
                                               identifier=str(patient_id),
                                               username=update._effective_user.username)

    logger.info(f'User {update._effective_user.username} started a new conversation')
    context.bot.send_message(chat_id=patient_id,
                             text=f'Hi {update._effective_user.first_name}. Welcome to HOW-R-U psychologist bot.\n'
                                  f'Hola {update._effective_user.first_name}. Bienvenido al bot psicólogo HOW-R-U')
    context.bot.send_message(chat_id=patient_id, text=f'Please select a language:\nElija un idioma por favor:',
                             reply_markup=keyboards.language_keyboard)

    return LANGUAGE


@send_typing_action
def language(update, context):
    """
    Processes language and asks for gender
    """
    update.callback_query.answer()

    patient_language = update.callback_query.data
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} chose language {patient_language}')

    context.user_data['patient'].language = patient_language
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['choose_gender'],
                             reply_markup=keyboards.gender_keyboard[patient.language])
    return GENDER


@send_typing_action
def gender(update, context):
    """
    Processes gender and asks for picture
    """
    update.callback_query.answer()

    patient = context.user_data['patient']
    patient_gender = update.callback_query.data
    logger.info(
        f'User {patient.username} chose gender {patient_gender}')
    patient.gender = patient_gender
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['choose_pic'],
                             reply_markup=keyboards.skip_keyboard[patient.language])
    return PICTURE


@send_typing_action
def picture(update, context):
    """
    Processes picture and asks for schedule
    """
    patient = context.user_data['patient']
    photo_file = update.message.photo[-1].get_file()
    pic_name = f'/opt/chatbot/chatbot/pics/{update.message.from_user.id}.jpg'
    photo_file.download(pic_name)
    patient.picture = pic_name
    os.remove(pic_name)
    logger.info(f'User {update.message.from_user.username} sent picture {pic_name}')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['choose_timezone'],
                             reply_markup=keyboards.send_location_keyboard[patient.language])
    return TIMEZONE


@send_typing_action
def skip_picture(update, context):
    """
    Sets default picture and asks for schedule
    """
    update.callback_query.answer()

    patient = context.user_data['patient']
    logger.info(f'User {patient.username} did not send a picture, using default')
    patient.picture = '/opt/chatbot/chatbot/pics/default_profile_picture.png'
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['choose_timezone'],
                             reply_markup=keyboards.send_location_keyboard[patient.language])
    return TIMEZONE


@send_typing_action
def timezone(update, context):
    """
    Gets the patient's timezone by analyzing the sent location
    """
    patient = context.user_data['patient']
    patient_timezone = Patient.get_timezone_from_location(update.message.location)
    logger.info(f'User {patient.username} choose timezone {patient_timezone}')
    patient.timezone = patient_timezone
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['choose_schedule'],
                             reply_markup=ReplyKeyboardRemove())
    return SCHEDULE

@send_typing_action
def default_timezone(update, context):
    """
    Sets default timezone to a patient (Europe/Madrid)
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'Set default timezone (Europe/Madrid) for user {patient.username}')
    patient.timezone = "Europe/Madrid"
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['choose_schedule'],
                             reply_markup=ReplyKeyboardRemove())
    return SCHEDULE


@send_typing_action
def schedule(update, context):
    """
    Processes schedule and calls finish() method
    """
    patient_schedule = update.message.text
    patient = context.user_data['patient']
    logger.info(f'User {update.message.from_user.username} chose schedule {patient_schedule}')
    patient.schedule = patient_schedule
    return finish(update, context)


@send_typing_action
def finish(update, context):
    """
    Saves patient in DB, assigns him/her to data_analyst, creates PendingQuestion entries for assigned_to_all questions
    and finally creates the user's PendingQuestionJob
    """
    patient = context.user_data['patient']
    patient.save()
    # Add patient to data analysts and assigned_to_all questions
    try:
        data_analysts = Doctor.objects.filter(is_analyst=True)
        for doctor in data_analysts:
            patient.assigned_doctors.add(doctor)
            patient.save()
            assigned_to_all = doctor.assigned_questions.filter(assigned_to_all=True)
            for question in assigned_to_all:
                pending_question = PendingQuestion(doctor=doctor,
                                                   question=question,
                                                   patient=patient,
                                                   answering=False)
                pending_question.save()
        logger.info("Patient %s assigned to data_analysts", patient.username)
    except Exception:
        logger.exception("Exception while adding patient %s to data_analysts.", patient.username)
    update.message.reply_text(messages[patient.language]['registration_ok'])
    logger.info(f'Creating pending_questions job for user {update.message.from_user.username}')
    PendingQuestionJob(context, patient)
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CallbackQueryHandler(start, pattern="^start$")
    ],
    states={
        LANGUAGE: [
            CallbackQueryHandler(language, pattern='^(ES|GB)$')
        ],
        GENDER: [
            CallbackQueryHandler(gender, pattern="^(Male|Female|Other)$")
        ],
        PICTURE: [
            MessageHandler(Filters.photo, picture), CallbackQueryHandler(skip_picture, pattern="^skip$")
        ],
        TIMEZONE: [
            MessageHandler(Filters.location, timezone),
            CallbackQueryHandler(default_timezone, pattern="^default-timezone$")
        ],
        SCHEDULE: [
            MessageHandler(Filters.regex('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'), schedule)
        ]
    },
    fallbacks=[],
    name="starter"
)
