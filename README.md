# Fam Pay Task

# Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

# Basic Requirements:

- [X] Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- [X] A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- [X] A basic search API to search the stored videos using their title and description.
- [X] Dockerize the project.
- [X] It should be scalable and optimised.

# Bonus Points:

- [X] Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
- [ ] Make a dashboard to view the stored videos with filters and sorting options (optional)
- [X] Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.
    - Ex 1: A video with title *`How to make tea?`* should match for the search query `tea how`

# Instructions:

- You are free to choose any search query, for example: official, cricket, football etc. (choose something that has high frequency of video uploads)
- Try and keep your commit messages clean, and leave comments explaining what you are doing wherever it makes sense.
- Also try and use meaningful variable/function names, and maintain indentation and code style.
- Submission should have a `README` file containing instructions to run the server and test the API.
- Accepted language & Framework
    1. Python (DRF, Django, Flask, etc)
    2. GoLang
    3. JavaScript
- Send your submission (Git repository) link at hiring@fampay.in

# Reference:

- YouTube data v3 API: [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)
- Search API reference: [https://developers.google.com/youtube/v3/docs/search/list](https://developers.google.com/youtube/v3/docs/search/list)
    - To fetch the latest videos you need to specify these: type=video, order=date, publishedAfter=<SOME_DATE_TIME>
    - Without publishedAfter, it will give you cached results which will be too old
