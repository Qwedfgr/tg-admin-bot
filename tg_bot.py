import json
import os

import dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tools_1c import Cluster

import tools
from df_utils import get_answer

dotenv.load_dotenv()
SETTINGS = tools.read_settings()
PROJECT_ID = os.environ['project_id']


def main():
    token_tg = os.environ["TOKEN_TG"]
    try:
        run_tg_bot(token_tg)
    except Exception as error:
        print(error)


def run_tg_bot(token_tg):
    updater = Updater(token_tg)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, dialog))

    updater.start_polling()

    updater.idle()


def start(bot, update):
    update.message.reply_text('Здравствуйте!')


def dialog(bot, update):
    print(update.message.text)
    answer, json_response = get_answer(update.message.chat_id, [update.message.text], 'ru')
    print(answer)
    update.message.reply_text(answer)
    update.message.reply_text('dwdew')

    if json_response.get('allRequiredParamsPresent'):
        handle_functions = {
            'terminate-session': terminate_session,
            'create-infobase': create_infobase,
            'set-schedule-jobs-lock': set_schedule_jobs_lock
        }
        handler = handle_functions[json_response['action']]
        data = json.dumps(json_response['parameters'])
        handler(data)


def terminate_session(data):
    cluster_name, ib_name = tools.get_cluster_and_ib_name(data['connection_string'])
    cluster = Cluster(cluster_name, SETTINGS)
    cluster.terminate_sessions(ib_name)


def set_schedule_jobs_lock(data):
    cluster_name, ib_name = tools.get_cluster_and_ib_name(data['Connection'])
    cluster = Cluster(cluster_name, SETTINGS)
    cluster.set_schedule_jobs_lock(ib_name, mode=data['mode'], username=data['username'], pwd=data['pwd'])


def create_infobase(data):
    cluster_name = tools.get_cluster_by_version(data['version'])
    cluster = Cluster(cluster_name, SETTINGS)
    cluster.create_infobase(data['ib_name'])


if __name__ == '__main__':
    main()
