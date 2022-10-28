
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})


// password generation button
var generatePassword = document.getElementById("generatePassword");


// generatedPassword value
const generatedPassword = document.getElementById('generatedPassword')

var pwCopier = document.getElementById('copy-generated-password')

// console.log('pwCopier: ', pwCopier)

pwCopier.addEventListener("click", ()=>{
  console.log('pwCopier clicked: ', generatedPassword.value);
  // pwCopier.setAttribute('data-bs-original-title', 'Passowrd copied!').tooltip('show');

  // Select the text field
  generatedPassword.select();
  generatedPassword.setSelectionRange(0,9999); // For mobile devices

  // copies the text from generatedPassword
  navigator.clipboard.writeText(generatedPassword.value);
});



// passwordLengthRangeNoticer
var passwordLengthRangeValue = document.getElementById("passwordLengthRange")
var passwordLengthDisplayValue = document.getElementById("passwordLengthDisplay")
passwordLengthDisplayValue.innerText = passwordLengthRangeValue.value

function passwordLengthRangeNoticer() {
  // console.log('passwordLengthRangeValue: ', passwordLengthRangeValue.value)
  // console.log('passwordLengthDisplay: ', passwordLengthDisplayValue.innerText)
  passwordLengthDisplayValue.innerText = passwordLengthRangeValue.value
}

sessionStorage.setItem("testing_DTH", "Smith");
var s=sessionStorage.getItem("testing_DTH");
console.log('s:::', s);