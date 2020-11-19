import base64
import os

from telegram import ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, run_async, CallbackQueryHandler

import chatbot.keyboards as keyboards
# noinspection PyUnresolvedReferences
import manage
from chatbot.config.messages import messages
from chatbot.filters.IsAnsweringFilter import is_answering_filter
from chatbot.handlers import send_typing_action, send_upload_photo_action
from chatbot.jobs.PendingQuestionJob import PendingQuestionJob
from chatbot.log.logger import logger
from howru_models.models import Patient

PROCESS_PROFILE_PIC, PROCESS_NAME, PROCESS_GENDER, CHOOSING, PROCESS_LANGUAGE, PROCESS_DELETE_USER, PROCESS_SCHEDULE, \
PROCESS_TIMEZONE = range(8)


# noinspection PyUnusedLocal
@send_typing_action
def config_menu(update, context):
    """
    Shows config menu as a keyboard
    """
    patient = context.user_data['patient']

    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['select_config'],
                             reply_markup=keyboards.config_keyboard[patient.language])

    return CHOOSING


@send_typing_action
def config(update, context):
    """
    Starts the configurator and checks whether the user is registered or not.
    """
    logger.info(f'User {update.message.from_user.username} started the configurator')
    try:
        context.user_data['patient'] = Patient.objects.get(identifier=update.message.from_user.id)
    except Patient.DoesNotExist:
        logger.info(
            f'User {update.message.from_user.username} tried to start the configurator but was not registered')
        update.message.reply_text('You must register first by clicking /start\n'
                                  'Debes registrarte primero pulsando /start.',
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    return config_menu(update, context)


@send_upload_photo_action
def ask_profile_pic(update, context):
    """
    Sends old profile picture to the user and asks the new one.
    """
    # Answer callback query
    update.callback_query.answer()
    # Get patient instance
    patient = context.user_data['patient']

    # Send current picture
    with open('current_pic.png', 'wb') as output:
        output.write(base64.b64decode(patient.picture))
    context.bot.send_photo(chat_id=patient.identifier, photo=open('current_pic.png', 'rb'),
                           caption=messages[patient.language]['current_picture'])
    os.remove('current_pic.png')

    # Ask for new picture
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['change_picture'],
                             reply_markup=keyboards.back_keyboard[patient.language])
    return PROCESS_PROFILE_PIC


@send_typing_action
def process_profile_pic(update, context):
    """
    Saves the new profile picture
    """
    patient = context.user_data['patient']
    photo_file = update.message.photo[-1].get_file()
    pic_name = f'/opt/chatbot/chatbot/pics/{patient.identifier}.jpg'
    photo_file.download(pic_name)
    patient.picture = pic_name
    patient.save()
    logger.info(f'User {patient.username} changed profile picture')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['picture_updated'],
                             reply_markup=ReplyKeyboardRemove())
    return config_menu(update, context)


@send_typing_action
def ask_change_name(update, context):
    """
    Sends old name to the user and asks for the new one
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} asked to change name')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['current_name'] + patient.name)
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['change_name'],
                             reply_markup=keyboards.back_keyboard[patient.language])
    return PROCESS_NAME


@send_typing_action
def process_name(update, context):
    """
    Saves the new name
    """
    patient = context.user_data['patient']
    old_name = patient.name
    name = update.message.text
    patient.name = name
    patient.save(update_fields=['name'])
    logger.info(f'User {patient.name} old name {old_name} changed name to {name}')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['name_updated'])
    return config_menu(update, context)


@send_typing_action
def ask_change_gender(update, context):
    """
    Sends old gender to the user and asks for the new one
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} asked to change gender')
    context.bot.send_message(chat_id=patient.identifier,
                             text=messages[patient.language]['current_gender'] + patient.gender)
    # TODO gender keyboard inline
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['change_gender'],
                             reply_markup=keyboards.gender_keyboard[patient.language])
    return PROCESS_GENDER


