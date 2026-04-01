output "log_group_name" {
  value = aws_cloudwatch_log_group.glue_logs.name
}

output "alarm_name" {
  value = aws_cloudwatch_metric_alarm.glue_job_failure.alarm_name
}