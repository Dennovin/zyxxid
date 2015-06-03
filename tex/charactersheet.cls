\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{charactersheet} [2015/04/01 D&D 5e Newbie Character Sheet]

\LoadClass{article}

\usepackage{fontspec,tabularx,tabulary,fp,numprint,etoolbox,enumitem,cellspace,color,colortbl,titlesec}
\usepackage[margin=0.5in]{geometry}

\setmainfont{PT Sans}
\newfontfamily\titlett{Aniron}
\newfontfamily\sectiontt[UprightFont={* Bold}]{PT Sans}
\titleformat{\section}{\titlett}{}{}{}{}

\pagestyle{empty}
\tymin=1.5in

\addparagraphcolumntypes{X}
\cellspacetoplimit 3pt
\cellspacebottomlimit 3pt
\setlength{\parindent}{0pt}

\definecolor{gray}{rgb}{0.75,0.75,0.75}
\definecolor{yellow}{rgb}{1.00,1.00,0.75}
\definecolor{oddrow}{rgb}{0.90,0.90,1.00}
\definecolor{evenrow}{rgb}{0.80,0.80,0.90}

\newenvironment{charactersheet}
  {
    \def\profbonus{2}

    \def\attrstr{0}
    \def\attrdex{0}
    \def\attrcon{0}
    \def\attrint{0}
    \def\attrwis{0}
    \def\attrcha{0}

    \def\attrac{0}
    \def\attrhp{0}
    \def\attrhd{0}

    \def\profstrsave{0}
    \def\profdexsave{0}
    \def\profconsave{0}
    \def\profintsave{0}
    \def\profwissave{0}
    \def\profchasave{0}

    \def\profathletics{0}
    \def\profacrobatics{0}
    \def\profsleightofhand{0}
    \def\profstealth{0}
    \def\profarcana{0}
    \def\profhistory{0}
    \def\profnature{0}
    \def\profreligion{0}
    \def\profinvestigation{0}
    \def\profhandleanimal{0}
    \def\profinsight{0}
    \def\profmedicine{0}
    \def\profperception{0}
    \def\profsurvival{0}
    \def\profdeception{0}
    \def\profintimidate{0}
    \def\profperformance{0}
    \def\profpersuasion{0}

    \newcommand{\givencharactername}{John Doe}
    \newcommand{\characterinfo}{}
    \newcommand{\attacks}{\hline}
    \newcommand{\traits}{}
    \newcommand{\abilities}{}
    \newcommand{\skills}{}
    \newcommand{\spells}{}
    \newcommand{\charactername}[1]{\renewcommand{\givencharactername}{##1}}
    \newcommand{\addinfo}[2]{\expandafter\def\expandafter\characterinfo\expandafter{\characterinfo{} {\sectiontt ##1} & \small{##2} \\ \\}}
    \newcommand{\addattack}[4]{\expandafter\def\expandafter\attacks\expandafter{\attacks{} ##1 & \textbf{##2} & \textbf{##3} & ##4 \\ \hline}}
    \newcommand{\addtrait}[1]{\expandafter\def\expandafter\traits\expandafter{\traits{} & \small{\hspace{0.25em} \textbullet \hspace{0.25em} ##1} \\ }}
    \newcommand{\addability}[1]{\expandafter\def\expandafter\abilities\expandafter{\abilities{} \item ##1}}
    \newcommand{\addspell}[3]{\expandafter\def\expandafter\spells\expandafter{\spells{} \item \textbf{##1} (##2): ##3 }}
    \newcommand{\setattr}[2]{\@namedef{attr##1}{##2}}
    \newcommand{\setprof}[2]{\@namedef{prof##1}{##2}}
    \newcommand{\setprofbonus}[1]{\def\profbonus{##1}}

    \newcommand{\abilityscore}[1]{\FPeval{\result}{round(trunc(round(##1 / 2,1),0) - 5,0)} \textbf{\numprint{\result}}}
    \newcommand{\skillvalue}[2]{\FPeval{\result}{round(trunc(round(##1 / 2,1),0) - 5 + (##2 * \profbonus),0)} \textbf{\numprint{\result}}}
  }
  {
    {\large\titlett \givencharactername \par}
    \vspace{-0.5em}
    \rule{\textwidth}{0.4pt}
    \vspace{1em}
    \noindent\begin{tabulary}{\linewidth}{LJ}
      \characterinfo
      \ifdefempty{\traits}{}{\sectiontt Your Traits} \traits
    \end{tabulary}

    \rule{\textwidth}{0.4pt}
    \vspace{0.5em}

    \begin{minipage}[t]{0.30\textwidth}
      \section*{Attributes and Skills}
      \noindent\begin{tabularx}{\linewidth}{ |X|Sc| }
        \hline
        \rowcolor{yellow} Hit Points & \textbf{\numprint{\attrhp}} \\
        \hline
        \rowcolor{yellow} Armor Class & \textbf{\numprint{\attrac}} \\
        \hline
        \rowcolor{yellow} Hit Dice & \textbf{\attrhd} \\
        \hline
        \multicolumn{2}{c}{} \\
        \hline
        \rowcolor{oddrow} Strength & \abilityscore{\attrstr} \\
        \hline
        \rowcolor{evenrow} Dexterity & \abilityscore{\attrdex} \\
        \hline
        \rowcolor{oddrow} Constitution & \abilityscore{\attrcon} \\
        \hline
        \rowcolor{evenrow} Intelligence & \abilityscore{\attrint} \\
        \hline
        \rowcolor{oddrow} Wisdom & \abilityscore{\attrwis} \\
        \hline
        \rowcolor{evenrow} Charisma & \abilityscore{\attrcha} \\
        \hline
        \multicolumn{2}{c}{} \\
        \hline
        \rowcolor{oddrow} Acrobatics & \skillvalue{\attrdex}{\profacrobatics} \\
        \hline
        \rowcolor{evenrow} Arcana & \skillvalue{\attrint}{\profarcana} \\
        \hline
        \rowcolor{oddrow} Athletics & \skillvalue{\attrstr}{\profathletics} \\
        \hline
        \rowcolor{evenrow} Deception & \skillvalue{\attrcha}{\profdeception} \\
        \hline
        \rowcolor{oddrow} Handle Animal & \skillvalue{\attrwis}{\profhandleanimal} \\
        \hline
        \rowcolor{evenrow} History & \skillvalue{\attrint}{\profhistory} \\
        \hline
        \rowcolor{oddrow} Insight & \skillvalue{\attrwis}{\profinsight} \\
        \hline
        \rowcolor{evenrow} Intimidate & \skillvalue{\attrcha}{\profintimidate} \\
        \hline
        \rowcolor{oddrow} Investigation & \skillvalue{\attrint}{\profinvestigation} \\
        \hline
        \rowcolor{evenrow} Medicine & \skillvalue{\attrwis}{\profmedicine} \\
        \hline
        \rowcolor{oddrow} Nature & \skillvalue{\attrint}{\profnature} \\
        \hline
        \rowcolor{evenrow} Perception & \skillvalue{\attrwis}{\profperception} \\
        \hline
        \rowcolor{oddrow} Performance & \skillvalue{\attrcha}{\profperformance} \\
        \hline
        \rowcolor{evenrow} Persuasion & \skillvalue{\attrcha}{\profpersuasion} \\
        \hline
        \rowcolor{oddrow} Religion & \skillvalue{\attrint}{\profreligion} \\
        \hline
        \rowcolor{evenrow} Sleight of Hand & \skillvalue{\attrdex}{\profsleightofhand} \\
        \hline
        \rowcolor{oddrow} Stealth & \skillvalue{\attrdex}{\profstealth} \\
        \hline
        \rowcolor{evenrow} Survival & \skillvalue{\attrwis}{\profsurvival} \\
        \hline
      \end{tabularx}

    \end{minipage}
    \begin{minipage}[t]{0.05\textwidth}
      \hspace{0.05\textwidth}
    \end{minipage}
    \begin{minipage}[t]{0.65\textwidth}

      \section*{Attacks}
      \noindent\begin{tabularx}{\textwidth}{ |X|Sc|Sc|Sc| }
        \hline
        \rowcolor{gray} \textbf{Attack} & \textbf{Hit Bonus} & \textbf{Damage} & \textbf{Range} \\
        \attacks
      \end{tabularx}
      \vspace{1em}

      \ifdefempty{\abilities}{}{
        \section*{Abilities}
        \begin{itemize}[noitemsep]
          \small\abilities
        \end{itemize}
      }

      \ifdefempty{\spells}{}{
        \section*{Spells}
        \begin{itemize}[noitemsep]
          \small\spells
        \end{itemize}
      }

    \end{minipage}
  }
