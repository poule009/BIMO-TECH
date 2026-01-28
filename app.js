const sections = document.querySelectorAll('section');
const header = document.querySelector('header');
const btnBurger = document.querySelector('#burger-menu');
const nav = document.querySelector('.navigation');
const linkNav = document.querySelectorAll('.navigation a');

// Initialize ScrollReveal
const sr = ScrollReveal({
    origin: 'bottom',
    distance: '60px',
    duration: 1000,
    delay: 200,
    reset: true
});

// Apply ScrollReveal to sections
sr.reveal('.home-content', { origin: 'top' });
sr.reveal('.about-img', { origin: 'left' });
sr.reveal('.about-content', { origin: 'right' });
sr.reveal('.services .box', { interval: 200 });
sr.reveal('.locations .heading', { origin: 'top' });
sr.reveal('.location-box', { interval: 200 });
sr.reveal('.newsletter', { origin: 'bottom' });
sr.reveal('footer', { origin: 'bottom' });

btnBurger.addEventListener('click', ()=> {
  nav.classList.toggle('active')
  btnBurger.classList.toggle('bx-x')
  if(window.scrollY == 0){
    header.classList.toggle('active')
 }
});

linkNav.forEach(link => {
    link.addEventListener('click', ()=> {
        nav.classList.remove('active')
       btnBurger.classList.remove('bx-x')
    });
})

// Optimization: Use requestAnimationFrame for scroll events to improve fluidity
let isScrolling = false;

window.addEventListener('scroll', () => {
    if (!isScrolling) {
        window.requestAnimationFrame(() => {
            // Toggle header active state
            header.classList.toggle('active', window.scrollY > 0);
            
            // Close mobile menu on scroll
            nav.classList.remove('active');
            btnBurger.classList.remove('bx-x');

            isScrolling = false;
        });
        isScrolling = true;
    }
}, { passive: true }); // Passive listener improves scroll performance

// Optimization: Use IntersectionObserver instead of scroll event for Active Link Highlighting
const observerOptions = {
    threshold: 0.5, // Trigger when 50% of the section is visible
    rootMargin: "-50px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            linkNav.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href').includes(id)) link.classList.add('active');
            });
        }
    });
}, observerOptions);

sections.forEach(section => observer.observe(section));
