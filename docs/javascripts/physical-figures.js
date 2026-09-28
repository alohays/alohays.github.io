/* Progressive enhancement: figures remain readable without this viewer. */
(() => {
  function enhanceFigures() {
    if (!document.querySelector('.pu-figure')) return;
    const korean = document.documentElement.lang === 'ko';
    document.querySelectorAll('article figure').forEach((figure, index) => {
      if (figure.querySelector('.pu-toolbar')) return;
      const visual = figure.querySelector('.pu-figure') || figure.querySelector('img');
      if (!visual) return;
      const toolbar = document.createElement('div');
      toolbar.className = 'pu-toolbar';
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'pu-expand';
      button.textContent = korean ? '크게 보기' : 'Expand figure';
      button.setAttribute('aria-label', korean ? `그림 ${index + 1} 크게 보기` : `Expand figure ${index + 1}`);
      button.addEventListener('click', () => {
        const dialog = document.createElement('dialog');
        dialog.className = 'pu-dialog';
        dialog.setAttribute('aria-label', korean ? `그림 ${index + 1} 확대` : `Figure ${index + 1}, expanded`);
        const head = document.createElement('div');
        head.className = 'pu-dialog-head';
        const label = document.createElement('span');
        label.textContent = korean ? `그림 ${index + 1}` : `Figure ${index + 1}`;
        const close = document.createElement('button');
        close.type = 'button'; close.className = 'pu-close';
        close.textContent = korean ? '닫기' : 'Close';
        close.addEventListener('click', () => dialog.close());
        head.append(label, close);
        const content = document.createElement('div');
        content.className = 'pu-dialog-body';
        const clone = visual.cloneNode(true);
        // SVG clipping and markers need unique IDs in the expanded copy too.
        let markup = clone.outerHTML;
        const ids = [...clone.querySelectorAll('[id]')].map(n => n.id);
        for (const id of ids.sort((a,b) => b.length-a.length)) {
          markup = markup.replaceAll(`id="${id}"`, `id="expanded-${id}"`)
            .replaceAll(`#${id})`, `#expanded-${id})`)
            .replaceAll(`#${id}"`, `#expanded-${id}"`);
        }
        content.innerHTML = markup;
        dialog.append(head, content);
        document.body.append(dialog);
        dialog.addEventListener('close', () => {
          document.body.classList.remove('pu-modal-open');
          dialog.remove(); button.focus({preventScroll:true});
        }, {once:true});
        dialog.addEventListener('click', e => {
          if (e.target !== dialog) return;
          const r = dialog.getBoundingClientRect();
          if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
        });
        dialog.showModal();
        document.body.classList.add('pu-modal-open');
        close.focus();
      });
      toolbar.append(button);
      const caption = figure.querySelector('figcaption');
      if (caption) figure.insertBefore(toolbar, caption); else figure.append(toolbar);
    });
  }
  if (typeof document$ !== 'undefined') document$.subscribe(enhanceFigures);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhanceFigures);
  else enhanceFigures();
})();
