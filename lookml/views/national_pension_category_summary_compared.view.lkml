include: "national_pension_category_summary.view"

view: national_pension_category_summary_compared {
  extends: [national_pension_category_summary]

  parameter: compared_month {
    type: number
    description: "If you want to compare two different measures in two different months, use it. If you set this value, this 'compared' view will generate lagged statistics."
  }

  dimension_group: data_create_yearmonth_lagged {
    description: "This field will be used as join phrase to compare original create date and this lagged date."
    type: time
    sql: cast(concat(${create_yearmonth}, '-01') as date) - INTERVAL {% parameter compared_month %} MONTH;;
    datatype:  date
    timeframes: [
      month,
      quarter,
      year
    ]
  }

}
