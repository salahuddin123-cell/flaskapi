CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})