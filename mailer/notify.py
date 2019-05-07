# notify me to update my today's tasks in mail_body.txt file
# for the mailer to send the maile to Meg

from win10toast import ToastNotifier

toaster = ToastNotifier()

toaster.show_toast("mailer asks:", "AAJ KYA UKHADA BETA??\n\nTASKS UPDATE KAR body_mail.txt ME...")
