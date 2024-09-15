let profile_image = document.getElementById('profile-photo-large')
let file_input = document.getElementById('new-profile-pic')

console.log(profile_image)
console.log(file_input)

file_input.addEventListener('change', function(){
    profile_image.src = URL.createObjectURL(file_input.files[0]);
    console.log(profile_image.src)
});