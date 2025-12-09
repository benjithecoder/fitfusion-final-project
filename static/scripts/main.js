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

/*  
===========================================================
TAB SYSTEM FOR ABOUT / GUIDE / LOG
-----------------------------------------------------------
This JavaScript controls which panel is visible.

Tabs:        <button class="exercise-tab" data-tab="about">
Panels:      <section data-tab-panel="about">

Goal:  
- Clicking a tab shows the matching panel.
- Other panels become hidden.
- When the page reloads (after POST), the tab from the URL hash
  (#about, #guide, #log) becomes active again.
===========================================================
*/


// STEP 1 — Select all tab buttons ("About", "Guide", "Log")
const exerciseTabs = document.querySelectorAll(".exercise-tab");

// STEP 2 — Select all panels that match those tabs
const exercisePanels = document.querySelectorAll("[data-tab-panel]");



/*
===========================================================
FUNCTION: showTab(target)
-----------------------------------------------------------
This function makes ONE tab active and shows the matching panel.
"target" is a string: "about", "guide", or "log".
===========================================================
*/
function showTab(target) {

    // Loop over ALL tab buttons
    exerciseTabs.forEach((t) => {

        // If this tab's data-tab matches the target → activate it
        if (t.dataset.tab === target) {
            t.classList.add("is-active");          // highlight tab
            t.setAttribute("aria-selected", "true"); // accessibility
        } 
        
        // Otherwise deactivate this tab
        else {
            t.classList.remove("is-active");
            t.setAttribute("aria-selected", "false");
        }
    });



    // Loop over all tab panels
    exercisePanels.forEach((panel) => {

        // If panel's data-tab-panel matches the target → show it
        if (panel.dataset.tabPanel === target) {
            panel.hidden = false;                  // make visible
            panel.classList.add("is-active");      // optional styling hook
        } 
        
        // Otherwise hide the panel
        else {
            panel.hidden = true;
            panel.classList.remove("is-active");
        }
    });
}



/*
===========================================================
EVENT LISTENERS — Handle clicks on tabs
-----------------------------------------------------------
When a user clicks a tab:
- Save the tab name in the URL as #about / #guide / #log
- Call showTab() to update the UI
===========================================================
*/
if (exerciseTabs.length && exercisePanels.length) {

    exerciseTabs.forEach((tab) => {

        tab.addEventListener("click", () => {
            // Get which tab was clicked (about/guide/log)
            const target = tab.dataset.tab;

            // Save the tab name in the URL → #log
            // Very important: this allows reload to keep the same tab
            window.location.hash = target;

            // Show the correct panel
            showTab(target);
        });
    });



    /*
    ===========================================================
    PAGE LOAD BEHAVIOR
    -----------------------------------------------------------
    When the page loads (including after POST reload):
    - Read the URL hash (#log)
    - If there is a hash, activate that tab
    - Otherwise default to "about"
    ===========================================================
    */

    // Remove the "#" → "log"
    const hash = window.location.hash.replace("#", "");

    if (hash) {
        // Example → #log → showTab("log")
        showTab(hash);
    } 
    else {
        // No hash? First visit → show About panel
        showTab("about");
    }
}


