\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{charactersheet} [2015/06/01 D&D 5e Character Sheet]

\LoadClass{article}

\usepackage{fontspec,tabularx,tabulary,fp,numprint,etoolbox,enumitem,cellspace,color,colortbl,titlesec,adjustbox,forloop,amssymb,setspace,multicol,multido}
\usepackage[margin=0.5in]{geometry}
\usepackage[table]{xcolor}

\setmainfont[Scale=0.90]{PT Sans}
\newfontfamily\titlett{Aniron}
\newfontfamily\sectiontt[UprightFont={* Bold}]{PT Sans}
\newfontfamily\spelldesctt[Scale=0.75]{PT Sans}
\titleformat{\section}{\titlett}{}{}{}{}

\pagestyle{empty}
\tymin=1.5in

\addparagraphcolumntypes{X}
\cellspacetoplimit 3pt
\cellspacebottomlimit 3pt
\setlength{\parindent}{0pt}
\setlength{\columnsep}{0.5cm}
\setlength{\multicolsep}{0pt}

\definecolor{gray}{rgb}{0.75,0.75,0.75}
\definecolor{yellow}{rgb}{1.00,1.00,0.75}
\definecolor{oddrow}{rgb}{0.90,0.90,1.00}
\definecolor{evenrow}{rgb}{0.80,0.80,0.90}
\definecolor{spellcolor0}{rgb}{0.90,0.90,0.90}
\definecolor{spellcolor1}{rgb}{1.00,0.60,0.60}
\definecolor{spellcolor2}{rgb}{1.00,0.80,0.60}
\definecolor{spellcolor3}{rgb}{0.90,0.90,0.60}
\definecolor{spellcolor4}{rgb}{0.70,1.00,0.60}
\definecolor{spellcolor5}{rgb}{0.60,1.00,0.80}
\definecolor{spellcolor6}{rgb}{0.60,0.90,0.90}
\definecolor{spellcolor7}{rgb}{0.60,0.70,1.00}
\definecolor{spellcolor8}{rgb}{0.70,0.60,1.00}
\definecolor{spellcolor9}{rgb}{0.90,0.60,0.90}

