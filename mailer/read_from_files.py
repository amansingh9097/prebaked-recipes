# Function to read the contacts from a given contacts file and return a list
# of names and email addresses
from string import Template

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            # check if not commented out
            if contact[0] != '#':
                names.append(contact.split()[0])
                emails.append(contact.split()[1])
        return names, emails

def read_template(filename):
    with open(filename, mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
