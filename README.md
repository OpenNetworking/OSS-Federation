#API for android client

###GET api/polis

#####Description
get polis list

#####Request example
	curl -X GET http://127.0.0.1:8000/api/polis

#####Response example
	{
        "data": [
            {
                "register_url": "http://www.aipu.com/api/register",
                "name": "Aipu"
            },
            {
                "register_url": "http://www.bipu.com/api/register",
                "name": "Bipu"
            },
            {
                "register_url": "http://www.cipu.com/api/register",
                "name": "Cipu"
            }
        ]
    }