\newenvironment{charactersheet}
  {
    \def\profbonus{2}
    \def\nonprofbonus{0}

    \def\attrstr{0}
    \def\attrdex{0}
    \def\attrcon{0}
    \def\attrint{0}
    \def\attrwis{0}
    \def\attrcha{0}

    \def\attrac{0}
    \def\attrhp{0}
    \def\attrinit{0}
    \def\attrspeed{0}

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

    \def\numspellcols{3}

    \def\classlabel{Class}

    \newcounter{ct}

    \newcommand{\givencharactername}{John Doe}
    \newcommand{\charclasses}{}
    \newcommand{\charrace}{}
    \newcommand{\charalignment}{}
    \newcommand{\charbg}{}
    \newcommand{\attacks}{\hline}
    \newcommand{\traits}{}
    \newcommand{\abilities}{}
    \newcommand{\languages}{}
    \newcommand{\resources}{}
    \newcommand{\skills}{}
    \newcommand{\spells}{}
    \newcommand{\spelldcs}{}
    \newcommand{\spellclass}{}
    \newcommand{\equipment}{}
    \newcommand{\magicitems}{}
    \newcommand{\charactername}[1]{\renewcommand{\givencharactername}{##1}}
    \newcommand{\setrace}[1]{\renewcommand{\charrace}{##1}}
    \newcommand{\setalignment}[1]{\renewcommand{\charalignment}{##1}}
    \newcommand{\setbg}[1]{\renewcommand{\charbg}{##1}}
    \newcommand{\addclass}[2]{\ifdefempty{\charclasses}{}{\def\classlabel{Classes}} \edef\charclasses{\ifdefempty{\charclasses}{}{\charclasses{},} ##1 (##2)}}
    \newcommand{\addattack}[5]{\expandafter\def\expandafter\attacks\expandafter{\attacks{} ##1 & \textbf{##2} & \textbf{##3} & ##4 & ##5 \\ \hline}}
    \newcommand{\addtrait}[1]{\expandafter\def\expandafter\traits\expandafter{\traits{} \item ##1 }}
    \newcommand{\addability}[1]{\expandafter\def\expandafter\abilities\expandafter{\abilities{} \item ##1}}
    \newcommand{\addnamedability}[2]{\expandafter\def\expandafter\abilities\expandafter{\abilities{} \item \textbf{##1:} ##2}}
    \newcommand{\addlang}[1]{\edef\languages{\ifdefempty{\languages}{}{\languages{},} ##1}}
    \newcommand{\addequip}[1]{\expandafter\def\expandafter\equipment\expandafter{\equipment{} \item ##1 }}
    \newcommand{\addmagicitem}[2]{\expandafter\def\expandafter\magicitems\expandafter{\magicitems{} \item \textbf{##1} \\ ##2}}
    \newcommand{\addresource}[3]{\expandafter\def\expandafter\resources\expandafter{\resources{} ##1 & \forloop{ct}{0}{\value{ct} < ##2}{ $\square$ } & ##3 \\ \hline }}
    \newcommand{\addspell}[9]{\expandafter\def\expandafter\spells\expandafter{\spells{}
        \begin{minipage}{\linewidth}
          \adjustbox{left=\linewidth,fbox,bgcolor=spellcolor##4}{
            \textbf{##1} \hspace*{\fill} {\spelldesctt \setstretch{0.7} ##3}
          }
          \par\vspace{0.5em}
          \par\noindent{\spelldesctt \setstretch{0.7} \ifthenelse{\equal{##2}{True}}{\textit{Ritual} $\cdot$ }{} \textit{##7} $\cdot$ \textit{##5}} \\
          \par\vspace{-0.5em}
          \par\noindent{\spelldesctt \setstretch{0.7} ##9 \par}
          \par\vspace{0.5em}
          \par\noindent{\spelldesctt \setstretch{0.7} \textit{Range: ##6} $\cdot$ \textit{Duration: ##8}} \\
          \par\vspace{1em}
        \end{minipage}
    }}

    \newcommand{\setattr}[2]{\@namedef{attr##1}{##2}}
    \newcommand{\setprof}[2]{\@namedef{prof##1}{##2}}
    \newcommand{\setprofbonus}[1]{\def\profbonus{##1}}
    \newcommand{\setnonprofbonus}[1]{\def\nonprofbonus{##1}}

    \newcommand{\abilityscore}[1]{\FPeval{\result}{round(trunc(round(##1 / 2,1),0) - 5,0)} \textbf{\numprint{\result}}}
    \newcommand{\skillvalue}[2]{\FPeval{\result}{round(trunc(round(##1 / 2,1),0) - 5 + max((##2 * \profbonus),\nonprofbonus),0)} \textbf{\numprint{\result}}}
    \newcommand{\calcspelldc}[1]{\FPeval{\result}{trunc(8 + \profbonus + round(trunc(round(\@nameuse{attr##1} / 2,1),0) - 5,0), 0)}\textbf{\numprint{\result}}}

    \newcommand{\addspelldc}[2]{\expandafter\def\expandafter\spelldcs\expandafter{\spelldcs{} ##1 Spell DC & \calcspelldc{##2} \\ \hline}}

    \newcommand{\skillrow}[3]{##1 \hfill \multido{}{\@nameuse{prof##2}}{\checkmark} & \skillvalue{\@nameuse{attr##3}}{\@nameuse{prof##2}}}
  }
  {
    {\large\titlett \givencharactername \par}
    \vspace{-0.5em}
    \rule{\textwidth}{0.4pt}

    \adjustbox{left=0.45\linewidth,valign=t}{
      \noindent\begin{tabulary}{\linewidth}{LJ}
        \ifdefempty{\charrace}{}{{\sectiontt Race} & \charrace \\}
        \ifdefempty{\charclasses}{}{{\sectiontt \classlabel} & \charclasses \\}
        \ifdefempty{\charbg}{}{{\sectiontt Background} & \charbg \\}
        \ifdefempty{\charalignment}{}{{\sectiontt Alignment} & \charalignment \\}
      \end{tabulary}
    }
    \adjustbox{left=0.05\linewidth,valign=t}{
      \hspace{0.05\textwidth}
    }
    \adjustbox{left=0.45\linewidth,valign=t}{
      \noindent\begin{tabulary}{\linewidth}{LJ}
        \ifdefempty{\languages}{}{{\sectiontt Languages} & \languages} \\
      \end{tabulary}
    }

    \vspace{0.5em}

    \rule{\textwidth}{0.4pt}
    \vspace{0.5em}

    \begin{minipage}[t]{0.30\textwidth}
      \section*{Attributes and Skills}
      \rowcolors{2}{oddrow}{evenrow}
      \noindent\begin{tabularx}{\linewidth}{ |X|Sc| }
        \hline
        \rowcolor{yellow} Hit Points & \textbf{\numprint{\attrhp}} \\
        \hline
        \rowcolor{yellow} Armor Class & \textbf{\numprint{\attrac}} \\
        \hline
        \hiderowcolors
        \multicolumn{2}{c}{} \\
        \showrowcolors
        \hline
        Initiative & \textbf{\numprint{\attrinit}} \\
        \hline
        Speed & \textbf{\numprint{\attrspeed}} \\
        \hline
        \spelldcs
        \hiderowcolors
        \multicolumn{2}{c}{} \\
        \showrowcolors
        \hline
        Strength & \textbf{\abilityscore{\attrstr}} (\attrstr) \\
        \hline
        Dexterity & \textbf{\abilityscore{\attrdex}} (\attrdex) \\
        \hline
        Constitution & \textbf{\abilityscore{\attrcon}} (\attrcon) \\
        \hline
        Intelligence & \textbf{\abilityscore{\attrint}} (\attrint) \\
        \hline
        Wisdom & \textbf{\abilityscore{\attrwis}} (\attrwis) \\
        \hline
        Charisma & \textbf{\abilityscore{\attrcha}} (\attrcha) \\
        \hline
        \hiderowcolors
        \multicolumn{2}{c}{} \\
        \showrowcolors
        \hline
        \skillrow{Acrobatics}{acrobatics}{dex} \\
        \hline
        \skillrow{Arcana}{arcana}{int} \\
        \hline
        \skillrow{Athletics}{athletics}{str} \\
        \hline
        \skillrow{Deception}{deception}{cha} \\
        \hline
        \skillrow{Handle Animal}{handleanimal}{wis} \\
        \hline
        \skillrow{History}{history}{int} \\
        \hline
        \skillrow{Insight}{insight}{wis} \\
        \hline
        \skillrow{Intimidate}{intimidate}{cha} \\
        \hline
        \skillrow{Investigation}{investigation}{int} \\
        \hline
        \skillrow{Medicine}{medicine}{wis} \\
        \hline
        \skillrow{Nature}{nature}{int} \\
        \hline
        \skillrow{Perception}{perception}{wis} \\
        \hline
        \skillrow{Performance}{performance}{cha} \\
        \hline
        \skillrow{Persuasion}{persuasion}{cha} \\
        \hline
        \skillrow{Religion}{religion}{int} \\
        \hline
        \skillrow{Sleight of Hand}{sleightofhand}{dex} \\
        \hline
        \skillrow{Stealth}{stealth}{dex} \\
        \hline
        \skillrow{Survival}{survival}{wis} \\
        \hline
        \hiderowcolors
        \multicolumn{2}{c}{} \\
        \showrowcolors
        \hline
        \skillrow{Strength Save}{strsave}{str} \\
        \hline
        \skillrow{Dexterity Save}{dexsave}{dex} \\
        \hline
        \skillrow{Constitution Save}{consave}{con} \\
        \hline
        \skillrow{Intelligence Save}{intsave}{int} \\
        \hline
        \skillrow{Wisdom Save}{wissave}{wis} \\
        \hline
        \skillrow{Charisma Save}{chasave}{cha} \\
        \hline
      \end{tabularx}
      \vspace{2em}

    \end{minipage}
    \begin{minipage}[t]{0.05\textwidth}
      \hspace{0.05\textwidth}
    \end{minipage}
    \begin{minipage}[t]{0.65\textwidth}

      \ifdefempty{\traits}{}{
        \section*{Traits, Ideals, Bonds, and Flaws}
        \begin{itemize}[noitemsep]
          \small\traits
        \end{itemize}
      }

      \section*{Attacks}
      \noindent\begin{tabularx}{\textwidth}{ |X|Sc|Sc|Sc|Sc| }
        \hline
        \rowcolor{gray} \textbf{Attack} & \textbf{Hit Bonus} & \textbf{Damage} & \textbf{Type} & \textbf{Range} \\
        \attacks
      \end{tabularx}

      \ifdefempty{\resources}{}{
        \section*{Resources}
        \noindent\begin{tabularx}{\textwidth}{ |X|Sl|Sc| }
          \hline
          \rowcolor{gray} \textbf{Resource Type} & & \textbf{Restored After} \\
          \hline
          \resources
        \end{tabularx}
      }

      \ifdefempty{\abilities}{}{
        \section*{Abilities}
        \begin{itemize}[noitemsep]
          \small\abilities
        \end{itemize}
      }

      \ifdefempty{\magicitems}{}{
        \section{Magic Items}
        \begin{itemize}[noitemsep]
          \small\magicitems
        \end{itemize}
      }

      \ifdefempty{\equipment}{}{
        \begin{multicols*}{3}[\section*{Equipment}]
          \begin{itemize}[noitemsep]
            \small\equipment
          \end{itemize}
        \end{multicols*}
      }

    \end{minipage}

    \clearpage

    \ifdefempty{\spells}{}{
      \begin{multicols}{\numspellcols}[\section*{Spells}]
        \spells
      \end{multicols}
    }
  }
