from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 APP STARTING...")

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "model_supplier.csv")

print("📂 PATH:", file_path)

try:
    model_df = pd.read_csv(file_path)
    print("✅ CSV LOADED:", model_df.shape)
except Exception as e:
    print("❌ ERROR LOADING CSV:", e)
    model_df = pd.DataFrame()  # biar app tetap jalan

@app.get("/recommend")
def recommend(barang: str):
    if model_df.empty:
        return {"error": "Data tidak tersedia"}

    hasil = model_df[
        model_df['description_barang']
        .str.contains(barang, case=False, na=False)
    ]

    hasil = hasil.sort_values('final_score', ascending=False).head(15)

    return hasil.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 9000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
