(() => {
  const section = document.querySelector('.client-logos');
  if (!section || !('IntersectionObserver' in window)) return;
  section.querySelectorAll('.client-logo-item').forEach((item, index) => {
    item.style.setProperty('--logo-order', index);
  });
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      section.classList.add('is-entering');
      observer.unobserve(section);
    }
  }, { threshold: 0.15 });
  observer.observe(section);
})();
