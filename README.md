# WSU Triangle Fraternity Test Exam
NOTICE: This repo is being kept in its exact state after submission for the competition. A forked repo will be used to continue development on this outside of competititon.

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

The frontend was thrown together in about 3 hours, as we spent most of our time unit testing and getting 100% code coverage on our backend.
It simply contains a search bar and displays results. The code is very ugly, as we needed to hack it together fast with our remaining time.

## How to run the frontend
`cd Frontend`
`npm ci`
`npm run start`
