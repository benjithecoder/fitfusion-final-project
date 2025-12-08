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


// ---------------------------------MOBILE HAMBURGER BUTTON -------------------


//Run this after the DOM is loaded (so elements exist)
document.addEventListener("DOMContentLoaded", () => {
  // Grab the navbar and toggle button
  const navbar = document.querySelector(".navbar");
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelectorAll(".nav-links a");

  // Safety check: only run if elements exist
  if (!navbar || !navToggle) return;

  // When you click the hamburger / X button
  navToggle.addEventListener("click", () => {
    const isOpen = navbar.classList.toggle("navbar-open");

    // Update aria-expanded (for screen readers)
    navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  // Optional: close the menu when you click a link (on mobile)
  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      if (navbar.classList.contains("navbar-open")) {
        navbar.classList.remove("navbar-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  });
});




// -------------------------EXERCISE DETAIL TABS ABOUT/GUIDE-------------------------

const exerciseTabs = document.querySelectorAll(".exercise-tab");
const exercisePanels = document.querySelectorAll("[data-tab-panel]");

if (exerciseTabs && exercisePanels.length) {
    exerciseTabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const target = tab.dataset.tab;

            // update tab active state
            exerciseTabs.forEach((t) => t.classList.remove("is-active"));
            tab.classList.add("is-active");

            // show matching panel, hide other
            exercisePanels.forEach((panel) => {
                if (panel.dataset.tabPanel === target) {
                    panel.hidden = false;
                    panel.classList.add("is-active");
                } else {
                    panel.hidden = true;
                    panel.classList.remove("is-active");
                }
            });
        });
    });
}

