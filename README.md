# snake-api

### download on [app store](https://itunes.apple.com/us/app/snake-professional/id1040358770?mt=8)

### run locally
* run a mongo database named `snake`
* install python 3
* create virtualenv `virtualenv -p python3 venv`
* run the virtualenv `source ven/bin/activate`
* install dependencies `pip3 install -r requirements.txt`
* run the server `python3 main.py`

### deploying
* clone [ecs-deploy](https://github.com/silinternational/ecs-deploy) into a ~/src folder
* `bash deploy.sh testing | production`
