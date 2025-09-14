\name{coffee_for_debugging}
\alias{coffee_for_debugging}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{
Calculate Required Coffee for Debugging Session
}
\description{
Estimates caffeine needs based on debugging complexity.
}
\usage{
coffee_for_debugging(error_messages, browser_tabs, hours_stuck)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{error_messages}{Integer. Number of different error messages seen}
  \item{browser_tabs}{Integer. Browser tabs currently open for troubleshooting}
  \item{hours_stuck}{Numeric. Hours spent on current bug}
}

\value{
Integer. Recommended cups of coffee (max 3 for your health)
}

\author{
Caffeinated Coder
}

\examples{
coffee_for_debugging(1, 2, 0.5)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory (show via RShowDoc("KEYWORDS")):
% \keyword{ ~kwd1 }
% \keyword{ ~kwd2 }
% Use only one keyword per line.
% For non-standard keywords, use \concept instead of \keyword:
% \concept{ ~cpt1 }
% \concept{ ~cpt2 }
% Use only one concept per line.
