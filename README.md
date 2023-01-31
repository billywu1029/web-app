# Placements.io Coding Assessment

Web app to solve the following use case:
Given a set of line-items, create a web app to allow users to maintain an adjustable invoice.

The features I decided to implement were as follows:
1. Displaying line-item data in a paginated table
    - Decided that this was a pretty logical first step for a web app. It involved quite a bit more front end than I ever work with, including Python's Flask library, flask SQLAlchemy, HTML, CSS, and Jinja.
    - I went with Flask for the web app itself, flask SQLAlchemy for a basic DB backend, and basic HTML/CSS for UI since I thought these would be the most straightforward for a demo web app. I'm aware that if I wanted more functionality I'd use Django or React/JS.
    - I saw that the JSON was around 3MB and later that the table had 10000 rows (line-items). It would be overkill to use fancy databases since Flask's SQLAlchemy would already do for this small dataset. 
2. Having a column in the table for each line-item's billable amount (actual_amount + adjustments)
    - This and the invoice grand total seemed very simple as long as the UI didn't pose problems. I knew how to get both from SQL queries so it was just a matter of displaying them properly (and figuring out how to run SQL queries in Flask).
3. Show invoice grand total, and calculate invoice totals for different campaign id's.
4. Integration with Amazon S3 - ability to export the uploaded JSON to an S3 bucket
    - I thought that this would be an appropriate challenge since I always wanted to learn more about using AWS since it's so ubiquitous. I do think that the integration I did covered most of the hard work of Amazon S3 setup; however, I didn't actually export the db itself. For the sake of simplicity and proof of concept I decided to go ahead and just upload the JSON itself to S3. I would imagine that extending this to export the DB wouldn't be too much more effort.
    - In order to store the AWS Access Key and the secret key, I went ahead with the design pattern of a .env file along with a config.py to store the environment variables. This would avoid hardcoding secrets and also decouple the secrets from the app's code itself, which is good practice as far as I'm aware.

In a future iteration, I'd extend these features for the following functionality:
- Fancier UI for the table to visually support easy SQL queries filtering/sorting on different columns
- Allow UI to support editing the adjustments field for a line-item (just a SQL update on backend)
- Put invoice grand total on the same page as the line-items table and adjust that sum value whenever filters are applied
- Convert the server's database itself into a CSV etc and then save it in the S3 bucket (so that edits on the table via web app would be reflected)

## Setup

1. In the terminal or your favorite IDE of choice (I used Pycharm since it's just born to do these kinds of quick proof of concept programs), create a Python virtual environment according to `requirements.txt`.
2. If you already have an AWS account with an S3 bucket, a user, and a user group, then skip to the next step. Otherwise, follow the instructions in this wonderful [blog](https://kishstats.com/aws/2018/03/15/aws-create-new-user.html).
3. Create a `.env` file. Put the following three lines of env vars:
```
export S3_BUCKET=<your S3 Bucket here>
export S3_KEY=<your S3 Access Key here>
export S3_SECRET=<your S3 Secret Access Key here>
```
4. Now activate your venv if you haven't already, and `flask run` (or run `main.py`).
5. Open up http://localhost:5000/

## Site Navigation
The "intended" usage of the web app is the following (some limited error handling exists):
1. Upload the JSON data of line-items. Get redirected to the line-item display page with the paginated table.
    - Uploading a new JSON overrides the old one on the server, on your S3 bucket, and the DB. This was done for simplicity's sake.
    - All non-JSON files are detected and removed by default too, to avoid any obvious file processing issues.
2. Go to Invoice to see the grand total amount.
    - There's no UI for this, but if you add a "/<`campaign_id`>" to the Invoice URL, it returns the invoice for just the line-items from this `campaign_id`.
3. Check the JSON on your S3 bucket for fictitious downstream purposes.
