from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_custom_keyboard(responses):
    """
    Creates a custom keyboard with response values.
    :param responses (str)
    """
    schema = [
        [InlineKeyboardButton(str(response), callback_data=f'response-{response.id}')] for response in responses
    ]
    return InlineKeyboardMarkup(schema)


gender_keyboard = {
    'ES': InlineKeyboardMarkup([
        [
            InlineKeyboardButton('♂️Masculino', callback_data="Male"),
            InlineKeyboardButton('♀️Femenino', callback_data="Female")
        ],
        [
            InlineKeyboardButton('🏳️‍🌈 Otro', callback_data="Other")
        ]
    ]
    ),
    'GB': InlineKeyboardMarkup([
        [
            InlineKeyboardButton('♂️Male', callback_data="Male"),
            InlineKeyboardButton('♀️Female', callback_data="Female")
        ],
        [
            InlineKeyboardButton('🏳️‍🌈 Other', callback_data="Other")
        ]
    ]
    )
}
language_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇪🇸", callback_data="ES"),
        InlineKeyboardButton("🇬🇧", callback_data="GB")
    ]
]
)
delete_user_keyboard = {
    'ES': InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❌ Sí, eliminar mi usuario", callback_data="deleteuser")
            ],
            [
                InlineKeyboardButton("🔙 Atrás", callback_data="back"),
            ]
        ]
    ),
    'GB': InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❌ Yes, delete my user", callback_data="deleteuser")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back"),
            ]
        ]

    )
}
skip_keyboard = {
    'ES': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏭️Saltar", callback_data="skip"),
        ]
    ]
    ),
    'GB': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏭️Skip", callback_data="skip"),
        ]
    ]
    )
}

back_keyboard = {
    'ES': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Atrás", callback_data="back"),
        ]
    ]
    ),
    'GB': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
        ]
    ]
    )
}

start_keyboard = {
    "ES": InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Crear una cuenta de nuevo", callback_data="start"),
        ]
    ]
    ),
    "GB": InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Create an account again", callback_data="start"),
        ]
    ]
    )
}

config_keyboard = {
    'ES': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🖼️ Cambiar imagen de perfil", callback_data="changepic"),
        ],
        [
            InlineKeyboardButton("🔤 Cambiar nombre", callback_data="changename"),
            InlineKeyboardButton("🌈 Cambiar género", callback_data="changegender")
        ],
        [
            InlineKeyboardButton("🌐 Cambiar idioma", callback_data="changelanguage"),
            InlineKeyboardButton("⏰ Cambiar horario", callback_data="changeschedule")
        ],
        [
            InlineKeyboardButton("📝 Ver mi perfil", callback_data="viewprofile"),
            InlineKeyboardButton("🗑️ Borrar usuario", callback_data="deleteuser")
        ],
        [
            InlineKeyboardButton("🚪️ Salir", callback_data="exit")
        ]
    ]
    ),
    'GB': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🖼️ Change profile picture", callback_data="changepic"),
        ],
        [
            InlineKeyboardButton("🔤 Change name", callback_data="changename"),
            InlineKeyboardButton("🌈 Change gender", callback_data="changegender"),
        ],
        [
            InlineKeyboardButton("🌐 Change language", callback_data="changelanguage"),
            InlineKeyboardButton("⏰ Change schedule", callback_data="changeschedule"),
        ],
        [
            InlineKeyboardButton("📝 View my profile", callback_data="viewprofile"),
            InlineKeyboardButton("🗑️ Delete user", callback_data="deleteuser")
        ],
        [
            InlineKeyboardButton("🚪️ Exit", callback_data="exit")
        ]
    ]
    )
}
