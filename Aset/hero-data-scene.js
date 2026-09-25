(() => {
  'use strict';
  const plot = document.querySelector('.regression-plot');
  if (!plot) return;
  const dots = Array.from(plot.querySelectorAll('.regression-dot'));
  const focus = plot.querySelector('.regression-spotlight');
  const marker = plot.querySelector('.regression-fit-focus');
  const focusWindow = plot.querySelector('.regression-spot-window');
  const model = JSON.parse(plot.querySelector('.regression-line').getAttribute('data-model'));
  const minX = 40, maxX = 740;
  const modelRange = 910; // Retain the original fitted model when shortening its visible domain.
  let selectedX = 495, selectedDot = null;
  function show(value) {
    selectedX = Math.max(minX, Math.min(maxX, value));
    marker.setAttribute('cx', selectedX);
    const t = (selectedX - minX) / modelRange;
    marker.setAttribute('cy', model[0] + model[1] * t + model[2] * t * t);
    focusWindow.setAttribute('x', selectedX - 45);
    focus.classList.add('is-active');
    const nearest = dots.reduce((best, dot) => Math.abs(Number(dot.getAttribute('cx')) - selectedX) < Math.abs(Number(best.getAttribute('cx')) - selectedX) ? dot : best);
    if (nearest !== selectedDot) { selectedDot?.classList.remove('is-active'); nearest.classList.add('is-active'); selectedDot = nearest; }
  }
  function hide() { focus.classList.remove('is-active'); selectedDot?.classList.remove('is-active'); selectedDot = null; }
  function resize() {
    const width = plot.clientWidth, height = plot.clientHeight;
    if (!width || !height) return;
    plot.setAttribute('viewBox', globalThis.matchMedia('(max-width: 1100px)').matches ? '0 150 790 200' : '0 60 790 290');
    const radius = width < 450 ? 3 : 3.7;
    const units = plot.viewBox.baseVal;
    dots.forEach(dot => { dot.setAttribute('rx', radius * units.width / width); dot.setAttribute('ry', radius * units.height / height); });
    marker.setAttribute('rx', 5 * units.width / width); marker.setAttribute('ry', 5 * units.height / height);
  }
  plot.setAttribute('tabindex', '0');
  plot.setAttribute('aria-label', 'Grafik ilustratif hubungan nonlinier dan confidence interval 95 persen. Arahkan kursor atau gunakan panah kiri dan kanan untuk menyorot kurva regresi.');
  plot.addEventListener('pointermove', event => {
    const rect = plot.getBoundingClientRect();
    if (rect.width) show(plot.viewBox.baseVal.x + (event.clientX - rect.left) / rect.width * plot.viewBox.baseVal.width);
  }, { passive: true });
  plot.addEventListener('pointerleave', hide);
  plot.addEventListener('focus', () => show(selectedX));
  plot.addEventListener('blur', hide);
  plot.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End', 'Escape'].includes(event.key)) return;
    event.preventDefault();
    if (event.key === 'Escape') { hide(); return; }
    show(event.key === 'Home' ? minX : event.key === 'End' ? maxX : selectedX + (event.key === 'ArrowRight' ? 35 : -35));
  });
  if ('ResizeObserver' in globalThis) new ResizeObserver(resize).observe(plot);
  else globalThis.addEventListener('resize', resize);
  resize();
})();
