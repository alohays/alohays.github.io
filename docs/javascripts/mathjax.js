window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  startup: {
    // Render each page once, including pages loaded by instant navigation.
    // A second pass over assistive MathML would nest another rendered formula.
    typeset: false,
    ready: () => {
      MathJax.startup.defaultReady();
      let pending = MathJax.startup.promise;
      document$.subscribe(() => {
        pending = pending.then(() => {
          const formulas = [...document.querySelectorAll(".arithmatex")]
            .filter(element => !element.querySelector("mjx-container"));
          if (!formulas.length) return;
          MathJax.typesetClear();
          MathJax.texReset();
          return MathJax.typesetPromise(formulas);
        }).catch(error => console.error("Math rendering failed", error));
      });
    }
  }
};
