view: national_pension_category_summary {

  derived_table: {
    sql: select
      create_yearmonth,
      biz_category_code,
      biz_category,
      sum(num_of_members) as sum_of_members,
      avg(num_of_members) as avg_of_members,
      sum(monthly_fixed_amount) as sum_of_monthly_fixed_amount,
      avg(monthly_fixed_amount) as avg_of_monthly_fixed_amount,
      sum(num_of_new_member) as sum_of_new_members,
      avg(num_of_new_member) as avg_of_new_members,
      sum(num_of_lost_members) as sum_of_lost_members,
      avg(num_of_lost_members) as avg_of_lost_members
    from
      sample_ds.national_pension_raw
    where register_status = 1
    group by create_yearmonth, biz_category_code, biz_category
      ;;

    materialized_view: yes
  }

  dimension: create_yearmonth {
    type: string
    hidden: yes
    sql: ${TABLE}.create_yearmonth ;;
  }

  dimension_group: data_create_yearmonth {
    description: "This field is generally avaiable to check company information."
    type: time
    sql: cast(concat(${create_yearmonth}, '-01') as date) ;;
    datatype:  date
    timeframes: [
      month,
      quarter,
      year
    ]
  }

  dimension: biz_category {
    type: string
    hidden: yes
    sql: ${TABLE}.biz_category ;;
  }

  dimension: biz_category_code {
    type: string
    hidden: yes
    sql: ${TABLE}.biz_category_code ;;
  }

  dimension: sum_of_members_per_category {
    type: number
    sql: ${TABLE}.sum_of_members ;;
  }

  dimension: avg_of_members_per_category {
    type: number
    sql: ${TABLE}.avg_of_members ;;
  }

  dimension: sum_of_monthly_fixed_amount_per_category {
    type: number
    sql: ${TABLE}.sum_of_monthly_fixed_amount ;;
  }

  dimension: avg_of_monthly_fixed_amount_per_category {
    type: number
    sql: ${TABLE}.avg_of_monthly_fixed_amount ;;
  }

  dimension: sum_of_new_members_per_category {
    type: number
    sql: ${TABLE}.sum_of_new_members ;;
  }

  dimension: avg_of_new_members_per_category {
    type: number
    sql: ${TABLE}.avg_of_new_members ;;
  }

  dimension: sum_of_lost_members_per_category {
    type: number
    sql: ${TABLE}.sum_of_lost_members ;;
  }

  dimension: avg_of_lost_members_per_category {
    type: number
    sql: ${TABLE}.avg_of_lost_members ;;
  }

  measure: sum_of_members {
    description: "Use this for sum of total members in the industry segment."
    type: sum
    sql: ${sum_of_members_per_category} ;;
  }

  measure: avg_of_members {
    description: "Use this for average of total members in the industry segment."
    type: average
    sql: ${avg_of_members_per_category} ;;
  }

  measure: corp_count {
    description: "The number of corporation in the industry segment."
    type: count
  }

  measure: sum_of_monthly_fixed_amount {
    description: "Use this for sum of monthly national pension in the industry segment."
    type: sum
    sql: ${sum_of_monthly_fixed_amount_per_category} ;;
  }

  measure: avg_of_monthly_fixed_amount {
    description: "Use this for average of monthly national pension in the industry segment."
    type: average
    sql: ${avg_of_monthly_fixed_amount_per_category} ;;
  }

  measure: sum_of_new_members {
    description: "Use this for sum of monthly new employees in the industry segment."
    type: sum
    sql: ${sum_of_new_members_per_category} ;;
  }

  measure: avg_of_new_members {
    description: "Use this for average of monthly new employees in the industry segment."
    type: sum
    sql: ${avg_of_new_members_per_category} ;;
  }

  measure: sum_of_lost_members {
    description: "Use this for sum of monthly lost employees in the industry segment."
    type: sum
    sql: ${sum_of_lost_members_per_category} ;;
  }

  measure: avg_of_lost_members {
    description: "Use this for average of monthly lost employees in the industry segment."
    type: average
    sql: ${avg_of_lost_members_per_category} ;;
  }

  # measure: sum_of_new_members {
  #   description: "Use this for sum of new monthly members in the industry segment."
  #   type: number
  #   sql: ${TABLE}.sum_of_monthly_fixed_amount ;;
  # }

  # measure: avg_of_new_members {
  #   description: "Use this for average of new monthly members in the industry segment."
  #   type: number
  #   sql: ${TABLE}.avg_of_monthly_fixed_amount ;;
  # }
  # measure: sum_of_lost_members {
  #   description: "Use this for sum of lost monthly members in the industry segment."
  #   type: number
  #   sql: ${TABLE}.sum_of_monthly_fixed_amount ;;
  # }

  # measure: avg_of_lost_members {
  #   description: "Use this for average of lost monthly members in the industry segment."
  #   type: number
  #   sql: ${TABLE}.avg_of_monthly_fixed_amount ;;
  # }
}
