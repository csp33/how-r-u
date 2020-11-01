current_template = 'Your current {} is '
new_template = 'Introduce your new {}:'
updated_template = 'Your {} has been successfully updated.'
messages = {
    "ES": {
        "choose_gender": "Por favor escoge tu género:",
        "choose_pic": "Por favor, envía una foto tuya o pulsa /skip si no quieres.",
        "choose_schedule": "Por favor elige la hora a la que quieres recibir las preguntas en formato HH:MM (24h)",
        "registration_ok": "Te has registrado correctamente en el sistema.",
        "exit_configurator": "Saliendo del menú de configuración...",
        "select_config": "Elige la configuración que deseas cambiar. Puedes pulsar /cancel en cualquier momento para "
                         "volver atrás o /exit para salir.",
        "change_picture": "Envía la nueva foto:",
        "current_picture": "Tu foto de perfil actual es la siguiente:",
        "picture_updated": "La imagen de perfil se ha actualizado.",
        "already_exists": "Ya se ha registrado antes.",
        "current_name": "Tu nombre actual es ",
        "change_name": "Introduce tu nuevo nombre:",
        "name_updated": "Tu nombre se ha actualizado.",
        "current_gender": "Tu género actual es ",
        "change_gender": "Introduce tu nuevo género:",
        "gender_updated": "Tu género se ha actualizado.",
        "current_schedule": "Tu horario actual es ",
        "change_schedule": "Introduce tu nuevo horario:",
        "schedule_updated": "Tu horario se ha actualizado",
        "current_language": "Tu idioma actual es ",
        "change_language": "Introduce tu nuevo idioma:",
        "language_updated": "Tu idioma se ha actualizado.",
        "no_questions": "No hay preguntas para hoy. ¡Nos vemos mañana!",
        "show_profile": "Estos son los datos de tu perfil:\n<b>Nombre</b>: {}\n<b>Género</b>: {}\n<b>Idioma</b>: {}\n<b>Horario</b>: {}",
        "delete_user": "¿Estás seguro de que deseas borrar tu usuario?\nAún puedes pulsar /cancel para volver atrás o /exit para salir de la configuración.",
        "deleted_user": "Usuario eliminado. Pulsa el botón de abajo para volver a registrarte.",
        "finish_answering": "Esas son todas las preguntas por hoy. ¡Gracias!"
    },
    "GB": {
        "choose_gender": "Please choose your gender:",
        "choose_pic": "Please send a photo of yourself or send /skip if you don\'t want to.",
        "choose_schedule": "Please specify the time when you would like to receive questions in HH:MM format (24h).",
        "registration_ok": "You have been successfully registered into the system.",
        "exit_configurator": "Leaving configuration menu...",
        "select_config": "Choose the configuration you want to change. You can press /cancel anytime to cancel the current operation or /exit to exit.",
        "change_picture": "Please send the new profile picture:",
        "current_picture": current_template.format('profile picture'),
        "picture_updated": updated_template.format('profile picture'),
        "already_exists": "You are already registered.",
        "current_name": current_template.format('name'),
        "change_name": new_template.format('name'),
        "name_updated": updated_template.format('name'),
        "current_gender": current_template.format('gender'),
        "change_gender": new_template.format('gender'),
        "gender_updated": updated_template.format('gender'),
        "current_language": current_template.format('language'),
        "change_language": new_template.format('language'),
        "language_updated": updated_template.format('language'),
        "current_schedule": current_template.format('schedule'),
        "change_schedule": new_template.format('schedule'),
        "schedule_updated": updated_template.format('schedule'),
        "no_questions": "There are no questions for today. See you tomorrow!",
        "show_profile": "These are your profile data:\n<b>Name</b>: {}\n<b>Gender</b>: {}\n<b>Language</b>: {"
                        "}\n<b>Schedule</b>: {}",
        "delete_user": "Are you sure you want to delete your user?\nYou can still press /cancel to go to the previous "
                       "menu or /exit to leave the configuration.",
        "deleted_user": "Your user has been deleted. Press the button below to register again.",
        "finish_answering": "You finished answering today's questions. Thanks!"
    }
}
