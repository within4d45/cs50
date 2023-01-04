/*
To do:
ReCreate different views for inbox and outbox (doing that in the add email function by getting different parameters additionally)
[x] Loading E-Mails after sending will miss the just sent e-mail
[x] init emails with unread
[] Error handling: 
  [] after sending: when object is message, do one, else redo email (if the email-address exists, if it doesn't, then handle the error)
  [] same with having no subject or address
[] fetching the user and do the following:
  [] don't show archive and unarchive buttons to the sender of the email
  [] don't show the reply button when the user is the one who has sent the email

Questions:
email-cards:
- making the anchor element pointy - is that good code 
- when we are in the overview, we have already fetched the e-mail contents - why do we want to fetch them again?
*/


document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    return false;
  };

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients = '', subject='', body='') {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#read-email').style.display = 'none';
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

  // Add "No Subject" when somebody has not entered any subject
  var subject = document.querySelector('#compose-subject').value;
  if (subject === '') {
    subject = 'No Subject';
  }

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: subject,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    // If the message has not been sent properly, give the user
    // the ability to revisit the E-Mail and fix the mistake
    if (typeof(result.error) !== "undefined") {
      element= document.querySelector('.message');
      // display the message as an alert via bootstrap api
      element.className = 'alert alert-danger message';
      element.innerHTML = result.error;
    } else {
      load_mailbox('sent');
    }
  })
}

function load_email(contents) {
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#read-email').innerHTML = ``;

  fetch('/emails/' + contents.id)
  .then(response => response.json())
  .then(email => {
    read_email(email);
  })

  // set email as read
  if (!contents.read) {
    fetch('/emails/' + contents.id, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  }

}

function add_email(contents) {
  const email = document.createElement('a');
  email.className = 'email-preview';

  email.innerHTML = `
  <div class="info">
    <div class="participants">
      <div class="from"><b>From:</b> ${contents.sender}</div>
      <div class="to"><b>To:</b> ${contents.recipients}</div>
    </div>
    <div class="timestamp"><b>Date:</b> ${contents.timestamp}</div>
  </div>
  <div class="subject">${contents.subject}</div>`;


  if (contents.read === true) {
    email.style.backgroundColor = "lightgrey";
  }

  /* Pass the content to be fetched in the next function */
  email.addEventListener('click', function() {
    load_email(contents);
  });

  // Add email to DOM
  document.querySelector('#emails-view').append(email);
}

function read_email(contents) {
  
  var button;
  if (contents.archived) {
    button = `<button class="btn btn-sm btn-outline-primary" id="archive">Unarchive</button>`
  } else {
    button = `<button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>`
  }

  const email = document.createElement('div');
  email.className = 'email-content';

  email.innerHTML = `
  <div class="from"><b>From:</b> ${contents.sender}</div>
  <div class="to"><b>To:</b> ${contents.recipients}</div>
  <div class="subject"><b> Subject:</b>${contents.subject}</div>
  <div class="timestamp"><b>Timestamp:</b> ${contents.timestamp}</div>
  <div id="email-options">
    <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
    ${button}
  </div>
  <hr>
  <div class="body">${contents.body}</div>`;
  
  // debugging help
  console.log(contents);
  
  document.querySelector('#read-email').append(email);

  document.querySelector('#archive').addEventListener('click', () => {
    fetch('/emails/' + contents.id, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !contents.archived
      })
    })
    .then( () => load_mailbox('inbox'))
  });

  document.querySelector('#reply').addEventListener('click', () => {
    const recipient = contents.sender;
    var subject = contents.subject;
    const email_body = 
      `\n\n"On ${contents.timestamp} ${contents.sender} wrote:\n`+
      `${contents.body}"`;

    // Checking if the incoming email was already a response, adding 'Re: ' if it wasn't
    if (subject.slice(0,4) !== 'Re: ') {
      subject = 'Re: ' + subject;
    }

    compose_email(recipients = recipient, subject = subject, body = email_body);
  });
}