view: national_pension_mom {

  parameter: compared_month {
    type: number
  }

  derived_table: {
    sql:
    select
      create_yearmonth,
      biz_workplace_name,
      biz_regid,
      register_status,
      postal_code,
      address_townbase,
      address_streetbase,
      legal_address_code,
      admin_address_code,
      prov_code,
      county_code,
      town_code,
      legal_personal_type,
      biz_category_code,
      biz_category,
      applied_date,
      reregistered_date,
      expired_date,
      num_of_members,
      monthly_fixed_amount,
      num_of_new_member,
      num_of_lost_members,
      lag(postal_code,{% parameter compared_month %}) over (partition by biz_workplace_name, biz_regid order by create_yearmonth) as postal_code_compared,
      lag(num_of_members, {% parameter compared_month %}) over (partition by biz_workplace_name, biz_regid order by create_yearmonth) as num_of_members_compared,
      lag(monthly_fixed_amount, {% parameter compared_month %}) over (partition by biz_workplace_name, biz_regid order by create_yearmonth) as monthly_fixed_amount_compared,
      lag(num_of_new_member, {% parameter compared_month %}) over (partition by biz_workplace_name, biz_regid order by create_yearmonth) as num_of_new_member_compared,
      lag(num_of_lost_members, {% parameter compared_month %}) over (partition by biz_workplace_name, biz_regid order by create_yearmonth) as num_of_lost_members_compared
    from
      sample_ds.national_pension_raw
        ;;
    # interval_trigger: "24 hours"
  }

  filter: current_date_3 {
    type: date
    sql: date_sub(CURRENT_DATE(), interval 3 day) ;;
  }

  dimension: address_streetbase {
    type: string
    sql: ${TABLE}.address_streetbase ;;
  }

  dimension: address_townbase {
    type: string
    sql: ${TABLE}.address_townbase ;;
  }

  dimension: admin_address_code {
    type: string
    sql: ${TABLE}.admin_address_code ;;
  }

  # dimension_group: applied {
  #   description: "This field is only usable to check new creation date of the company."
  #   type: time
  #   timeframes: [
  #     raw,
  #     time,
  #     date,
  #     week,
  #     month,
  #     quarter,
  #     year
  #   ]
  #   datatype: datetime
  #   sql: ${TABLE}.applied_date ;;
  # }

  dimension: biz_category {
    type: string
    sql: ${TABLE}.biz_category ;;
  }

  dimension: biz_category_code {
    type: string
    sql: ${TABLE}.biz_category_code ;;
  }

  dimension: biz_regid {
    type: string
    sql: ${TABLE}.biz_regid ;;
  }

  dimension: biz_workplace_name {
    type: string
    sql: ${TABLE}.biz_workplace_name ;;
  }

  dimension: county_code {
    type: number
    sql: ${TABLE}.county_code ;;
  }

  dimension: create_yearmonth {
    type: string
    sql: ${TABLE}.create_yearmonth ;;
  }

  dimension_group: expired {
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    datatype: datetime
    sql: ${TABLE}.expired_date ;;
  }

  dimension: legal_address_code {
    type: string
    sql: ${TABLE}.legal_address_code ;;
  }

  dimension: legal_personal_type {
    type: number
    sql: ${TABLE}.legal_personal_type ;;
  }

  dimension: monthly_fixed_amount {
    type: number
    sql: ${TABLE}.monthly_fixed_amount ;;
  }

  # dimension: previous_month_monthly_fixed_amount {
  #   type: number
  #   sql: lag(${TABLE}.monthly_fixed_amount,1) over (partition by ${biz_category_code}, ${create_yearmonth} order by ${create_yearmonth})  ;;
  # }
  # Dimension defined in this 'Dimension' segment will show the following error. Analytic functions cannot be arguments to aggregate functions at [35:5]

  dimension: num_of_lost_members {
    type: number
    sql: ${TABLE}.num_of_lost_members ;;
  }

  dimension: num_of_members {
    type: number
    sql: ${TABLE}.num_of_members ;;
  }

  dimension: num_of_new_member {
    type: number
    sql: ${TABLE}.num_of_new_member ;;
  }

  dimension: postal_code {
    type: string
    sql: ${TABLE}.postal_code ;;
  }

  dimension: prov_code {
    type: number
    sql: ${TABLE}.prov_code ;;
  }

  dimension: register_status {
    type: number
    sql: ${TABLE}.register_status ;;
  }

  dimension_group: reregistered {
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    datatype: datetime
    sql: ${TABLE}.reregistered_date ;;
  }

  dimension: town_code {
    type: number
    sql: ${TABLE}.town_code ;;
  }

  dimension: postal_code_compared {
    type: string
    sql: ${TABLE}.postal_code_compared ;;
  }

  dimension: num_of_members_compared {
    type: number
    sql: ${TABLE}.num_of_members_compared ;;
  }

  dimension: monthly_fixed_amount_compared {
    type: number
    sql: ${TABLE}.monthly_fixed_amount_compared ;;
  }

  dimension: num_of_new_member_compared {
    type: number
    sql: ${TABLE}.num_of_new_member_compared ;;
  }

  dimension: num_of_lost_members_compared {
    type: number
    sql: ${TABLE}.num_of_lost_members_compared ;;
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

  set: corporation_detail {
    fields: [
      biz_workplace_name,
      address_townbase,
      biz_category
    ]
  }

  measure: average_monthly_fixed_amount {
    type: average
    sql: ${TABLE}.monthly_fixed_amount ;;
    drill_fields: [ corporation_detail* ]
  }

  measure: average_monthly_fixed_amount_compared {
    type: average
    sql: ${TABLE}.monthly_fixed_amount_compared ;;
    drill_fields: [ corporation_detail* ]
  }

  measure: total_monthly_fixed_amount {
    type: sum
    sql: ${TABLE}.monthly_fixed_amount ;;
    drill_fields: [ corporation_detail* ]
  }

  measure: total_monthly_fixed_amount_compared {
    type: sum
    sql: ${TABLE}.monthly_fixed_amount_compared ;;
    drill_fields: [ corporation_detail* ]
  }

  dimension: monthly_fixed_amount_mom {
    type:  number
    sql:  ${monthly_fixed_amount} - ${monthly_fixed_amount_compared} ;;
  }

  measure: total_monthly_fixed_mon_amount {
    type:  sum
    sql: ${monthly_fixed_amount_mom} ;;
    drill_fields: [ corporation_detail* ]
  }

  measure: average_monthly_fixed_mom_amount {
    type: average
    sql: ${monthly_fixed_amount_mom} ;;
    html: {% if value > 100 %}
         <p style="color: red; font-size: 50%">{{ rendered_value }}</p>
       {% elsif value >1000 %}
         <p style="color: blue; font-size:80%">{{ rendered_value }}</p>
       {% else %}
         <p style="color: black; font-size:100%">{{ rendered_value }}</p>
       {% endif %};;
    drill_fields: [ corporation_detail* ]
  }

  measure: average_monthly_amount_mom_ratio {
    type: number
    sql:  IFNULL(safe_divide(${average_monthly_fixed_mom_amount},${average_monthly_fixed_amount}),0) ;;
    drill_fields: [ corporation_detail* ]
  }

  measure: count {
    type: count
    drill_fields: [biz_workplace_name]
  }
}
