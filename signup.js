const form = document.querySelector('.signup-form');
const inputs = form.querySelectorAll('input');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  let formData = {};

  inputs.forEach((input) => {
    if (input.value !== '') {
      formData[input.name] = input.value;
    }
  });

  console.log('Form Data:', formData);

 
});

const form1 = document.querySelector('.login-form');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const username = form1.querySelector('input[name="username"]').value;
  const password = form1.querySelector('input[name="password"]').value;

  console.log(`Username: ${username}`);
  console.log(`Password: ${password}`);

});