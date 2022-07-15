resource "aws_budgets_budget" "ecs" {
  name              = "budget-ecs-monthly-${terraform.workspace}"
  budget_type       = "COST"
  limit_amount      = "100"
  limit_unit        = "USD"
  time_period_end   = "2087-06-15_00:00"
  time_period_start = "2022-07-01_00:00"
  time_unit         = "MONTHLY"

  cost_filter {
    name = "Service"
    values = [
      "Amazon Elastic Container Service"
    ]
  }
  cost_filter {
    name = "TagKeyValue"
    values = [
      join("$", ["user:Environment", terraform.workspace])
    ]
  }

  cost_types {
    include_credit             = false
    include_discount           = false
    include_subscription       = false
    include_tax                = false
    include_upfront            = false
    include_other_subscription = false
    include_refund             = false
    include_recurring          = false
    include_support            = false
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 85
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["edgardojesus16@gmail.com", "ivan@lazzaro.io"]
  }
}

