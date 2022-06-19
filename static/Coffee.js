var btnPress = document.getElementById('yesBtn');
var i =0;
var speed = 50;

const activePge = window.location.href;
console.log(activePge)
const navList = document.querySelectorAll('nav a').forEach(link => {
    if(link.href == activePge){
        console.log(link.href)
        link.classList.add('active');
    }
});
document.getElementById('myForm').addEventListener('submit',function(){alert("My Website is Thanking you!")},false) ; 
function changeText(){
    console.log('hello')
    if(document.getElementById('yesBtn').innerHTML.includes('Press Me!!')){
        document.getElementById('yesBtn').innerHTML = 'Go To Contact Us Page';
    }
    else{
        document.getElementById('yesBtn').innerHTML = 'Press Me!!'
    }
}

