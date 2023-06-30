# apis-prototype
Amadeus Prototype APIs

## How to run the project locally using docker
Run the below command from inside the folder.
```sh
docker compose up
```

Then you should be able to access it the browser using `http://127.0.0.1:8000/`

## How to run the project locally

Clone the repository.

### Create a venv inside the folder:

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start the server 
Finally, run the Django server.

```sh
python amadeus_demo_api/manage.py runserver
```

Finally, open a browser and go to `http://127.0.0.1:8000/`
