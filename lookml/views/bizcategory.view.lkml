view: bizcategory {
  sql_table_name: `sample_ds.bizcategory`
    ;;

  dimension: cat_code {
    type: string
    sql: ${TABLE}.cat_code ;;
  }

  dimension: cat_l1 {
    type: string
    sql: ${TABLE}.cat_l1 ;;
    description : "In general, largest catgories in Korea Industry segment table such like 건설업, 제조업"
    drill_fields: [
      cat_l2, cat_l3, cat_l4
    ]
  }

  filter: filter_cat_l1 {
    type: string
    suggest_dimension: bizcategory.cat_l1
  }

  dimension: cat_l1_code {
    type: string
    sql: ${TABLE}.cat_l1_code ;;
  }

  dimension: filtered_l1_code {
    type: string
    sql: ${TABLE}.cat_l1_code = ${filter_cat_l1} ;;
  }

  filter: filter_cat_l2 {
    type:  string
    suggest_dimension: bizcategory.cat_l2
    description : "Middle size category in Korea Industry segment table such like 석탄 원유 및 천연가스 광업, 금속 광업, 비금속광물 광업; 연료용 제외"
  }

  dimension: cat_l2 {
    type: string
    sql: ${TABLE}.cat_l2 ;;
    drill_fields: [
      cat_l3, cat_l4
    ]
  }

  dimension: cat_l2_code {
    type: string
    sql: ${TABLE}.cat_l2_code ;;
  }

  dimension: cat_l3 {
    type: string
    sql: ${TABLE}.cat_l3 ;;
    drill_fields: [
      cat_l4
    ]
  }

  dimension: cat_l3_code {
    type: string
    sql: ${TABLE}.cat_l3_code ;;
  }

  dimension: cat_l4 {
    type: string
    sql: ${TABLE}.cat_l4 ;;
  }

  dimension: cat_l4_code {
    type: string
    sql: ${TABLE}.cat_l4_code ;;
  }

  dimension: cat_l5 {
    type: string
    sql: ${TABLE}.cat_l5 ;;
  }

  set: cat_drill_set {
    fields: [
      cat_l1
      , cat_l2
      , cat_l3
      , cat_l4
    ]
  }

  measure: count {
    type: count
    drill_fields: []
  }
}
