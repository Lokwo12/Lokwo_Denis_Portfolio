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


	// Multi-theme + brand toggle (cycles through combinations)
	(function(){
		const btn = document.getElementById('theme-toggle');
		const root = document.documentElement;

		const brands = ['indigo','teal','green'];
		const themes = ['dark','light'];
		// Build ordered cycle of combinations
		const cycle = [
			{theme:'dark', brand:'indigo'},
			{theme:'dark', brand:'teal'},
			{theme:'dark', brand:'green'},
			{theme:'light', brand:'indigo'},
			{theme:'light', brand:'teal'},
			{theme:'light', brand:'green'},
		];

		function apply(theme, brand){
			// theme: 'light' or 'dark'
			if(theme === 'light'){
				root.setAttribute('data-theme','light');
				btn && btn.setAttribute('aria-pressed','false');
			}else{
				root.removeAttribute('data-theme'); // default dark
				btn && btn.setAttribute('aria-pressed','true');
			}
			// brand: 'indigo' uses default (remove attr), otherwise set
			if(brand && brand !== 'indigo'){
				root.setAttribute('data-brand', brand);
			}else{
				root.removeAttribute('data-brand');
			}
			// update button title for clarity
			if(btn){
				btn.title = `Theme: ${theme} · Brand: ${brand || 'indigo'}`;
			}
			localStorage.setItem('theme', theme);
			localStorage.setItem('brand', brand || 'indigo');
		}

		function loadInitial(){
			const storedTheme = localStorage.getItem('theme');
			const storedBrand = localStorage.getItem('brand');
			if(storedTheme){
				apply(storedTheme, storedBrand || 'indigo');
			}else{
				const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
				apply(prefersDark ? 'dark' : 'light', storedBrand || 'indigo');
			}
		}

		function currentIndex(){
			const t = localStorage.getItem('theme') || (root.getAttribute('data-theme') === 'light' ? 'light' : 'dark');
			const b = localStorage.getItem('brand') || (root.getAttribute('data-brand') || 'indigo');
			return Math.max(0, cycle.findIndex(x => x.theme===t && x.brand===(b || 'indigo')));
		}

		loadInitial();
		if(btn){
			btn.addEventListener('click', () => {
				const idx = currentIndex();
				const next = cycle[(idx + 1) % cycle.length];
				apply(next.theme, next.brand);
			});
		}
	})();
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
