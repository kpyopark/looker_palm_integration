connection: "bigquery-connection"

# include all the views
include: "/views/**/*.view"

datagroup: lookml_hol_sample_default_datagroup {
  # sql_trigger: SELECT MAX(id) FROM etl_log;;
  max_cache_age: "1 hour"
}

persist_with: lookml_hol_sample_default_datagroup

explore: postal_location {}

explore: bizcategory {
  description: "이 View는 한국 산업 코드 정보를 담고 있습니다. 대분류(Catl1)부터 세분류(CatL4)까지 가지고 있으며, 산업코드를 구분짓는데 사용합니다. "
}

#explore: bizcategory_vw {}

#explore: custom_biz {}

#explore: national_pension_raw {}

explore: national_pension_category_summary {
  description: "이 화면은 국민연금에 대한 산업별 월 단위 통계 정보를 제공합니다. 제공되는 정보는 다음과 같습니다.
평균/총 근로자 수
평균/총 연금 납부액
평균/총 신규 근로자 수
평균/총 실업 근로자 수
또한, 이 화면은 월별 통계를 비교할 수 있는 추가적인 기능도 제공합니다."

  always_filter: {
    filters : [national_pension_category_summary_compared.compared_month: "1"]
  }

  join: bizcategory {
    type: inner
    sql_on: ${national_pension_category_summary.biz_category_code} = ${bizcategory.cat_code} ;;
    relationship: one_to_one
  }

  join: national_pension_category_summary_compared {
    type: inner
    sql_on: ${national_pension_category_summary.data_create_yearmonth_month} = ${national_pension_category_summary_compared.data_create_yearmonth_lagged_month}
    and ${national_pension_category_summary.biz_category_code} = ${national_pension_category_summary_compared.biz_category_code};;
    relationship:  one_to_one
  }

}


explore: national_pension_mom {
  description: "This view provides monthly company-specific payment details for the National Pension Service. It includes information on the number of employees who contribute to the company's pension, and the amount of pension paid by the company. And also it includes gelocation information."

  always_filter: {
    filters : [national_pension_mom.data_create_yearmonth_year: "2022", national_pension_mom.compared_month: "1"]
  }

  join: bizcategory {
    type: inner
    sql_on: ${national_pension_mom.biz_category_code} = ${bizcategory.cat_code} ;;
    relationship: one_to_one
  }
  join: postal_location {
    from: postal_location
    type: inner
    sql_on: ${national_pension_mom.postal_code} = ${postal_location.postcode} ;;
    relationship:  one_to_one
  }
  join: postal_old_location {
    from: postal_location
    type: inner
    sql_on: ${national_pension_mom.postal_code_compared} = ${postal_old_location.postcode} ;;
    relationship:  one_to_one
  }

}
