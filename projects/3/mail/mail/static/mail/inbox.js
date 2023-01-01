/*
To do:
Create different views for inbox and outbox (doing that in the add email function by getting different parameters additionally)
[] Loading E-Mails after sending will miss the just sent e-mail
[] init emails with unread
*/


document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#email').addEventListener('click', () => read_email(id));
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    send_email()
      .then(load_mailbox('sent'));
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function read_email(id) {
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // add e-mails to the view via add_email
  fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(add_email);
    })
}

function send_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    });

  return false;
}

function add_email(contents) {
  email = document.createElement('div');
  email.className = 'email-view';

  email.innerHTML = `<a
                      <div class="info">
                      <div class="participants">
                        <div class="from"><b>From:</b> ${contents.sender}</div>
                        <div class="to"><b>To:</b> ${contents.recipients}</div>
                      </div>
                      <div class="timestamp"><b>Date:</b> ${contents.timestamp}</div>
                    </div>
                    <div class="subject">${contents.subject}</div>
                    <div class="body">${contents.body.slice(0, 30)}</div>`;

  if (contents.read === true) {
    email.style.backgroundColor = "lightgrey";
  }

  // Add email to DOM
  document.querySelector('#emails-view').append(email);
}