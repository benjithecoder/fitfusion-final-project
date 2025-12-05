// ---------TESTIMONIALS INFINITE MARQUEE---------

document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector(".testimonials-track");
    if (!track) return;

    const cards = Array.from(track.children);

    //Duplicate all cards once to make a seamless loop
    cards.forEach(card => {
        const clone = card.cloneNode(true);
        clone.classList.add("testimonial-clone");
        track.appendChild(clone);
    });
});