@send_typing_action
def process_gender(update, context):
    """
    Saves the new gender
    """
    # Answer query
    update.callback_query.answer()

    # Get patient and gender from query
    patient = context.user_data['patient']
    gender = update.callback_query.data

    # Change gender in patient object
    patient.gender = gender
    patient.save(update_fields=['_gender'])

    logger.info(f'User {patient.username} changed gender to {gender}')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['gender_updated'])
    return config_menu(update, context)


@send_typing_action
def ask_change_language(update, context):
    """
    Sends old language to the user and asks for the new one
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} asked to change language')
    context.bot.send_message(chat_id=patient.identifier,
                             text=messages[patient.language]['current_language'] + patient.get_language_display())
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['change_language'],
                             reply_markup=keyboards.language_keyboard)
    return PROCESS_LANGUAGE


@send_typing_action
def process_language(update, context):
    """
    Saves the new language
    """
    update.callback_query.answer()

    patient = context.user_data['patient']
    patient.language = update.callback_query.data
    patient.save(update_fields=['language'])
    logger.info(f'User {patient.username} changed language to {patient.language}')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['language_updated'])
    return config_menu(update, context)


@send_typing_action
def view_profile(update, context):
    """
    Sends profile information to the user
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    message = messages[patient.language]['show_profile'].format(patient.name, patient.gender,
                                                                patient.get_language_display(),
                                                                patient.schedule.strftime('%H:%M'),
                                                                patient.timezone)
    context.bot.send_message(chat_id=patient.identifier, text=message, parse_mode=ParseMode.HTML)
    return config_menu(update, context)


@send_typing_action
def ask_delete_user(update, context):
    """
    Asks for confirmation to completely delete the user from the system.
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} wants to delete his account.')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['delete_user'],
                             reply_markup=keyboards.delete_user_keyboard[patient.language])
    return PROCESS_DELETE_USER


@send_typing_action
def ask_change_schedule(update, context):
    """
    Sends old schedule to the user and asks for the new one
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} asked to change schedule')
    schedule = patient.schedule.strftime("%H:%M")
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['current_schedule'] + schedule)
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['change_schedule'],
                             reply_markup=keyboards.back_keyboard[patient.language])
    return PROCESS_SCHEDULE


@send_typing_action
@run_async
def process_change_schedule(update, context):
    """
    Saves the new schedule, deletes previous jobs and creates updated ones.
    """
    patient = context.user_data['patient']

    # Get new schedule from msg and set it
    new_schedule = update.message.text
    patient.schedule = new_schedule
    patient.save(update_fields=['_schedule'])

    # Remove old job and create a new one with the new schedule
    for old_job in context.job_queue.get_jobs_by_name(f'{patient.identifier}_pending_questions_job'):
        old_job.schedule_removal()
    PendingQuestionJob(context, patient)

    logger.info(f'User {patient.username} changed schedule to {patient.schedule}')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['schedule_updated'])

    return config_menu(update, context)


@send_typing_action
def process_wrong_schedule(update, context):
    """
    Informs that the patient introduced a wrong schedule
    """
    patient = context.user_data['patient']
    text = update.message.text
    logger.info(f'User {patient.username} introduced an invalid schedule ({text})')
    context.bot.send_message(chat_id=patient.identifier,
                             text=messages[patient.language]['invalid_schedule'].format(text),
                             reply_markup=keyboards.back_keyboard[patient.language])

    return PROCESS_SCHEDULE


