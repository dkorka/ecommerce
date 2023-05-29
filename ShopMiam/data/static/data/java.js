let zoom = document.querySelectorAll('.annonce');

zoom.forEach(element => {
    element.addEventListener('mouseover',()=>{element.style.backgroundColor = '#EEF7F2'});
    });

zoom.forEach(element => {
    element.addEventListener('mouseout',()=>{element.style.backgroundColor = 'white'});
    });


let form = document.querySelector('form.modif_panier')
form.addEventListener('change', ()=>{form.submit()});