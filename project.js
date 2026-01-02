const toggleMenuBtn = document.querySelector('.toggle-menu-btn');
const navLinks = document.querySelector('.nav-links');

toggleMenuBtn.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});
function FindDoctor() {
  window.location.href = ' finddoctor.html';
}



function Appointment() {
  window.location.href = "take_appointement.html";
}

const form = document.querySelector('.form-container form');
let formData = [];

form.addEventListener('submit', (e) => {
  e.preventDefault();


  const name = document.querySelector('#name').value;
  const email = document.querySelector('#email').value;
  const subject = document.querySelector('#subject').value;
  const message = document.querySelector('#message').value;


  const newData = { name, email, subject, message};


  formData.push(newData);
 console.log(formData);
 form.reset();
});