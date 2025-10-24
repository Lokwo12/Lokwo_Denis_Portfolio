document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.gallery-item');
  items.forEach(item => {
    const caption = item.querySelector('[data-caption]');
    const btn = item.querySelector('[data-toggle]');
    if (!caption || !btn) return;
    caption.classList.add('collapsible');
    requestAnimationFrame(() => {
      const hasOverflow = caption.scrollHeight > caption.clientHeight + 2;
      if (hasOverflow) {
        btn.hidden = false;
        btn.addEventListener('click', () => {
          const expanded = caption.classList.toggle('expanded');
          btn.textContent = expanded ? 'Show less' : 'Show more';
        });
      } else {
        caption.classList.remove('collapsible');
      }
    });
  });
});