@send_typing_action
def ask_change_timezone(update, context):
    """
    Asks a patient to change his timezone
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} asked to change timezone')
    current_timezone = patient.timezone
    context.bot.send_message(chat_id=patient.identifier,
                             text=messages[patient.language]['current_timezone'] + current_timezone)
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['change_timezone'],
                             reply_markup=keyboards.change_timezone_keyboard[patient.language])
    return PROCESS_TIMEZONE


@send_typing_action
def process_change_timezone(update, context):
    """
    Calculates timezone from the provided location and sets it
    """
    patient = context.user_data['patient']
    patient_timezone = Patient.get_timezone_from_location(update.message.location)
    patient.timezone = patient_timezone
    patient.save(update_fields=["timezone"])
    logger.info(f'User {patient.username} choose timezone {patient_timezone}')
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['timezone_updated'])

    return config_menu(update, context)


@send_typing_action
def default_timezone(update, context):
    """
    Sets default timezone to a patient (Europe/Madrid)
    """
    update.callback_query.answer()
    patient = context.user_data['patient']
    logger.info(f'Set default timezone (Europe/Madrid) for user {patient.username}')
    patient.timezone = "Europe/Madrid"
    patient.save(update_fields=["timezone"])
    context.bot.send_message(chat_id=patient.identifier, text=messages[patient.language]['timezone_updated'])

    return config_menu(update, context)


@send_typing_action
@run_async
def process_delete_user(update, context):
    """
    Deletes the user from the system.
    """
    update.callback_query.answer()

    # Get patient id
    patient = context.user_data['patient']
    chat_id = patient.identifier
    language = patient.language

    # Log it
    logger.info(f'User {patient.username} deleted his account.')

    # Delete the patient
    patient.delete()

    # Finish conversation
    context.bot.send_message(chat_id=chat_id, text=messages[patient.language]['deleted_user'],
                             reply_markup=keyboards.start_keyboard[language])
    return ConversationHandler.END


@send_typing_action
def back(update, context):
    """
    Cancels current action and shows config menu
    """
    update.callback_query.answer()
    username = context.user_data["patient"].username
    logger.info(
        f'User {username} cancelled current operation.')
    return config_menu(update, context)


@send_typing_action
def _exit(update, context):
    """
    Exits from the configurator
    """
    patient = context.user_data['patient']
    logger.info(f'User {patient.username} close the configurator.')

    update.callback_query.answer()
    update.callback_query.edit_message_text(messages[patient.language]['exit_configurator'])
    return ConversationHandler.END


config_handler = ConversationHandler(
    entry_points=[CommandHandler('config', config)],
    states={
        CHOOSING: [
            CallbackQueryHandler(ask_profile_pic, pattern="^changepic$"),
            CallbackQueryHandler(ask_change_name, pattern="^changename$"),
            CallbackQueryHandler(ask_change_timezone, pattern="^changetimezone$"),
            CallbackQueryHandler(ask_change_gender, pattern="^changegender$"),
            CallbackQueryHandler(ask_change_schedule, pattern="^changeschedule"),
            CallbackQueryHandler(ask_change_language, pattern="^changelanguage$"),
            CallbackQueryHandler(view_profile, pattern="^viewprofile$"),
            CallbackQueryHandler(ask_delete_user, pattern="^deleteuser$"),
        ],
        PROCESS_GENDER: [
            CallbackQueryHandler(process_gender, pattern="^(Male|Female|Other)$")
        ],
        PROCESS_PROFILE_PIC: [
            MessageHandler(Filters.photo, process_profile_pic)
        ],
        PROCESS_NAME: [
            MessageHandler(~is_answering_filter & ~Filters.command, process_name)
        ],
        PROCESS_LANGUAGE: [
            CallbackQueryHandler(process_language, pattern='^(ES|GB)$')
        ],
        PROCESS_DELETE_USER: [
            CallbackQueryHandler(process_delete_user, pattern="^deleteuser$")
        ],
        PROCESS_SCHEDULE: [
            MessageHandler(Filters.regex('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'), process_change_schedule),
            MessageHandler(~Filters.regex('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'), process_wrong_schedule)
        ],
        PROCESS_TIMEZONE: [
            MessageHandler(Filters.location, process_change_timezone),
            CallbackQueryHandler(default_timezone, pattern="^default-timezone$")
        ]

    },
    fallbacks=[
        CallbackQueryHandler(back, pattern="^back$"),
        CallbackQueryHandler(_exit, pattern="^exit$")
    ],
    name="configurator"
)
