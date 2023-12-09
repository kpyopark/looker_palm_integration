view: postal_location {

  sql_table_name: `sample_ds.postal_location`
    ;;

  dimension: latitude {
    type: number
    sql: ${TABLE}.latitude ;;
  }

  dimension: latitude_l1 {
    type: number
    sql: ${TABLE}.latitude_l1 ;;
  }

  dimension: latitude_l2 {
    type: number
    sql: ${TABLE}.latitude_l2 ;;
  }

  dimension: latitude_l3 {
    type: number
    sql: ${TABLE}.latitude_l3 ;;
  }

  dimension: longitude {
    type: number
    sql: ${TABLE}.longitude ;;
  }

  dimension: longitude_l1 {
    type: number
    sql: ${TABLE}.longitude_l1 ;;
  }

  dimension: longitude_l2 {
    type: number
    sql: ${TABLE}.longitude_l2 ;;
  }

  dimension: longitude_l3 {
    type: number
    sql: ${TABLE}.longitude_l3 ;;
  }

  dimension: postcode {
    type: string
    sql: ${TABLE}.postcode ;;
  }

  dimension: postcode_l1 {
    type: string
    sql: ${TABLE}.postcode_l1 ;;
  }

  dimension: postcode_l2 {
    type: string
    sql: ${TABLE}.postcode_l2 ;;
  }

  dimension: postcode_l3 {
    type: string
    sql: ${TABLE}.postcode_l3 ;;
  }

  dimension: loc_l1 {
    type:  location
    sql_longitude: ${longitude_l1} ;;
    sql_latitude: ${latitude_l1} ;;
  }

  dimension: loc_l2 {
    type:  location
    sql_longitude: ${longitude_l2} ;;
    sql_latitude: ${latitude_l2} ;;
  }

  dimension: loc_l3 {
    type:  location
    sql_longitude: ${longitude_l3} ;;
    sql_latitude: ${latitude_l3} ;;
  }

  dimension: loc {
    type: location
    sql_longitude: ${longitude} ;;
    sql_latitude: ${latitude} ;;
  }

  measure: count {
    type: count
    drill_fields: []
  }
}
