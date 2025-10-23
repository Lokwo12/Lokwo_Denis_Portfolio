// Homepage animations: testimonials, blog, projects
(function(){
  // Simple fade-up animation for testimonials
  function animateTestimonials() {
    document.querySelectorAll('.testimonial-card').forEach(function(card, i) {
      card.style.opacity = 0;
      card.style.transform = 'translateY(30px)';
      setTimeout(function() {
        card.style.transition = 'opacity 0.6s, transform 0.6s';
        card.style.opacity = 1;
        card.style.transform = 'translateY(0)';
      }, 200 + i * 200);
    });
  }

  // Animate on scroll utility
  function animateOnScroll(selector, animation) {
    const elements = document.querySelectorAll(selector);
    function check() {
      elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 60) {
          el.classList.add(animation);
        }
      });
    }
    window.addEventListener('scroll', check, { passive: true });
    check();
  }

  // Random animation effects for cards
  const blogEffects = ['fade-in', 'slide-up', 'zoom-in'];
  const projectEffects = ['slide-up', 'fade-in', 'flip-in'];
  const testimonialEffects = ['fade-up', 'zoom-in', 'rotate-in'];
  function randomEffect(effects) { return effects[Math.floor(Math.random() * effects.length)]; }
  function animateRandomOnScroll(selector, effects) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el) => {
      const effect = randomEffect(effects);
      el.classList.add('pre-anim');
      el.setAttribute('data-effect', effect);
    });
    function check() {
      elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 60) {
          el.classList.add(el.getAttribute('data-effect'));
        }
      });
    }
    window.addEventListener('scroll', check, { passive: true });
    check();
  }

  // Init on DOM ready
  window.addEventListener('DOMContentLoaded', function(){
    animateTestimonials();
    animateOnScroll('.blog-card', 'fade-in');
    animateOnScroll('.project-card', 'slide-up');
    animateOnScroll('.testimonial-card', 'fade-up');

    animateRandomOnScroll('.blog-card', blogEffects);
    animateRandomOnScroll('.project-card', projectEffects);
    animateRandomOnScroll('.testimonial-card', testimonialEffects);
  });
})();
