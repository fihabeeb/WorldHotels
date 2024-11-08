# Web Development Project - World Hotels

During the first year of my computer science course, I was tasked with created a functional hotel booking website on my own (no group). This readme will go into some detail about the process of making this project, as well as a short self assessment at the end.

## Step 1 - HTML and CSS

The course started by teaching us HTML and then CSS. So the first steps in the project was to create the front-end portion of the website. As this was a solo first year project, the expected quality of the final product was not so steep. We used basic HTML and CSS to create the main page, as well as the login page of the website. We learnt to use functions like Django extension
```HTML
{% extends "base.html" %}
```
and CSS classes and IDs
```CSS
    .text_Box_2_text{
    margin-left: 1%;
    margin-right: 1%;
    margin-top: 10px;
    margin-bottom: 10px;
}
```
to make the development process more efficient.

## Step 2 - Database Design

The next part of the project dealt with the database side of things. We needed a database to store the information for all the hotels, and also the customers and the administrators. Also stored in the database is payment records. The database contains 5 tables:

User Information:
- User Information ID
- Name
- Surname
- Email
- PhoneNumber
..* User_Password
..* Privilages

## How to install??

SELECT * FROM UserInformation;
SELECT * FROM HotelInformation;
SELECT * FROM Billings;
SELECT * FROM Room;
SELECT * FROM BookingTable;