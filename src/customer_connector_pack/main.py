from fastapi import FastAPI

app = FastAPI(title="Customer Connector Pack")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
