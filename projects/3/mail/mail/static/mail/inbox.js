/*
To do:
ReCreate different views for inbox and outbox (doing that in the add email function by getting different parameters additionally)
[] Loading E-Mails after sending will miss the just sent e-mail
[] init emails with unread
[] after sending: when object is message, do one, else redo email
[] don't show archive and unarchive buttons to the sender of the email

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
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    return false;
  };

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
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
  })
  .then(() => load_mailbox('sent'));
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
    fetch('/emails/' + email_id, {
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
  <div class="subject">${contents.subject}</div>
  <div class="body">${contents.body.slice(0, 30)}</div>`;


  if (contents.read === true) {
    email.style.backgroundColor = "lightgrey";
  }

  /* Pass the id to be fetched in the next function */
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

  document.querySelector('#reply').addEventListener('click', compose_email);
}