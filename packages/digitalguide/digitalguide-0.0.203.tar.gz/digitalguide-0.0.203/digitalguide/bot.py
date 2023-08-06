#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from collections import defaultdict
from configparser import ConfigParser

from digitalguide import (contextActions, conversationActions, imageActions,
                          listenfrageActions, schaetzfragenActions,
                          writeActions)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

config = ConfigParser()
config.read("config.ini")


LOG_USER = (os.getenv('LOG_USER', 'True') == 'True')
LOG_INTERAKTION = (os.getenv('LOG_INTERAKTION', 'True') == 'True')
RUN_LOCAL = (os.getenv('RUN_LOCAL', 'False') == 'True')

MESSANGER = os.getenv('MESSANGER', 'Telegram')

if MESSANGER == "Telegram":
    from digitalguide.errorHandler import error_handler
    from digitalguide.generateActions import (callback_query_handler,
                                                read_action_yaml)
    from digitalguide.generateStates import read_state_yml
    from telegram.ext import (CallbackQueryHandler, CommandHandler,
                                ConversationHandler, Filters, MessageHandler,
                                Updater)
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    PORT = int(os.environ.get('PORT', '8080'))

    #my_persistence = DBPersistence("klimafuehrung_persistencedb")
    updater = Updater(TOKEN,
                        # persistence=my_persistence,
                        use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    action_functions = {**contextActions.telegram_action_functions,
                        **listenfrageActions.telegram_action_functions,
                        **conversationActions.telegram_action_functions,
                        **schaetzfragenActions.telegram_action_functions,
                        **imageActions.telegram_action_functions,
                        **writeActions.telegram_action_functions,
                        }

    generalActions = read_action_yaml(
        "actions/telegram_general.yml", action_functions=action_functions, log_user=LOG_USER, log_interaction=LOG_INTERAKTION)

    cqh = callback_query_handler({**generalActions})

    prechecks = [CommandHandler('start', generalActions[config["bot"]["start_action"]]),
                    CallbackQueryHandler(cqh)]

    conv_handler = ConversationHandler(
        allow_reentry=True,
        per_chat=False,
        conversation_timeout=6 * 60 * 60,
        entry_points=[CommandHandler(
            'start', generalActions[config["bot"]["start_action"]])],
        # persistent=True,
        name=config["bot"]["bot_name"],

        states={
            **read_state_yml("states/telegram_general.yml", actions={**generalActions}, prechecks=prechecks),

            ConversationHandler.TIMEOUT: [MessageHandler(Filters.regex(r'^(.)+'), generalActions["timeout"])],
        },

        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error_handler)


elif MESSANGER == "WhatsApp":
    from digitalguide.whatsapp.generateActions import read_action_yaml
    from digitalguide.whatsapp.generateStates import (CommandHandler,
                                                        read_state_yml)
    from digitalguide.whatsapp.WhatsAppUpdate import WhatsAppUpdate
    from flask import Flask, Response, request
    from twilio.rest import Client

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    app = Flask(__name__)

    user_states = defaultdict(lambda: "START_START")
    user_context = defaultdict(dict)

    action_functions = {**contextActions.whatsapp_action_functions,
                        **listenfrageActions.whatsapp_action_functions,
                        **schaetzfragenActions.whatsapp_action_functions,
                        **imageActions.whatsapp_action_functions,
                        **writeActions.whatsapp_action_functions,
                        }

    general_actions = read_action_yaml("actions/whatsapp_general.yml", action_functions=action_functions)

    prechecks = [CommandHandler('start', general_actions[config["bot"]["start_action"]]),
                    ]

    general_handler = read_state_yml("states/whatsapp_general.yml", actions={
                                        **general_actions}, prechecks=prechecks)

    @app.route('/bot', methods=['POST'])
    def bot():
        print(request.values)
        update = WhatsAppUpdate(**request.values)
        icoming_state = user_states[update.From]
        context = user_context[update.From]

        print("Current context: {}".format(context))
        print("Current state: {}".format(icoming_state))
        print("Update: {}".format(str(request.values)))

        for handler in prechecks + general_handler[icoming_state]:
            print("Filter Eval: {}".format(handler))
            if handler.check_update(update):
                print("Filter True: {}".format(handler))
                new_state = handler.callback(client, update, context)
                if new_state:
                    user_states[update.From] = new_state
                break
        return Response(status=200)

if __name__ == '__main__':
    if MESSANGER == "Telegram":
        if RUN_LOCAL:
            updater.start_polling()
        else:
            updater.start_webhook(listen="0.0.0.0",
                                    port=PORT,
                                    url_path=TOKEN,
                                    webhook_url=os.environ.get("APP_URL") + TOKEN)

    updater.idle()

    if MESSANGER == "WhatsApp":
        app.run()