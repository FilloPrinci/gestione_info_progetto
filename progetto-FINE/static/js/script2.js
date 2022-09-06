var canvas = document.getElementById('canvas1');
canvas.width = document.body.clientWidth;
canvas.height = document.body.clientHeight;

function fullscreen() {
    if (!fullWindowState) {
        fullWindowState = true;
        //canvas goes full Window
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.className = "fullscreen"

        document.body.scrollTop = 0; // <-- pull the page back up to the top
        document.body.style.overflow = 'hidden'; // <-- relevant addition
    } else {
        fullWindowState = false;
        //canvas goes normal
        canvas.width = 820;
        canvas.height = 600;
        canvas.className = "";

        document.body.style.overflow = 'visible'; // <-- toggle back to normal mode
    }

}