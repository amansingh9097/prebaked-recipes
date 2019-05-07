# notify me to update my today's tasks in mail_body.txt file
# for the mailer to send the maile to Meg

# using win10toast to show notification at the bottom-right of the screen
from win10toast import ToastNotifier

toaster = ToastNotifier()

toaster.show_toast("AAJ KYA UKHAD LIYA??", "Update your today's tasks in 'aaj_kya_kiya.txt' before 5 pm IST.")
