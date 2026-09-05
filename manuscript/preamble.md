```latex
% ── Page Geometry (tight margins for dense scholarly layout) ──────
\usepackage[margin=1cm, top=1.2cm, bottom=1.2cm, heightrounded]{geometry}

% ── Color Support ─────────────────────────────────────────────────
\usepackage{xcolor}
\definecolor{lean4blue}{RGB}{0,70,150}
\definecolor{mathlibgreen}{RGB}{0,120,60}
\definecolor{fepred}{RGB}{180,30,30}

% ── Mathematics ───────────────────────────────────────────────────
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{amsthm}
\usepackage{bm}

% ── Code Listings ────────────────────────────────────────────────
\usepackage{listings}
\usepackage{fvextra}
\RecustomVerbatimEnvironment{Highlighting}{Verbatim}{
  commandchars=\\\{\},
  breaklines=true,
  breakanywhere=true
}
\lstset{
  basicstyle=\ttfamily\footnotesize,
  breaklines=true,
  frame=single,
  captionpos=b,
  numbers=left,
  numberstyle=\tiny,
  keywordstyle=\color{lean4blue}\bfseries,
  commentstyle=\color{gray}\itshape,
  stringstyle=\color{fepred}
}
\lstdefinelanguage{lean4}{
  keywords={theorem,lemma,def,structure,class,instance,variable,import,open,namespace,end,by,exact,rw,apply,simp,linarith,nlinarith,positivity,ring,norm_num,have,show,calc,match,fun,let,where},
  comment=[l]{--},
  morecomment=[s]{/-}{-/},
  string=[b]"
}

% ── Tables & Layout ──────────────────────────────────────────────
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{multirow}

% ── Line-breaking tolerances ─────────────────────────────────────
% Lean identifiers (e.g. ``MeasurableSpace.borel_eq_generateFrom_Ico``) and
% inline code spans frequently break the right margin. Pandoc already
% sets ``\emergencystretch=3em`` and loads ``microtype``; bumping these
% three knobs cuts the overfull-hbox count by roughly a third without
% noticeably increasing interword spacing in normal prose.
\setlength{\emergencystretch}{4em}
\hbadness=2000
\tolerance=4000

% ── Cross-referencing (red hyperlinks: internal, URL, citations) ──
% hyperref is loaded by Pandoc's default template (via bookmark), so
% re-loading it here triggers an option clash. Instead, queue our color
% scheme before the template loads it, and reapply via \hypersetup once
% the document begins (also covers any later override by the template).
\PassOptionsToPackage{colorlinks=true,linkcolor=fepred,urlcolor=fepred,citecolor=fepred,anchorcolor=fepred}{hyperref}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=fepred,urlcolor=fepred,citecolor=fepred,anchorcolor=fepred}}
% Pandoc loads bookmark (and therefore hyperref) after header includes. Queue
% cleveref after bookmark so cross-references are defined in the preamble and
% retain the package ordering required by cleveref.
\AddToHook{package/bookmark/after}{\RequirePackage{cleveref}}

% ── Styled theorem/code panels ───────────────────────────────────
% tcolorbox intentionally NOT loaded: the only style it defined (lean4box)
% is referenced by no manuscript section, and tcolorbox is absent from a
% TeX Live basic install, which aborted every PDF render. Re-add the
% package here together with its first real use, not before.

% ── Theorem environments ─────────────────────────────────────────
\theoremstyle{definition}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{definition}[theorem]{Definition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{example}[theorem]{Example}

% ── FEP-specific operators ────────────────────────────────────────
\DeclareMathOperator{\KL}{KL}
% G(π) notation for Expected Free Energy, following Parr & Friston (2022)
\DeclareMathOperator{\EFE}{G}
\DeclareMathOperator{\FE}{F}
\DeclareMathOperator{\Ent}{H}
\DeclareMathOperator{\ELBO}{ELBO}
\DeclareMathOperator{\softmax}{softmax}
\newcommand{\E}{\mathbb{E}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\Prob}{\mathbb{P}}
% Variational free energy with tilde for expected
\newcommand{\VFE}{\widetilde{F}}
% Generative model notation
\newcommand{\gen}[1]{p(#1)}
\newcommand{\rec}[1]{q(#1)}

% Unicode-capable mono font for Lean code listings. Pandoc's Highlighting
% (fancyvrb) environment defaults to \ttfamily = lmtt, which lacks the Greek
% and mathematical glyphs used in the catalogue. FreeSerif covers the complete
% audited prose glyph set; FreeMono preserves fixed-width code. XeTeX character
% transitions supply the four mathematical-script carrier names that FreeMono
% does not contain, without changing the spacing of the surrounding code.
\usepackage{fontspec}
\setmainfont{FreeSerif}
\setmonofont{FreeMono}[Scale=MatchLowercase]
\usepackage{ucharclasses}
\newfontfamily\leanunicodefont{FreeSerif}
\setTransitionsFor{MathematicalAlphanumericSymbols}{\leanunicodefont}{}

% Math font for unicode-math: Latin Modern Math has full BMP coverage
% including U+2223 (\mid), U+226A/226B (\ll/\gg), and the Greek/blackboard
% letters used throughout the FEP derivations. Without an explicit
% \setmathfont, unicode-math's fallback chain ends in lmroman text font
% (which lacks U+2223) and warns on every \mid in math mode.
\setmathfont{latinmodern-math.otf}
```
