#' Calculate Required Coffee for Debugging Session
#'
#' Estimates caffeine needs based on debugging complexity.
#'
#' @param error_messages Integer. Number of different error messages seen
#' @param browser_tabs Integer. Browser tabs currently open to find solution
#' @param hours_stuck Numeric. Hours spent on current bug
#'
#' @return Integer. Recommended cups of coffee (max 3 for your health)
#'
#' @examples
#' coffee_for_debugging(1, 2, 0.5)
#' coffee_for_debugging(5, 12, 4)  # Consider a walk instead
#'
#' @author Caffeinated Coder
#' @seealso \code{traceback()}, \code{browser()}
#' @export
coffee_for_debugging <- function(
  error_messages,
  browser_tabs,
  hours_stuck
) {
  coffee_needed <- error_messages + (browser_tabs * 0.2) + hours_stuck

  # Cap at 3 cups for sanity and health
  result <- min(ceiling(coffee_needed), 3)

  if (result >= 3) {
    message("Maybe try rubber duck debugging instead?")
  }

  return(result)
}
