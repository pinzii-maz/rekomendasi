from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_df = pd.read_csv("model_supplier.csv")

@app.get("/recommend")
def recommend(barang: str):
    hasil = model_df[
        model_df['description_barang']
        .str.contains(barang, case=False, na=False)
    ]
    hasil = hasil.sort_values('final_score', ascending=False)
    return hasil.to_dict(orient='records')

