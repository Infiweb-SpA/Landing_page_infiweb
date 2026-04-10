// Mobile menu toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Navbar active link on scroll + highlight
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

function updateActiveLink() {
    let current = '';
    const scrollPos = window.scrollY + 150;
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href').substring(1);
        if (href === current) {
            link.classList.add('active');
        }
    });
}

window.addEventListener('scroll', updateActiveLink);
updateActiveLink();

// Back to top button
const backBtn = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backBtn.classList.add('show');
    } else {
        backBtn.classList.remove('show');
    }
});
backBtn?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Animated counters (Intersection Observer)
const counters = document.querySelectorAll('.stat-number');
const speed = 200;

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counter = entry.target;
            const updateCount = () => {
                const target = parseInt(counter.getAttribute('data-target'));
                const current = parseInt(counter.innerText);
                const increment = Math.ceil(target / 30);
                if (current < target) {
                    counter.innerText = Math.min(current + increment, target);
                    setTimeout(updateCount, 20);
                } else {
                    counter.innerText = target;
                }
            };
            updateCount();
            observer.unobserve(counter);
        }
    });
}, { threshold: 0.5 });

counters.forEach(counter => observer.observe(counter));

// Scroll Reveal Animation
const revealElements = document.querySelectorAll('.service-card, .project-card, .testimonial-card, .challenge-card, .about-content, .about-image');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

revealElements.forEach(el => {
    el.classList.add('reveal');
    revealObserver.observe(el);
});

// Contact Form AJAX
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

contactForm?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };

    formMessage.innerHTML = '<span style="color:#00cfff;">Enviando...</span>';

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000); // 10s

    try {
        const response = await fetch('/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
            signal: controller.signal
        });

        clearTimeout(timeout);

        const result = await response.json();

        if (result.success) {
            formMessage.innerHTML = '<span style="color:#10b981;">✅ Mensaje enviado correctamente</span>';
            contactForm.reset();
        } else {
            formMessage.innerHTML = '<span style="color:#ef4444;">❌ Error al enviar</span>';
        }

    } catch (error) {
        if (error.name === 'AbortError') {
            formMessage.innerHTML = '<span style="color:#f59e0b;">⏱️ El servidor tardó demasiado</span>';
        } else {
            formMessage.innerHTML = '<span style="color:#ef4444;">❌ Error de conexión</span>';
        }

        console.error("Error:", error);
    }
});