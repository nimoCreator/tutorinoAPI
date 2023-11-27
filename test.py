from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return "Hello"

@app.get("/user")
async def getUser(name: str):
    return userinfo

@app.post("/newOffer")
async def postOffer():

@app.put("/updateOffer")
async def updateOffer():

@app.delete("/deleteOffer")
async def deleteOffer():

