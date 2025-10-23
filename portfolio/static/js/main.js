// Simple typing animation + nav toggle
document.addEventListener('DOMContentLoaded', function(){
	// typing animation for element with data-roles
	const el = document.querySelector('[data-roles]');
	if(el){
		const roles = el.getAttribute('data-roles').split('|');
		let r=0, idx=0, forward=true;
		const speed = 80;
		function tick(){
			const full = roles[r];
			if(forward){
				idx++;
				if(idx>=full.length){forward=false;setTimeout(tick,800);return}
			} else {
				idx--;
				if(idx<=0){forward=true;r=(r+1)%roles.length;setTimeout(tick,350);return}
			}
			el.textContent = full.slice(0, idx);
			setTimeout(tick, speed);
		}
		tick();
	}

		// mobile nav - toggle class for better control and accessibility
		const toggle = document.querySelector('.nav-toggle');
		const nav = document.querySelector('.site-nav');
		if(toggle && nav){
			toggle.addEventListener('click', ()=>{
				const open = toggle.getAttribute('aria-expanded') === 'true';
				toggle.setAttribute('aria-expanded', String(!open));
				nav.classList.toggle('open');
				if(!open){
					// focus first link when opened
					const first = nav.querySelector('a');
					if(first) first.focus();
				}
			});
		}

			// show simple loading state on contact form submit
			const contactForm = document.querySelector('form[aria-label="Contact form"]');
			if(contactForm){
				contactForm.addEventListener('submit', ()=>{
					const submit = contactForm.querySelector('button[type="submit"]');
					if(submit){
						submit.disabled = true;
						submit.textContent = 'Sending...';
					}
				});
			}
});
