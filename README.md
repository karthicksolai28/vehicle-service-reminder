# Vehicle Service Reminder

Bike / car service dates track panni, next service eppo due nu kaattum Django web app.

## Features
- User signup / login (ovvoru user-um avanga vehicles mattum paapanga)
- Vehicle and service record add, edit, delete
- Auto next service date (last service + 90 days) and next km (+ 3000 km)
- Status: OK, Due soon, Overdue
- Dashboard: total vehicles, overdue, due soon, total spent
- Vehicle search by name or number
- Admin panel
- Email reminder command for overdue / due soon vehicles

## Tech
Python, Django, SQLite, HTML, CSS

## Setup
```bash
git clone <git clone https://github.com/karthicksolai28/vehicle-service-reminder.git>
cd service_reminder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Send reminders
```bash
python manage.py send_reminders
```
Emails console-la print aagum. Real email venum na `MAILERS` setting-a SMTP-ku maathalam.

## Screenshots
(Screenshots inga add pannalam)