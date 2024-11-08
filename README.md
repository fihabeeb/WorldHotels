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

- UserInformation: Stores things like email, password (encrypted), and user ID. Also stores the user's administration level.
- HotelInformation: Stores information about each hotel, including its city, and prices.
- Billings: Stores all transactions, including received payments and refunds
- Room: When a customer buys a hotel, a record is generated and placed in this table. It holds the room number, and which hotel the room is in
- BookingTable: Stores all bookings made. Holds information like the check in and check out date, and the user id of the one who booked.


## Step 3 - Back-End Development using Python Flask

Now that the front end (HTML and CSS) and the Database has been made, what's left is the backend to put those two together but to also add more functionality. Our module required us to use Python Flask.