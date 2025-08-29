from fastapi import FastAPI
import uvicorn
from app.parser import get_top_vacancies
from app.models import Vacancy

app = FastAPI()

@app.get("/health", summary="CHECK")
def health():
    return {"status": "ok"}

@app.get("/vacancies", response_model=list[Vacancy])
def vacancies():
    return get_top_vacancies()



def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
    