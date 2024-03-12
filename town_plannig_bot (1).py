#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging
import sqlite3
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "6377690221:AAEcjWc1AscC1laDs-OBgdzpUC1FrYm8vE8"

# Google Drive API setup
SERVICE_ACCOUNT_FILE = 'https://github.com/townplanningrajasthan/telegram_bot/blob/390b66eb5f04d73dbfc3ec2b234acc9c7c10bba8/telegram-417006-885d9de0f13f.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Temporary directory to store PDF files before uploading
TEMP_DIR = 'temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


def start(update, context):
    update.message.reply_text("Welcome to the PDF Bot! Send me a PDF file to store it in Google Drive.")


def store_pdf(update, context):
    document = update.message.document
    file_id = document.file_id
    file_name = document.file_name
    file_path = os.path.join(TEMP_DIR, file_name)

    # Download the PDF file to a temporary directory
    file = context.bot.get_file(file_id)
    file.download(file_path)

    # Upload the PDF file to Google Drive
    file_metadata = {'name': file_name}
    media = {'mimeType': 'application/pdf', 'body': open(file_path, 'rb')}
    drive_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Delete the temporary file
    os.remove(file_path)

    update.message.reply_text("PDF successfully stored in Google Drive with ID: {}".format(drive_file.get('id')))


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document.pdf, store_pdf))  # Handler for PDF documents

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

