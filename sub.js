const form = document.querySelector('.square-form');
const formData = [];

form.addEventListener('submit', (e) =>{
  e.preventDefault();

  const name = document.querySelector('input[type="text"]').value;
  const lastName = document.querySelector('input[type="text"]:nth-child(2)').value;
  const phone = document.querySelector('input[type="tel"]').value;
  const product = document.querySelector('#product').value;
  const paymentType = getPaymentType();
  const paymentCode = document.querySelector('#payment-code').value;
  const location = document.querySelector('#location').value;

  formData.push({
    name,
    lastName,
    phone,
    product,
    paymentType,
    paymentCode,
    location
  });

  localStorage.setItem('formData', JSON.stringify(formData));

  form.reset();
});

function getPaymentType() {
  if (document.querySelector('.colored-icon.larger-icon.active').classList.contains('fa-cc-visa')) {
    return 'Visa';
  } else if (document.querySelector('.colored-icon.larger-icon.active').classList.contains('fa-paypal')) {
    return 'PayPal';
  } else if (document.querySelector('.colored-icon.larger-icon.active').classList.contains('fa-cc-amazon-pay')) {
    return 'Amazon Pay';
  } else if (document.querySelector('.colored-icon.larger-icon.active').classList.contains('fa-cc-mastercard')) {
    return 'MasterCard';
  }
}



   
   const tableBody = document.querySelector('#submissionsTable tbody');


   const formdata = JSON.parse(localStorage.getItem('formdata')) || [];


   formData.forEach(data => {
       const row = document.createElement('tr');

       const nameCell = document.createElement('td');
       nameCell.textContent = data.name;
       row.appendChild(nameCell);

       const lastNameCell = document.createElement('td');
       lastNameCell.textContent = data.lastName;
       row.appendChild(lastNameCell);

       const phoneCell = document.createElement('td');
       phoneCell.textContent = data.phone;
       row.appendChild(phoneCell);

       const productCell = document.createElement('td');
       productCell.textContent = data.product;
       row.appendChild(productCell);

       const paymentTypeCell = document.createElement('td');
       paymentTypeCell.textContent = data.paymentType;
       row.appendChild(paymentTypeCell);

       const paymentCodeCell = document.createElement('td');
       paymentCodeCell.textContent = data.paymentCode;
       row.appendChild(paymentCodeCell);

       const locationCell = document.createElement('td');
       locationCell.textContent = data.location;
       row.appendChild(locationCell);

       tableBody.appendChild(row);
   })
   ;