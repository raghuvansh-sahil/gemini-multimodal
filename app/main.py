import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File
from receipt import process_image
from database import initialise_database, insert_receipt_inDB, get_receipts_fromDB
from categories import initialise_categorized_spending, populate_categorized_spending, get_categorized_spending
from spending import spending_per_day, spending_per_month, spending_per_year

app = FastAPI()
gemini_model = None

@app.on_event("startup")
def on_startup():
    global gemini_model
    genai.configure(api_key='AIzaSyCn_qLK6GuFHcACihDgS9xaQ_OTSwyQylg')
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')

    initialise_database()

@app.post("/insert-receipt")
async def insert_receipt(image: UploadFile = File(...)):
    image_bytes = await image.read()
    receipt = process_image(gemini_model, image_bytes)

    if receipt is not None:
        insert_receipt_inDB(receipt)
    
    return receipt

@app.get('/get-receipts')
def get_receipts():
    receipts = get_receipts_fromDB()
    return receipts

@app.get('/get-pie-chart')
def get_pie_chart():
    categorized_spending = get_categorized_spending()
    return categorized_spending

@app.get('/get-daily-spendings')
def get_daily_spendings():
    daily_spendings = spending_per_day()
    return daily_spendings

@app.get('/get-monthly-spendings')
def get_monthly_spendings():
    monthly_spendings = spending_per_month()
    return monthly_spendings

@app.get('/get-yearly-spendings')
def get_yearly_spendings():
    yearly_spendings = spending_per_year()
    return yearly_spendings