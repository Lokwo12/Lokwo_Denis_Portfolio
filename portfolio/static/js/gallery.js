document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.gallery-item');
  items.forEach(item => {
    const caption = item.querySelector('[data-caption]');
    const btn = item.querySelector('[data-toggle]');
    if (!caption || !btn) return;
    // Apply collapsible and check overflow
    caption.classList.add('collapsible');
    // Give the browser a moment to compute layout
    requestAnimationFrame(() => {
      const hasOverflow = caption.scrollHeight > caption.clientHeight + 2; // allow small rounding
      if (hasOverflow) {
        btn.hidden = false;
        btn.addEventListener('click', () => {
          const expanded = caption.classList.toggle('expanded');
          if (expanded) {
            btn.textContent = 'Show less';
          } else {
            btn.textContent = 'Show more';
          }
        });
      } else {
        // No overflow, remove collapsible cap to avoid unnecessary clipping
        caption.classList.remove('collapsible');
      }
    });
  });
});