# Log Group para Glue
resource "aws_cloudwatch_log_group" "glue_logs" {
  name              = "/aws-glue/jobs/${var.project}-${var.env}"
  retention_in_days = 7
}

# Alarma: fallos de Glue Job
resource "aws_cloudwatch_metric_alarm" "glue_job_failure" {
  alarm_name          = "${var.project}-${var.env}-glue-failure"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "glue.driver.aggregate.numFailedTasks"
  namespace           = "Glue"
  period              = 300
  statistic           = "Sum"
  threshold           = 0

  alarm_description = "Alarma cuando falla el Glue Job"

  dimensions = {
    JobName = var.glue_job_name
  }
}

# Dashboard básico
resource "aws_cloudwatch_dashboard" "dashboard" {
  dashboard_name = "${var.project}-${var.env}-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric",
        x    = 0,
        y    = 0,
        width  = 12,
        height = 6,

        properties = {
          metrics = [
            ["Glue", "glue.driver.aggregate.numCompletedTasks", "JobName", var.glue_job_name],
            [".", "glue.driver.aggregate.numFailedTasks", ".", "."]
          ],
          period = 300,
          stat   = "Sum",
          region = var.region,
          title  = "Glue Job Metrics"
        }
      }
    ]
  })
}