# WSU Triangle Fraternity Test Exam
Created for the WSU Hackathon 2024, this is a web application that allows members of the WSU Triangle Fraternity
to upload exams and other study materials to a central location. Uses Azure Blob storage to store files and a Flask
backend to serve the files and metadata to the frontend.

# Backend

## How to run the backend
`cd Backend`
`pip install -r requirements.txt`
`docker-compose up`
`flask run`

## How to run the tests
`cd Backend`
`pytest ./tests/tests.py`


# Frontend

Notice that the frontend is a little thrown together. We spent most of our time unit testing the backend and making sure it was as robust as possible. We did not have time to make the frontend as pretty as we would have liked. We hope you understand.

## How to run the frontend
`cd Frontend`
`npm ci`
`npm run start`
