## Retriever for predefined SQLs.

사전에, 이미 Vector Database에 Predefined SQL이 적재되어 있는 상태여야 합니다. (nl_to_sql2.ipynb 참조) 

이를 사용자 Question에 맞추어 필터를 추출하고, 사용자에게 결과값을 제시해 주는 서비스입니다.
필요에 따라서는 SQL자체를 제시하는 방법도 가능합니다.

사용하기 전에 아래 .env 파일을 생성을 하거나, CloudRun환경에서 Environment Variable을 추가하세요.

(.env파일에 있어야하는 항목들)

    export LOCATION=<<vector table이 존재하는 리젼>>
    export TARGET_LOCATION=<<업무 테이블이 존재하는 리젼. 간혹 Vector Table이 있는 Region과 실제 없무 Table들이 있는 리젼이 다른경우가 있어서 추가함.>>
    export DATASET=<<vector table이 존재하는 리젼>>
    export TABLE_NAME=<<vector table명>>
    export PROJECT_ID=<<project id>>


### cloud run deploy

gcloud cli를 설치했다고 가정한다. 

service key가 local에 설치되었다고 가정한다. 

terminal상에서, 

    $ cd cloudrun/predefined_query_retriever
    $ gcloud run deploy


## DialogFlow CS에 Open API Tool추가하기

상위 폴더에 있는 README.md 파일 참조