const form = document.querySelector('.login-form');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const username = form.querySelector('input[name="username"]').value;
  const password = form.querySelector('input[name="password"]').value;

  console.log(`Username: ${username}`);
  console.log(`Password: ${password}`);

  // Send form data to server using AJAX or Fetch API
});