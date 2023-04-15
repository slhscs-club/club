 /* 
    Copyright (c) 2023 by Louis Hoebregts (https://codepen.io/Mamboleoo/pen/obWGYr)

    Permission is hereby granted, free of charge, to any person obtaining a copy of 
    this software and associated documentation files (the "Software"), to deal in the Software 
    without restriction, including without limitation the rights to use, copy, modify, merge, 
    publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons 
    to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or 
    substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
    OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 

let canvas;
let ctx;
let particles = [];
let amount = 0;
let mouse = {x:0,y:0};
let radius = 3;
let timeouts = [];
const colors = ["#FFFFFF", "#AAAAAA"];
let ww;
let wh;

addEventListener("DOMContentLoaded", () => {
    canvas = document.querySelector("#particle-canvas");
    ctx = canvas.getContext("2d");
    ww = canvas.width = window.innerWidth;
    wh = canvas.height = window.innerHeight;

    window.addEventListener("resize", initSceneWait);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("touchmove", onTouchMove);
    window.addEventListener("click", onMouseClick);
    window.addEventListener("touchend", onTouchEnd);
    initScene();
    requestAnimationFrame(render);
});

function Particle(x,y) {
    this.x =  Math.random() * ww;
    this.y =  Math.random() * wh;
    this.dest = {
        x : x,
        y: y
    };
    this.r =  Math.random() * 5 + 2;
    this.vx = (Math.random() - 0.5) * 20;
    this.vy = (Math.random() - 0.5) * 20;
    this.accX = 0;
    this.accY = 0;
    this.friction = Math.random() * 0.01 + 0.94;

    this.color = colors[Math.floor(Math.random() * 6)];
}

Particle.prototype.render = function() {
    this.accX = (this.dest.x - this.x) / 100;
    this.accY = (this.dest.y - this.y) / 100;
    this.vx += this.accX;
    this.vy += this.accY;
    this.vx *= this.friction;
    this.vy *= this.friction;

    this.x += this.vx;
    this.y += this.vy;

    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.r, this.r);

    let a = this.x - mouse.x;
    let b = this.y - mouse.y;

    let distance = Math.sqrt(a * a + b * b);

    if(distance < radius * 70) {
        this.accX = (this.x - mouse.x) / 100;
        this.accY = (this.y - mouse.y) / 100;
        this.vx += this.accX;
        this.vy += this.accY;
    }
}

function onMouseMove(e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
}

function onTouchMove(e) {
    if(e.touches.length > 0 ){
        mouse.x = e.touches[0].clientX;
        mouse.y = e.touches[0].clientY;
    }
}

function onTouchEnd(e) {
    mouse.x = -9999;
    mouse.y = -9999;
}

function initScene() {
    ww = canvas.width = window.innerWidth;
    wh = canvas.height = window.innerHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = 'images/logo.png';
    img.onload = function (e)
    {
        ctx.drawImage(img, ww / 2 - 256, wh / 2 - 256, 512, 512);
        
        let data  = ctx.getImageData(0, 0, ww, wh).data;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.globalCompositeOperation = "screen";

        particles = [];

        for(let i = 0; i < ww; i += 12){
            for(let j = 0; j < wh; j += 12){
                if(data[ ((i + j * ww) * 4) + 3] > 150){
                    particles.push(new Particle(i,j));
                }
            }
        }

        amount = particles.length;
    }
}

function onMouseClick() {
    radius++;

    if(radius == 5){
        radius = 2;
    }
}

function render(a) {
    requestAnimationFrame(render);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < amount; i++) {
        particles[i].render();
    }
}

function initSceneWait() {
    while (timeouts.length > 0) {
        clearTimeout(timeouts.pop());
    }

    const timeout = setTimeout(initScene, 1500);
    timeouts.push(timeout); 
}
