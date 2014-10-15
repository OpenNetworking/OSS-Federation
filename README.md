#API for android client

##Setup
    git clone https://github.com/OpenNetworking/OSS-Federation.git
    cd OSS-Federation
    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
    python manage.py runserver
    
    

##Test Server
Host: [140.112.29.198:9999](http://140.112.29.198:9999)

##API List
- [GET api/polis](#api_polis)
- [GET api/colors](#api_colors)

##<a name="api_polis"></a>GET api/polis

#####Description
get polis list

#####Request example
	curl -X GET http://127.0.0.1:8000/api/polis

#####Response example
	{
        "data": [
            {
                "colors": [
                    {
                        "color_number": 1
                    },
                    {
                        "color_number": 2
                    },
                    {
                        "color_number": 3
                    }
                ],
                "register_url": "http://www.aipu.com/api/register",
                "name": "Aipu"
            },
            {
            	"colors": [
                    {
                        "color_number": 4
                    }
                ],
                "register_url": "http://www.bipu.com/api/register",
                "name": "Bipu"
            },
            {
                "colors": [],
                "register_url": "http://www.cipu.com/api/register",
                "name": "Cipu"
            }
        ]
    }
    
    
##<a name="api_colors"></a>GET api/colors

#####Description
get colors list

#####Request example
	curl -X GET http://127.0.0.1:8000/api/colors

#####Response example
	{
        "data": [
            {
                "polis_name": "aipu",
                "color_number": 1
            },
            {
                "polis_name": "aipu",
                "color_number": 2
            },
            {
                "polis_name": "bipu",
                "color_number": 3
            }
        ]
    }
